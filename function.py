# --- Import Extractors ---
from location_extractor import LocationExtractor
from experience_extractor import NumberExtractor
from skill_extractor import SkillExtractor, skills_expansions, skills_list
from industry_extractor import IndustryExtractor, industry_type_expansion, industry_type
from job_extractor import JobTitleExtractor, job_title_expansion, job_titles


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

