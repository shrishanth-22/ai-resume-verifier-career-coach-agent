from fastapi import APIRouter, File, Form, UploadFile, HTTPException, status
from backend.models.schemas import BusinessAgentResponse
from backend.services.analysis_service import MultiAgentAnalysisService
from backend.agents.base import logger

router = APIRouter(prefix="/api/v1", tags=["Analysis"])
analysis_service = MultiAgentAnalysisService()

@router.post("/analyze", response_model=BusinessAgentResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    target_role: str = Form("Senior Staff Engineer")
):
    """
    Ephemerally parses an uploaded PDF or image resume, runs the multi-agent
    audits, and outputs recruitment scoring, skill gaps, coaching roadmaps, and risk analyses.
    """
    logger.info(f"Router: Received upload request for {file.filename} targeting role: {target_role}")

    allowed_extensions = (".pdf", ".png", ".jpg", ".jpeg")
    if not file.filename.lower().endswith(allowed_extensions):
        logger.warning(f"Router: Rejected file format {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Strict Input Policy: Only files with .pdf, .png, .jpg, or .jpeg extensions are accepted."
        )

    max_bytes = 5 * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        logger.warning(f"Router: Rejected file size {len(content)} bytes")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Strict Input Policy: File size exceeds the maximum allowed limit of 5MB."
        )

    response = await analysis_service.analyze_resume(content, file.filename, target_role)
    return response
