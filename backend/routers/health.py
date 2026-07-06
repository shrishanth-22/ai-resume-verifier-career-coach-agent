from fastapi import APIRouter
from backend.agents.base import OPENAI_API_KEY, GITHUB_TOKEN

router = APIRouter(tags=["System health"])

@router.get("/health")
def health_check():
    """Health check endpoint to verify configuration parameters."""
    return {
        "status": "healthy",
        "openai_configured": bool(OPENAI_API_KEY and not OPENAI_API_KEY.startswith("mock_") and OPENAI_API_KEY != "your_openai_api_key_here"),
        "github_configured": bool(GITHUB_TOKEN)
    }
