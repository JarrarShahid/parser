# --- Import Extractors ---
from location_extractor import LocationExtractor
from experience_extractor import NumberExtractor
from skill_extractor import SkillExtractor, skills_expansions, skills_list
from industry_extractor import IndustryExtractor, industry_type_expansion, industry_type
from job_extractor import JobTitleExtractor, job_title_expansion, job_titles
import json
from templates import query_intent_web_search
from dotenv import load_dotenv
import os
import requests
from fastapi import HTTPException


load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_candidate_info(text: str) -> dict:
    """Extract structured candidate information from free text."""
    extractors = {
        "experience": NumberExtractor(),
        "industry": IndustryExtractor(industry_type, industry_type_expansion),
        "job_title": JobTitleExtractor(job_titles, job_title_expansion),
        "location": LocationExtractor(),
        "skills": SkillExtractor(skills_list, skills_expansions),
    }
    return {key: extractor.extract(text) for key, extractor in extractors.items()}


def build_conditions(values, column, condition_type="(.)"):
    """Helper to build OR conditions for a list of values."""
    return [{"column": column, "type": condition_type, "value": v} for v in values]


def build_crust_filters(extracted: dict) -> dict:
    """Build CrustData screener/persondb/search filters JSON from extracted fields."""
    conditions = []

    # --- Experience ---
    if extracted.get("experience"):
        operator_map = {"=": "=", "=>": "=>", "=<": "=<", ">": ">", "<": "<"}
        exp_conditions = [
            {"column": "years_of_experience_raw", "type": operator_map.get(op, "="), "value": num}
            for num, op in extracted["experience"]
            if op in operator_map
        ]
        if exp_conditions:
            conditions.append({"op": "or", "conditions": exp_conditions})

    # --- Industry ---
    if extracted.get("industry"):
        conditions.append({
            "op": "or",
            "conditions": build_conditions(extracted["industry"], "all_employers.company_industries")
        })

    # --- Job Title ---
    if extracted.get("job_title"):
        conditions.append({
            "op": "or",
            "conditions": build_conditions(extracted["job_title"], "current_employers.title")
        })

    # --- Location ---
    if extracted.get("location"):
        conditions.append({
            "op": "or",
            "conditions": build_conditions(extracted["location"], "region")
        })

    # --- Skills ---
    if extracted.get("skills"):
        conditions.append({
            "op": "or",
            "conditions": build_conditions(extracted["skills"], "skills")
        })

    # ✅ Correct structure: filters + siblings limit/preview
    return {
        "filters": {"op": "and", "conditions": conditions},
        "limit": 3,
        "preview": True,
    }

def _extract_json_from_text(text: str):
    """
    Try to locate a JSON object in text and parse it.
    Returns dict on success or raises ValueError.
    """
    text = text.strip()
    # quick path: if starts with { and is valid json
    if text.startswith("{"):
        try:
            return json.loads(text)
        except Exception:
            pass

    # fallback: find first { and last } and try to parse
    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1 and last > first:
        candidate = text[first:last+1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    # regex to match braces might be dangerous; give up
    raise ValueError("No valid JSON object found in model output.")

def call_openai_extract(query_text: str, model: str = OPENAI_MODEL, api_key: str = OPENAI_API_KEY, timeout: int = 30):
    """
    Calls OpenAI ChatCompletions (gpt-3.5-turbo) with the extraction system prompt.
    Returns parsed dict (matching extract_candidate_info output).
    Raises HTTPException on error.
    """
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured on server.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": query_intent_web_search},
            {"role": "user", "content": query_text}
        ],
        "temperature": 0.0,
        "max_tokens": 700,
        "n": 1,
    }

    try:
        resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=timeout)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error contacting OpenAI: {str(e)}")

    if resp.status_code != 200:
        # include body for debugging but not too verbose
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {resp.status_code} - {resp.text}")

    body = resp.json()
    try:
        content = body["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Unexpected OpenAI response format: {str(e)}")

    # Extract JSON from content
    try:
        data = _extract_json_from_text(content)
    except ValueError:
        # Provide helpful debug in 502
        raise HTTPException(status_code=502, detail="OpenAI response did not contain valid JSON as expected.")

    # Basic validation: ensure all five keys exist and are lists
    expected_keys = ["experience", "industry", "job_title", "location", "skills"]
    for k in expected_keys:
        if k not in data or not isinstance(data[k], list):
            raise HTTPException(status_code=502, detail=f"OpenAI returned invalid/missing key: {k}")

    return data