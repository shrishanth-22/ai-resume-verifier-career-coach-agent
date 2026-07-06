from backend.agents.base import get_openai_client, is_mock_mode, logger
from backend.models.schemas import ParsedResume, SkillGapReport, SkillGapItem

class SkillGapAgent:
    """Agent 4: Performs deep skill gap mapping against the target career goals."""

    def analyze(self, parsed: ParsedResume, target_role: str) -> SkillGapReport:
        logger.info(f"SkillGapAgent: Analyzing skill gaps for target role '{target_role}'...")
        if is_mock_mode():
            logger.warning("SkillGapAgent: Using simulated skill gap analyzer.")
            return self._simulate_analyze(parsed, target_role)

        try:
            client = get_openai_client()
            prompt = (
                f"Candidate Name: {parsed.candidate_info.name}\n"
                f"Target Role: {target_role}\n"
                f"Skills Listed: {', '.join(parsed.skills)}\n"
                f"Experiences: {[e.role + ' at ' + e.company for e in parsed.experiences]}\n"
            )
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert skill gap analyzer. Match the candidate skills with the requirements of the target role. Highlight match percentage, present skills, missing skills, and priority indices (1-100) for missing skills."},
                    {"role": "user", "content": prompt}
                ],
                response_format=SkillGapReport,
                temperature=0.2
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"SkillGapAgent error: {e}. Falling back to simulation.")
            return self._simulate_analyze(parsed, target_role)

    def _simulate_analyze(self, parsed: ParsedResume, target_role: str) -> SkillGapReport:
        present_skills = parsed.skills
        
        target_role_lower = target_role.lower()
        if "frontend" in target_role_lower or "react" in target_role_lower:
            all_possible_skills = ["React", "TypeScript", "Redux", "Webpack", "Next.js", "Jest", "CSS Grid", "TailwindCSS", "REST APIs", "Node.js", "Docker", "CI/CD Pipeline"]
        else:
            all_possible_skills = ["Python", "FastAPI", "Docker", "Kubernetes", "AWS", "gRPC", "System Design", "Kafka", "SQL", "CI/CD Pipeline", "Redis", "NoSQL"]

        present_set = set([s.lower() for s in present_skills])
        missing_skills = [s for s in all_possible_skills if s.lower() not in present_set]
        
        matched_count = len(all_possible_skills) - len(missing_skills)
        pct = int((matched_count / len(all_possible_skills)) * 100)
        pct = min(95, max(45, pct))
        
        matrix = []
        priorities = [90, 80, 75, 60]
        reasons = {
            "System Design": "Critical for architecting scalable, active-active services and caching models.",
            "Kubernetes": "Standard deployment platform for high-scale microservices orchestration.",
            "gRPC": "Essential for high-throughput, low-latency inter-service communication.",
            "Kafka": "Needed for event-driven asynchronous microservice messaging topologies.",
            "Next.js": "Primary modern framework for performance-optimized frontends.",
            "Redux Toolkit": "Core standard for managing shared state grids cleanly.",
            "Webpack": "Required for bundling configurations and page speed optimization.",
            "TailwindCSS": "Industry standard for modular, rapid visual style compilation."
        }
        
        for idx, skill in enumerate(missing_skills[:4]):
            priority = priorities[idx] if idx < len(priorities) else 50
            reason = reasons.get(skill, f"Highly recommended skill required to operate as an elite engineer in the target domain.")
            matrix.append(SkillGapItem(
                skill=skill,
                priority=priority,
                gap_reason=reason
            ))

        return SkillGapReport(
            present_skills=present_skills,
            missing_skills=missing_skills[:5],
            skill_match_percentage=pct,
            skill_gap_matrix=matrix
        )
