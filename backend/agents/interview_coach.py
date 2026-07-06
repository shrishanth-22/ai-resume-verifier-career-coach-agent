from backend.agents.base import get_openai_client, is_mock_mode, logger
from backend.models.schemas import ParsedResume, SkillGapReport, InterviewCoachReport, InterviewQuestion

class InterviewCoachAgent:
    """Agent 6: Generates targeted mock interview questions tailored to the candidate's career gaps."""

    def generate_questions(self, parsed: ParsedResume, skill_gap: SkillGapReport, target_role: str) -> InterviewCoachReport:
        logger.info(f"InterviewCoachAgent: Generating practice questions for '{target_role}'...")
        if is_mock_mode():
            logger.warning("InterviewCoachAgent: Using simulated interview coach questions pool.")
            return self._simulate_questions(parsed, skill_gap, target_role)

        try:
            client = get_openai_client()
            prompt = (
                f"Candidate Name: {parsed.candidate_info.name}\n"
                f"Target Role: {target_role}\n"
                f"Skills Present: {', '.join(skill_gap.present_skills)}\n"
                f"Skills Gaps: {', '.join(skill_gap.missing_skills)}\n"
            )
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an elite interview coaching agent. Generate practice questions (System Design, Coding, and Behavioral) specific to the gaps. Provide hints and ideal answers for each question."},
                    {"role": "user", "content": prompt}
                ],
                response_format=InterviewCoachReport,
                temperature=0.7
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"InterviewCoachAgent error: {e}. Falling back to simulation.")
            return self._simulate_questions(parsed, skill_gap, target_role)

    def _simulate_questions(self, parsed: ParsedResume, skill_gap: SkillGapReport, target_role: str) -> InterviewCoachReport:
        questions = [
            InterviewQuestion(
                id="q1",
                question="How would you design a sliding window rate limiter middleware for a high-traffic microservices cluster (e.g. 100k requests/min)?",
                difficulty="Hard",
                category="System Design",
                hint="Think about Redis sorted sets (ZSET) timestamp logs and sliding window cleaning sweeps.",
                answer="Utilize a Redis sliding-window filter mechanism. Track requests as Unix timestamp scores inside a sorted set keyed by the client's identifier. Purge elements older than current timestamp minus interval window, then check card count."
            ),
            InterviewQuestion(
                id="q2",
                question="Explain the technical runtime differences between Server-Side Rendering (SSR) and Static Site Generation (SSG) in Next.js applications.",
                difficulty="Medium",
                category="Frontend Systems",
                hint="SSG resolves static files once on compilation; SSR formats static files dynamically on every incoming request.",
                answer="Static Site Generation (SSG) compiles HTML once during building, minimizing host calculations. Server-Side Rendering (SSR) executes compilation dynamically on each user request, which increases TTFB but allows dynamic data."
            ),
            InterviewQuestion(
                id="q3",
                question="Describe the sequence of actions Kubernetes performs when a pod health check reports an OOM-Killed event.",
                difficulty="Medium",
                category="Cloud Native",
                hint="Check liveness/readiness probes, container exit codes, and CGroups limits restrictions.",
                answer="Kubernetes detects liveness failure or exit code 137. It references the restartPolicy configured for the pod (e.g., Always) and uses back-off delays to spin up a new container instance under node memory limits."
            )
        ]
        return InterviewCoachReport(questions=questions)
