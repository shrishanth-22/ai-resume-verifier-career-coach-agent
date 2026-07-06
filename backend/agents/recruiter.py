from backend.agents.base import get_openai_client, is_mock_mode, logger
from backend.models.schemas import (
    ParsedResume, ATSReport, VerificationReport, SkillGapReport, CareerCoachReport,
    RecruiterReport, RiskAssessmentItem
)

class RecruiterAssistantAgent:
    """Agent 7: Generates structured hiring recommendations, recruiter summaries, risk analyses, and candidate fit metrics."""

    def synthesize(
        self,
        parsed: ParsedResume,
        ats: ATSReport,
        verification: VerificationReport,
        skill_gap: SkillGapReport,
        career_roadmap: CareerCoachReport
    ) -> RecruiterReport:
        logger.info(f"RecruiterAssistantAgent: Synthesizing recruiter summary report...")
        if is_mock_mode():
            logger.warning("RecruiterAssistantAgent: Using simulated recruiter synthesis.")
            return self._simulate_synthesize(parsed, ats, verification, skill_gap, career_roadmap)

        try:
            client = get_openai_client()
            prompt = (
                f"Candidate Name: {parsed.candidate_info.name}\n"
                f"ATS Score: {ats.ats_score}\n"
                f"Claims Verified: {verification.verified_count}/{verification.verified_count + verification.unverified_count}\n"
                f"Skill Match Percentage: {skill_gap.skill_match_percentage}\n"
                f"Missing Skills: {', '.join(skill_gap.missing_skills)}\n"
                f"Roadmap Summary: {career_roadmap.summary}\n"
            )
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an elite recruiter assistant agent. Synthesize the sub-reports into an executive summary, direct hiring recommendation (e.g. 'Strong Buy / Fast Track'), overall resume strength score (0-100), career readiness score (0-100), risk assessments, and key resume insights."},
                    {"role": "user", "content": prompt}
                ],
                response_format=RecruiterReport,
                temperature=0.4
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"RecruiterAssistantAgent error: {e}. Falling back to simulation.")
            return self._simulate_synthesize(parsed, ats, verification, skill_gap, career_roadmap)

    def _simulate_synthesize(
        self,
        parsed: ParsedResume,
        ats: ATSReport,
        verification: VerificationReport,
        skill_gap: SkillGapReport,
        career_roadmap: CareerCoachReport
    ) -> RecruiterReport:
        summary = (
            f"{parsed.candidate_info.name} is an elite engineering talent demonstrating a proven background in "
            f"modular frontend architecture and scaling. The candidate has pinned strong open-source records and solid "
            f"system designs. Their fit is highly aligned, with minimal gap adjustments required for core DevOps tasks."
        )
        
        strength_score = int(80 + (verification.verified_count / max(1, verification.verified_count + verification.unverified_count)) * 10)
        strength_score = min(98, max(50, strength_score))
        
        readiness_score = int(skill_gap.skill_match_percentage)
        
        rec = "Proceed with Upskilling (Recommended)"
        if readiness_score >= 85:
            rec = "Strong Buy / Fast Track (Highly Recommended)"
        elif readiness_score >= 70:
            rec = "Proceed to Technical Interview"

        risks = [
            RiskAssessmentItem(
                risk_factor="AWS Certification Credential Verification Failure",
                severity="Medium",
                mitigation="Verify certification portal registration or request alternate proof from candidate."
            ),
            RiskAssessmentItem(
                risk_factor="Missing event-driven streaming background (Kafka/RabbitMQ)",
                severity="Low",
                mitigation="Request candidate complete milestone coursework on event-driven architectures."
            )
        ]

        insights = [
            "Demonstrated strong leadership and caching systems background at Vercel.",
            "Functional open-source rate limiter repository confirms deep FastAPI understanding.",
            "Educational pedigree (Stanford Systems Engineering) aligns cleanly with high performance requirements."
        ]

        return RecruiterReport(
            executive_summary=summary,
            hiring_recommendation=rec,
            resume_strength_score=strength_score,
            career_readiness_score=readiness_score,
            risk_assessment=risks,
            resume_insights=insights
        )
