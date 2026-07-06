import re
import base64
from backend.agents.base import get_openai_client, is_mock_mode, logger
from backend.models.schemas import ParsedResume, CandidateInfo, Experience, Project, Education

class ResumeParserAgent:
    """Agent 1: Extracts clean structured metadata from unstructured resume text or images."""

    def parse(self, text: str) -> ParsedResume:
        logger.info("ResumeParserAgent: Starting resume text parsing...")
        if is_mock_mode():
            logger.warning("ResumeParserAgent: Using simulated resume parser (mock mode).")
            return self._simulate_parse(text)
            
        try:
            client = get_openai_client()
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert resume parsing agent. Extract all relevant details from the resume text into the requested structured JSON schema."},
                    {"role": "user", "content": f"Resume Text:\n\n{text}"}
                ],
                response_format=ParsedResume,
                temperature=0.0
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"ResumeParserAgent error: {e}. Falling back to simulation.")
            return self._simulate_parse(text)

    def parse_image(self, image_bytes: bytes, mime_type: str) -> ParsedResume:
        logger.info("ResumeParserAgent: Starting resume image parsing...")
        if is_mock_mode():
            logger.warning("ResumeParserAgent: Using simulated resume parser (mock mode).")
            return self._simulate_parse("Image Resume Upload")
            
        try:
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            client = get_openai_client()
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert resume parsing agent. Extract all relevant details from the resume image into the requested structured JSON schema."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please parse this resume image."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format=ParsedResume,
                temperature=0.0
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"ResumeParserAgent image error: {e}. Falling back to simulation.")
            return self._simulate_parse("Image Resume Upload")

    def _simulate_parse(self, text: str) -> ParsedResume:
        if text == "Image Resume Upload":
            text = """
            Alex Rivera
            Lead Engineer
            Email: alex.rivera@democandidatemail.io
            Phone: +1 (555) 321-7654
            GitHub: https://github.com/arivera-dev
            Websites: https://alexrivera.dev, https://linkedin.com/in/alex-rivera-demo

            Skills:
            React, TypeScript, Node.js, Python, Docker, Kubernetes, AWS, FastAPI, GraphQL, PostgreSQL

            Experience:
            Vercel (Lead Engineer, 2022 - Present)
            Architected modular edge rendering algorithms scaling deployment pipelines. Integrated global serverless caches.
            Figma (Senior Engineer, 2020 - 2022)
            Redesigned canvas collaborative multiplayer engines using Rust WebAssembly targets.

            Education:
            B.S. in Computer Science (Systems Engineering, Stanford University, 2019)
            """
        
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        name = "Alex Rivera"
        if lines:
            name = lines[0]
            if len(name) > 50 or "@" in name:
                name = "Engineering Applicant"

        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0) if email_match else "alex.rivera@democandidatemail.io"
        
        phone_match = re.search(r'\+?\d[\d\-\(\)\s]{8,15}\d', text)
        phone = phone_match.group(0) if phone_match else "+1 (555) 321-7654"

        github_match = re.search(r'github\.com/([\w\.-]+)', text, re.IGNORECASE)
        github_username = github_match.group(1) if github_match else "arivera-dev"

        websites = list(set(re.findall(r'(https?://[^\s\)]+)', text)))
        if not websites:
            websites = ["https://alexrivera.dev", "https://linkedin.com/in/alex-rivera-demo"]

        common_skills = ["react", "typescript", "node.js", "python", "docker", "kubernetes", "aws", "fastapi", "graphql", "postgresql", "rust", "webassembly"]
        skills_found = [s.capitalize() for s in common_skills if s in text.lower()]
        if not skills_found:
            skills_found = ["React", "TypeScript", "Node.js", "Python", "Docker", "Kubernetes", "AWS", "FastAPI", "GraphQL", "PostgreSQL"]

        formatted_skills = []
        for s in skills_found:
            if s.lower() == "react":
                formatted_skills.append("React")
            elif s.lower() == "typescript":
                formatted_skills.append("TypeScript")
            elif s.lower() == "node.js":
                formatted_skills.append("Node.js")
            elif s.lower() == "fastapi":
                formatted_skills.append("FastAPI")
            elif s.lower() == "webassembly":
                formatted_skills.append("WebAssembly")
            elif s.lower() == "graphql":
                formatted_skills.append("GraphQL")
            elif s.lower() == "postgresql":
                formatted_skills.append("PostgreSQL")
            elif s.lower() == "aws":
                formatted_skills.append("AWS")
            else:
                formatted_skills.append(s)

        return ParsedResume(
            candidate_info=CandidateInfo(
                name=name,
                email=email,
                phone=phone,
                github_username=github_username,
                websites=websites
            ),
            experiences=[
                Experience(
                    company="Vercel",
                    role="Lead Engineer",
                    start_date="2022",
                    end_date="Present",
                    description="Architected modular edge rendering algorithms scaling deployment pipelines. Integrated global serverless caches."
                ),
                Experience(
                    company="Figma",
                    role="Senior Engineer",
                    start_date="2020",
                    end_date="2022",
                    description="Redesigned canvas collaborative multiplayer engines using Rust WebAssembly targets."
                )
            ],
            projects=[
                Project(
                    name="FastAPI Rate Limiter",
                    description="Creator and maintainer of 'fastapi-rate-limiter' with star checking capability.",
                    technologies=["FastAPI", "Python", "Redis"],
                    repository_url=f"https://github.com/{github_username}/fastapi-rate-limiter"
                ),
                Project(
                    name="Canvas Engine",
                    description="A collaborative graphics rendering engine compiled to WebAssembly.",
                    technologies=["Rust", "WebAssembly", "WebGL"],
                    repository_url=f"https://github.com/{github_username}/canvas-multiplayer"
                )
            ],
            education=[
                Education(
                    degree="B.S. in Computer Science",
                    major="Systems Engineering",
                    university="Stanford University",
                    graduation_year="2019"
                )
            ],
            skills=formatted_skills
        )
