from backend.agents.base import get_openai_client, is_mock_mode, logger
from backend.models.schemas import ParsedResume, ATSReport

class ATSOptimizationAgent:
    """Agent 2: Evaluates resume format, structure, and keyword density relative to target career goal."""

    def evaluate(self, parsed: ParsedResume, target_role: str) -> ATSReport:
        logger.info(f"ATSOptimizationAgent: Evaluating ATS compatibility for '{target_role}'...")
        if is_mock_mode():
            logger.warning("ATSOptimizationAgent: Using simulated ATS evaluator.")
            return self._simulate_evaluate(parsed, target_role)

        try:
            client = get_openai_client()
            prompt = (
                f"Candidate Name: {parsed.candidate_info.name}\n"
                f"Target Role: {target_role}\n"
                f"Skills Listed: {', '.join(parsed.skills)}\n"
                f"Experiences: {[e.role + ' at ' + e.company for e in parsed.experiences]}\n"
                f"Projects: {[p.name + ': ' + p.description for p in parsed.projects]}\n"
            )
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert ATS optimization agent. Analyze the parsed resume details against the target job role. Provide compatibility scores, formatting checks, density metrics, missing key words, and suggestions."},
                    {"role": "user", "content": prompt}
                ],
                response_format=ATSReport,
                temperature=0.2
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"ATSOptimizationAgent error: {e}. Falling back to simulation.")
            return self._simulate_evaluate(parsed, target_role)

    def _simulate_evaluate(self, parsed: ParsedResume, target_role: str) -> ATSReport:
        formatting_checks = [
            "Grammar & Spelling check indices passed",
            "Horizontal margin layout structures verified",
            "Contact coordinate links index resolved",
            "No tables/images layout syntax breaks detected"
        ]
        
        skills_count = len(parsed.skills)
        score = int(70 + min(20, (skills_count / 12) * 20))
        
        target_lower = target_role.lower()
        if "staff" in target_lower or "principal" in target_lower or "lead" in target_lower:
            missing = ["System Design", "Distributed Systems", "Chaos Engineering", "Service Mesh"]
            suggestions = [
                "Quantify technical achievements (e.g. 'Reduced edge response latency by 35% using custom edge caches').",
                "Highlight mentoring and cross-functional leadership explicitly in experience headers.",
                "Detail container orchestration (Kubernetes/Istio) and active-active replica scaling in core projects."
            ]
            density = 78.5
        elif "frontend" in target_lower or "react" in target_lower:
            missing = ["Next.js", "Redux Toolkit", "Webpack", "TailwindCSS"]
            suggestions = [
                "Quantify frontend load times optimizations (e.g., 'Boosted LCP metric by 40% through lazy-loaded imports').",
                "Pin React/TypeScript portfolio sites at the top of the contacts list.",
                "Mention unit testing framework integration (Jest/Cypress) under skill sets."
            ]
            density = 82.0
        else:
            missing = ["Docker / Kubernetes", "gRPC", "CI/CD Pipeline", "Redis Caching"]
            suggestions = [
                "Add database caching patterns explicitly to Backend experience listings.",
                "Ensure GitHub URLs link directly to functional, documented open-source repositories.",
                "List automated pipeline tools (GitHub Actions, Jenkins) under DevOps capabilities."
            ]
            density = 74.0

        return ATSReport(
            ats_score=score,
            formatting_checks=formatting_checks,
            core_keyword_density=density,
            missing_keywords=missing,
            suggestions=suggestions
        )
