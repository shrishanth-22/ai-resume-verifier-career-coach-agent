from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import analyze, health

app = FastAPI(
    title="AI Resume Verifier + Career Coach Agent",
    description="Resume Intelligence Platform & Multi-Agent Recruitment System - Business Agent.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(health.router)
