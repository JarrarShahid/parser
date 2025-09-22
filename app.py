from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import uvicorn
from function import (
    extract_candidate_info, 
    build_crust_filters, 
    call_openai_extract)
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")  
CRUST_API_URL = os.getenv("CRUST_API_URL")
CRUST_TOKEN = os.getenv("CRUST_TOKEN")  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")

app = FastAPI()


# ----------------------------
# Pydantic Models
# ----------------------------

class CandidateRequest(BaseModel):
    """Request model for candidate filter generation API."""
    text: str = Field(..., example="Find software engineer with 3 years of experience in React located in Fulda, Germany, experienced in Health Care")


class FilterResponse(BaseModel):
    """Response model containing only the filters JSON."""
    filters: Dict[str, Any]
    limit: int
    preview: bool

# ----------------------------
# FastAPI Endpoint
# ----------------------------

@app.post("/generate-filters", response_model=FilterResponse, tags=["Filters"])
async def generate_filters(request: CandidateRequest):
    """
    Generate CrustData-compatible filters from a free-text candidate search query.
    
    ### Request Body:
    - **text**: Natural language query
    
    ### Response:
    - **filters**: JSON filter object ready for CrustData
    
    ### Error Codes:
    - **400**: Empty or invalid input text
    - **422**: No extractable candidate info found
    - **500**: Unexpected server error
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")

        extracted_info = extract_candidate_info(request.text)

        if not any(extracted_info.values()):
            raise HTTPException(
                status_code=422,
                detail="No relevant candidate information could be extracted from the text."
            )

        filters = build_crust_filters(extracted_info)

        return FilterResponse(
            filters=filters["filters"],
            limit=filters["limit"],
            preview=filters["preview"]
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/search-with-filters")
def search_with_filters(request: CandidateRequest):
    # 1. Call your own API to generate filters
    my_response = requests.post(
        f"{BASE_URL}/generate-filters",
        json=request.dict()  # pass the user prompt here
    )
    filters_payload = my_response.json()

    # 2. Call the third-party API with your API's response as body
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{CRUST_TOKEN}"
    }
    crust_response = requests.post(
        CRUST_API_URL,
        headers=headers,
        json=filters_payload
    )

    return crust_response.json()

@app.post("/search-with-filters-ai", tags=["Filters"])
def search_with_filters_ai(request: CandidateRequest):
    """
    New flow:
    - Use GPT-3.5 (query_intent_web_search prompt) to extract candidate info from the input text.
    - Build filters via build_crust_filters(...)
    - Forward filters to Crust API and return Crust response.

    Error codes:
    - 400: bad client input
    - 502: upstream (OpenAI/Crust) errors
    - 500: server errors
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")

        # 1) Get extracted info from the AI
        extracted_info = call_openai_extract(request.text)

        # 2) Build crust filters locally
        filters = build_crust_filters(extracted_info)

        # 3) Forward to Crust
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{CRUST_TOKEN}"
        }
        try:
            crust_response = requests.post(CRUST_API_URL, headers=headers, json=filters, timeout=30)
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Error calling Crust API: {str(e)}")

        if crust_response.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"Crust API error: {crust_response.status_code} - {crust_response.text}")

        return crust_response.json()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def main():
    print("🚀 Starting FastAPI server....")
    # Run FastAPI server
    port = int(8002)
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    main()