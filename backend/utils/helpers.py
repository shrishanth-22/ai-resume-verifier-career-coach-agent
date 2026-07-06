def get_demo_results() -> dict:
    """Returns a full mocked analysis response conforming to BusinessAgentResponse schema."""
    return {
        "parsed_resume": {
            "candidate_info": {
                "name": "Alex Rivera",
                "email": "alex.rivera@democandidatemail.io",
                "phone": "+1 (555) 321-7654",
                "github_username": "arivera-dev",
                "websites": ["https://alexrivera.dev", "https://linkedin.com/in/alex-rivera-demo"]
            },
            "skills": ["React", "TypeScript", "Node.js", "Python", "Docker", "Kubernetes", "AWS", "FastAPI", "GraphQL", "PostgreSQL"],
            "experiences": [
                {
                    "company": "Vercel",
                    "role": "Lead Engineer",
                    "start_date": "2022",
                    "end_date": "Present",
                    "description": "Architected modular edge rendering algorithms scaling deployment pipelines. Integrated global serverless caches."
                },
                {
                    "company": "Figma",
                    "role": "Senior Engineer",
                    "start_date": "2020",
                    "end_date": "2022",
                    "description": "Redesigned canvas collaborative multiplayer engines using Rust WebAssembly targets."
                }
            ],
            "projects": [
                {
                    "name": "FastAPI Rate Limiter",
                    "description": "Creator and maintainer of 'fastapi-rate-limiter' with star checking capability.",
                    "technologies": ["FastAPI", "Python", "Redis"],
                    "repository_url": "https://github.com/arivera-dev/fastapi-rate-limiter"
                },
                {
                    "name": "Canvas Engine",
                    "description": "A collaborative graphics rendering engine compiled to WebAssembly.",
                    "technologies": ["Rust", "WebAssembly", "WebGL"],
                    "repository_url": "https://github.com/arivera-dev/canvas-multiplayer"
                }
            ],
            "education": [
                {
                    "degree": "B.S. in Computer Science",
                    "major": "Systems Engineering",
                    "university": "Stanford University",
                    "graduation_year": "2019"
                }
            ]
        },
        "ats_report": {
            "ats_score": 87,
            "formatting_checks": [
                "Grammar & Spelling check indices passed",
                "Horizontal margin layout structures verified",
                "Contact coordinate links index resolved",
                "No tables/images layout syntax breaks detected"
            ],
            "core_keyword_density": 78.5,
            "missing_keywords": ["System Design", "Distributed Systems", "Chaos Engineering", "Service Mesh"],
            "suggestions": [
                "Quantify technical achievements (e.g. 'Reduced edge response latency by 35% using custom edge caches').",
                "Highlight mentoring and cross-functional leadership explicitly in experience headers.",
                "Detail container orchestration (Kubernetes/Istio) and active-active replica scaling in core projects."
            ]
        },
        "validation_report": {
            "claims": [
                {
                    "claim_type": "Work History",
                    "target": "Lead Engineer at Vercel (2022 - Present)",
                    "status": "Verified (Simulated match)",
                    "notes": "Validation checks on public employee registries and LinkedIn verification index resolved cleanly."
                },
                {
                    "claim_type": "GitHub Repository",
                    "target": "arivera-dev/fastapi-rate-limiter",
                    "status": "Verified (Live API resolved)",
                    "notes": "GitHub API confirmed repository exists under arivera-dev/fastapi-rate-limiter with 1,240 stars and active commits."
                },
                {
                    "claim_type": "Project Claim Verification",
                    "target": "Canvas Engine",
                    "status": "Simulated Verification",
                    "notes": "Project description details aligned with target technologies: Rust, WebAssembly, WebGL."
                },
                {
                    "claim_type": "AWS Cloud Certification",
                    "target": "AWS Certified Solutions Architect - Professional",
                    "status": "Unverified (Registry mismatch)",
                    "notes": "AWS certification verification portal check failed to resolve Alex Rivera credential ID AR-99824."
                }
            ],
            "verified_count": 3,
            "unverified_count": 1,
            "verification_timeline": [
                {"event": "Security Clearance & Verification Hook Initialized", "date": "Today 10:00 AM", "status": "Verified"},
                {"event": "Contact Coordinates Registry Match Check", "date": "Today 10:01 AM", "status": "Verified"},
                {"event": "GitHub Repository Audit: arivera-dev/fastapi-rate-limiter", "date": "Today 10:02 AM", "status": "Verified"},
                {"event": "Heuristic Project Scan: Canvas Engine", "date": "Today 10:03 AM", "status": "Verified"},
                {"event": "AWS Certification Lookup: AR-99824", "date": "Today 10:06 AM", "status": "Warning"}
            ]
        },
        "skill_gap_report": {
            "present_skills": ["React", "TypeScript", "Node.js", "Python", "Docker", "Kubernetes", "AWS", "FastAPI", "GraphQL", "PostgreSQL"],
            "missing_skills": ["System Design", "Distributed Systems", "Chaos Engineering", "Service Mesh"],
            "skill_match_percentage": 72,
            "skill_gap_matrix": [
                {"skill": "System Design", "priority": 90, "gap_reason": "Critical for architecting scalable, active-active services and caching models."},
                {"skill": "Distributed Systems", "priority": 85, "gap_reason": "Essential for understanding replica synchronization and consensus models."},
                {"skill": "Chaos Engineering", "priority": 70, "gap_reason": "Highly recommended for establishing resiliency and fault injection standards."},
                {"skill": "Service Mesh", "priority": 60, "gap_reason": "Needed for routing service traffic securely inside container pods."}
            ]
        },
        "career_roadmap": {
            "summary": "Alex Rivera shows excellent capabilities in core full-stack technologies. To step into the target Senior Staff Engineer role, focus must shift to distributed systems architectures, container network mesh scaling, and high-throughput message brokerage interfaces.",
            "learning_progress": [
                {"milestone": "Advanced System Design", "percentage": 45},
                {"milestone": "Cloud Native Scalability", "percentage": 60},
                {"milestone": "Tech Leadership & Alignment", "percentage": 30}
            ],
            "milestones": [
                {
                    "name": "Advanced System Design & Distributed Networks",
                    "timeline": "Weeks 1 - 4",
                    "items": [
                        "Study event-driven messaging structures (Apache Kafka partitions, subscriber consumer groups).",
                        "Design high-concurrency caching frameworks utilizing Redis clusters and active-active replicas."
                    ],
                    "resources": [
                        "Designing Data-Intensive Applications by Martin Kleppmann",
                        "Alex Xu's System Design Interview Guides"
                    ]
                },
                {
                    "name": "Cloud Native Deployments & Orchestration",
                    "timeline": "Weeks 5 - 8",
                    "items": [
                        "Set up locally hosted Kubernetes clusters and mount service mesh traffic layers (Istio).",
                        "Implement fault tolerance checks using chaos testing mesh algorithms (Chaos Mesh)."
                    ],
                    "resources": [
                        "Kubernetes Official Documentation & Tutorial Guides",
                        "CNCF Cloud Native Trail Map Handbook"
                    ]
                },
                {
                    "name": "Executive Technical Leadership & RFCs",
                    "timeline": "Weeks 9 - 12",
                    "items": [
                        "Write executive-level RFC technical specification papers mapping serverless caching pipelines.",
                        "Practice code optimization cost estimates matching business operational metrics."
                    ],
                    "resources": [
                        "Will Larson's StaffEng.com engineering resources",
                        "The Staff Engineer's Path by Tanya Reilly"
                    ]
                }
            ],
            "general_resume_tips": [
                "Quantify technical performance impact metrics (e.g. 'boosted cache hit ratio by 28%').",
                "Structure experience highlights with the STAR format matching high-level business goals.",
                "Resolve AWS credential registry discrepancies before submitting profiles."
            ]
        },
        "interview_coach_report": {
            "questions": [
                {
                    "id": "q1",
                    "question": "How would you design a sliding window rate limiter middleware for a high-traffic microservices cluster (e.g. 100k requests/min)?",
                    "difficulty": "Hard",
                    "category": "System Design",
                    "hint": "Think about Redis sorted sets (ZSET) timestamp logs and sliding window cleaning sweeps.",
                    "answer": "Utilize a Redis sliding-window filter mechanism. Track requests as Unix timestamp scores inside a sorted set keyed by the client's identifier. Purge elements older than current timestamp minus interval window, then check card count."
                },
                {
                    "id": "q2",
                    "question": "Explain the technical runtime differences between Server-Side Rendering (SSR) and Static Site Generation (SSG) in Next.js applications.",
                    "difficulty": "Medium",
                    "category": "Frontend Systems",
                    "hint": "SSG resolves static files once on compilation; SSR formats static files dynamically on every incoming request.",
                    "answer": "Static Site Generation (SSG) compiles HTML once during building, minimizing host calculations. Server-Side Rendering (SSR) executes compilation dynamically on each user request, which increases TTFB but allows dynamic data."
                },
                {
                    "id": "q3",
                    "question": "Describe the sequence of actions Kubernetes performs when a pod health check reports an OOM-Killed event.",
                    "difficulty": "Medium",
                    "category": "Cloud Native",
                    "hint": "Check liveness/readiness probes, container exit codes, and CGroups limits restrictions.",
                    "answer": "Kubernetes detects liveness failure or exit code 137. It references the restartPolicy configured for the pod (e.g., Always) and uses back-off delays to spin up a new container instance under node memory limits."
                }
            ]
        },
        "recruiter_report": {
            "executive_summary": "Alex Rivera is an elite engineering talent demonstrating a proven background in modular frontend architecture and scaling. The candidate has pinned strong open-source records and solid system designs. Their fit is highly aligned, with minimal gap adjustments required for core DevOps tasks.",
            "hiring_recommendation": "Strong Buy / Fast Track (Highly Recommended)",
            "resume_strength_score": 92,
            "career_readiness_score": 75,
            "risk_assessment": [
                {
                    "risk_factor": "AWS Certification Credential Verification Failure",
                    "severity": "Medium",
                    "mitigation": "Verify certification portal registration or request alternate proof from candidate."
                },
                {
                    "risk_factor": "Missing event-driven streaming background (Kafka/RabbitMQ)",
                    "severity": "Low",
                    "mitigation": "Request candidate complete milestone coursework on event-driven architectures."
                }
            ],
            "resume_insights": [
                "Demonstrated strong leadership and caching systems background at Vercel.",
                "Functional open-source rate limiter repository confirms deep FastAPI understanding.",
                "Educational pedigree (Stanford Systems Engineering) aligns cleanly with high performance requirements."
            ]
        }
    }
