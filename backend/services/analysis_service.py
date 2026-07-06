import io
from fastapi import HTTPException, status
import pypdf
from backend.agents.base import logger
from backend.agents.parser import ResumeParserAgent
from backend.agents.ats import ATSOptimizationAgent
from backend.agents.verifier import ResumeVerificationAgent
from backend.agents.skill_gap import SkillGapAgent
from backend.agents.career_coach import CareerCoachAgent
from backend.agents.interview_coach import InterviewCoachAgent
from backend.agents.recruiter import RecruiterAssistantAgent
from backend.models.schemas import BusinessAgentResponse

class MultiAgentAnalysisService:
    """Orchestrator that coordinates the end-to-end Multi-Agent Recruitment System pipeline."""

    def __init__(self):
        self.parser_agent = ResumeParserAgent()
        self.ats_agent = ATSOptimizationAgent()
        self.verification_agent = ResumeVerificationAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.career_coach_agent = CareerCoachAgent()
        self.interview_coach_agent = InterviewCoachAgent()
        self.recruiter_agent = RecruiterAssistantAgent()

    async def analyze_resume(self, file_bytes: bytes, file_name: str, target_role: str) -> BusinessAgentResponse:
        logger.info(f"AnalysisService: Initiating multi-agent analysis for {file_name}...")
        
        if file_name.lower().endswith(".pdf") or file_bytes.startswith(b"%PDF"):
            logger.info("AnalysisService: Running ResumeParserAgent (PDF parsing)...")
            resume_text = self._extract_text_from_pdf(file_bytes)
            parsed_resume = self.parser_agent.parse(resume_text)
        elif file_name.lower().endswith(".png") or file_bytes.startswith(b"\x89PNG"):
            logger.info("AnalysisService: Running ResumeParserAgent (PNG OCR parsing)...")
            parsed_resume = self.parser_agent.parse_image(file_bytes, "image/png")
        elif file_name.lower().endswith((".jpg", ".jpeg")) or file_bytes.startswith(b"\xff\xd8\xff"):
            logger.info("AnalysisService: Running ResumeParserAgent (JPEG OCR parsing)...")
            parsed_resume = self.parser_agent.parse_image(file_bytes, "image/jpeg")
        else:
            logger.warning("AnalysisService: Unsupported header or extension. Falling back to PDF text extraction.")
            try:
                resume_text = self._extract_text_from_pdf(file_bytes)
                parsed_resume = self.parser_agent.parse(resume_text)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Strict Input Policy: Unsupported or corrupted file format."
                )

        logger.info("AnalysisService: Running ATSOptimizationAgent...")
        ats_report = self.ats_agent.evaluate(parsed_resume, target_role)

        logger.info("AnalysisService: Running ResumeVerificationAgent...")
        validation_report = await self.verification_agent.validate(parsed_resume)

        logger.info("AnalysisService: Running SkillGapAgent...")
        skill_gap_report = self.skill_gap_agent.analyze(parsed_resume, target_role)

        logger.info("AnalysisService: Running CareerCoachAgent...")
        career_roadmap = self.career_coach_agent.coach(parsed_resume, skill_gap_report, target_role)

        logger.info("AnalysisService: Running InterviewCoachAgent...")
        interview_coach_report = self.interview_coach_agent.generate_questions(parsed_resume, skill_gap_report, target_role)

        logger.info("AnalysisService: Running RecruiterAssistantAgent...")
        recruiter_report = self.recruiter_agent.synthesize(
            parsed_resume, ats_report, validation_report, skill_gap_report, career_roadmap
        )

        logger.info("AnalysisService: End-to-end multi-agent pipeline completed.")
        return BusinessAgentResponse(
            parsed_resume=parsed_resume,
            ats_report=ats_report,
            validation_report=validation_report,
            skill_gap_report=skill_gap_report,
            career_roadmap=career_roadmap,
            interview_coach_report=interview_coach_report,
            recruiter_report=recruiter_report
        )

    def _extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        try:
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            return text
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to parse PDF binary file stream: {e}"
            )
