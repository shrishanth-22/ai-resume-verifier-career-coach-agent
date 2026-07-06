from backend.agents.base import get_openai_client, is_mock_mode, logger
from backend.models.schemas import ParsedResume, SkillGapReport, CareerCoachReport, RoadmapMilestone, LearningProgressItem

class CareerCoachAgent:
    """Agent 5: Synthesizes career coach roadmap milestones and maps learning resource paths."""

    def coach(self, parsed: ParsedResume, skill_gap: SkillGapReport, target_role: str) -> CareerCoachReport:
        logger.info(f"CareerCoachAgent: Formulating career coach advice for target role '{target_role}'...")
        if is_mock_mode():
            logger.warning("CareerCoachAgent: Using simulated career coach advisor.")
            return self._simulate_coach(parsed, skill_gap, target_role)

        try:
            client = get_openai_client()
            prompt = (
                f"Candidate Name: {parsed.candidate_info.name}\n"
                f"Target Role: {target_role}\n"
                f"Skills Present: {', '.join(skill_gap.present_skills)}\n"
                f"Skills Missing: {', '.join(skill_gap.missing_skills)}\n"
            )
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an elite career coach. Provide an executive summary of target career goals, learning progress bars (0-100), chronological milestones with timeline dates and curated resources, and resume tips."},
                    {"role": "user", "content": prompt}
                ],
                response_format=CareerCoachReport,
                temperature=0.7
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"CareerCoachAgent error: {e}. Falling back to simulation.")
            return self._simulate_coach(parsed, skill_gap, target_role)

    def _simulate_coach(self, parsed: ParsedResume, skill_gap: SkillGapReport, target_role: str) -> CareerCoachReport:
        summary = (
            f"Candidate Alex Rivera shows excellent capabilities in core full-stack technologies. To step into the "
            f"target '{target_role}' role, focus must shift to distributed systems architectures, container network mesh scaling, "
            f"and high-throughput message brokerage interfaces."
        )

        progress = [
            LearningProgressItem(milestone="Advanced System Design", percentage=45),
            LearningProgressItem(milestone="Cloud Native Scalability", percentage=60),
            LearningProgressItem(milestone="Tech Leadership & Alignment", percentage=30)
        ]

        milestones = [
            RoadmapMilestone(
                name="Advanced System Design & Distributed Networks",
                timeline="Weeks 1 - 4",
                items=[
                    "Study event-driven messaging structures (Apache Kafka partitions, subscriber consumer groups).",
                    "Design high-concurrency caching frameworks utilizing Redis clusters and active-active replicas."
                ],
                resources=[
                    "Designing Data-Intensive Applications by Martin Kleppmann",
                    "Alex Xu's System Design Interview Guides"
                ]
            ),
            RoadmapMilestone(
                name="Cloud Native Deployments & Orchestration",
                timeline="Weeks 5 - 8",
                items=[
                    "Set up locally hosted Kubernetes clusters and mount service mesh traffic layers (Istio).",
                    "Implement fault tolerance checks using chaos testing mesh algorithms (Chaos Mesh)."
                ],
                resources=[
                    "Kubernetes Official Documentation & Tutorial Guides",
                    "CNCF Cloud Native Trail Map Handbook"
                ]
            ),
            RoadmapMilestone(
                name="Executive Technical Leadership & RFCs",
                timeline="Weeks 9 - 12",
                items=[
                    "Write executive-level RFC technical specification papers mapping serverless caching pipelines.",
                    "Practice code optimization cost estimates matching business operational metrics."
                ],
                resources=[
                    "Will Larson's StaffEng.com engineering resources",
                    "The Staff Engineer's Path by Tanya Reilly"
                ]
            )
        ]

        tips = [
            "Quantify technical performance impact metrics (e.g. 'boosted cache hit ratio by 28%').",
            "Structure experience highlights with the STAR format matching high-level business goals.",
            "Resolve unverifiedAWS registry credentials mismatch before submitting candidate profiles."
        ]

        return CareerCoachReport(
            summary=summary,
            learning_progress=progress,
            milestones=milestones,
            general_resume_tips=tips
        )
