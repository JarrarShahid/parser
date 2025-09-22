from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import uvicorn
from function import extract_candidate_info, build_crust_filters

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

def main():
    print("🚀 Starting FastAPI server....")
    # Run FastAPI server
    port = int(8002)
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    main()