from typing import List, Optional
from pydantic import BaseModel, Field

class CandidateInfo(BaseModel):
    name: str = Field(description="The full name of the candidate")
    email: Optional[str] = Field(None, description="The email address of the candidate")
    phone: Optional[str] = Field(None, description="The contact phone number of the candidate")
    github_username: Optional[str] = Field(None, description="The GitHub username of the candidate, if available")
    websites: List[str] = Field(default_factory=list, description="Other links/portfolio websites found")

class Experience(BaseModel):
    company: str = Field(description="Name of the company/organization")
    role: str = Field(description="Job title/role")
    start_date: Optional[str] = Field(None, description="Start date of employment")
    end_date: Optional[str] = Field(None, description="End date of employment")
    description: str = Field(description="Key responsibilities and engineering achievements")

class Project(BaseModel):
    name: str = Field(description="Name of the project")
    description: str = Field(description="Brief summary of the project's purpose and functionality")
    technologies: List[str] = Field(default_factory=list, description="List of technologies used in the project")
    repository_url: Optional[str] = Field(None, description="GitHub repository URL or website link")

class Education(BaseModel):
    degree: str = Field(description="Degree obtained (e.g. BS, MS)")
    major: str = Field(description="Major or field of study")
    university: str = Field(description="Name of the institution")
    graduation_year: Optional[str] = Field(None, description="Year of graduation")

class ParsedResume(BaseModel):
    candidate_info: CandidateInfo
    experiences: List[Experience]
    projects: List[Project]
    education: List[Education]
    skills: List[str] = Field(default_factory=list, description="List of technical and soft skills")

class ATSReport(BaseModel):
    ats_score: int = Field(description="ATS compatibility score (0-100)")
    formatting_checks: List[str] = Field(description="Checklist of format verifications (e.g. 'Margins OK')")
    core_keyword_density: float = Field(description="Density percentage of target keywords")
    missing_keywords: List[str] = Field(description="List of target keywords missing from the resume")
    suggestions: List[str] = Field(description="Actionable formatting and optimization recommendations")

class VerificationTimelineEvent(BaseModel):
    event: str = Field(description="The verification event name (e.g. 'GitHub Registry Check')")
    date: str = Field(description="Date or timestamp of the check")
    status: str = Field(description="Outcome status (e.g. 'Verified', 'Warning')")

class VerificationClaim(BaseModel):
    claim_type: str = Field(description="Type of claim (e.g. 'Work History', 'Repository')")
    target: str = Field(description="Specific target of the claim")
    status: str = Field(description="Status of verification (e.g. 'Verified', 'Unverified', 'Simulated')")
    notes: str = Field(description="Detailed verification feedback or simulated audit log")

class VerificationReport(BaseModel):
    claims: List[VerificationClaim] = Field(default_factory=list)
    verified_count: int = 0
    unverified_count: int = 0
    verification_timeline: List[VerificationTimelineEvent] = Field(default_factory=list)

class SkillGapItem(BaseModel):
    skill: str = Field(description="Name of the skill")
    priority: int = Field(description="Priority index (1-100) indicating critical importance for the role")
    gap_reason: str = Field(description="Brief reason explaining the requirement context")

class SkillGapReport(BaseModel):
    present_skills: List[str] = Field(description="List of matching skills present in the resume")
    missing_skills: List[str] = Field(description="List of matching skills missing from the resume")
    skill_match_percentage: int = Field(description="Skill alignment percentage (0-100)")
    skill_gap_matrix: List[SkillGapItem] = Field(default_factory=list, description="Detailed skill-by-skill priority gaps")

class RoadmapMilestone(BaseModel):
    name: str = Field(description="Title of the milestone")
    timeline: str = Field(description="Suggested timeframe (e.g. 'Weeks 1-2')")
    items: List[str] = Field(description="Actionable tasks to complete")
    resources: List[str] = Field(description="Curated learning links, documentation, or books")

class LearningProgressItem(BaseModel):
    milestone: str = Field(description="Milestone or topic name")
    percentage: int = Field(description="Candidate's current learning progress percentage (0-100)")

class CareerCoachReport(BaseModel):
    summary: str = Field(description="Career coach executive summary of the gap analysis")
    learning_progress: List[LearningProgressItem] = Field(default_factory=list)
    milestones: List[RoadmapMilestone] = Field(description="Chronological learning steps")
    general_resume_tips: List[str] = Field(description="Practical tips to improve the resume for this role")

class InterviewQuestion(BaseModel):
    id: str = Field(description="Unique question identifier (e.g. 'q1')")
    question: str = Field(description="Practice question text")
    difficulty: str = Field(description="Difficulty level (e.g. 'Medium', 'Hard')")
    category: str = Field(description="Category (e.g. 'System Design', 'Behavioral')")
    hint: str = Field(description="Helpful hint for preparing response")
    answer: str = Field(description="Ideal answer guidelines or reference solution")

class InterviewCoachReport(BaseModel):
    questions: List[InterviewQuestion] = Field(default_factory=list)

class RiskAssessmentItem(BaseModel):
    risk_factor: str = Field(description="Description of identified risk or credential gap")
    severity: str = Field(description="Risk severity level: 'Low', 'Medium', or 'High'")
    mitigation: str = Field(description="Mitigation recommendation for recruiter or candidate")

class RecruiterReport(BaseModel):
    executive_summary: str = Field(description="Recruiter summary profile highlight of candidate suitability")
    hiring_recommendation: str = Field(description="Overall recommendation (e.g. 'Strong Buy / Fast Track', 'Proceed with Upskilling')")
    resume_strength_score: int = Field(description="Calculated overall resume structure strength (0-100)")
    career_readiness_score: int = Field(description="Calculated readiness index for target role (0-100)")
    risk_assessment: List[RiskAssessmentItem] = Field(default_factory=list)
    resume_insights: List[str] = Field(default_factory=list, description="Key resume observations and differentiators")

class BusinessAgentResponse(BaseModel):
    parsed_resume: ParsedResume
    ats_report: ATSReport
    validation_report: VerificationReport
    skill_gap_report: SkillGapReport
    career_roadmap: CareerCoachReport
    interview_coach_report: InterviewCoachReport
    recruiter_report: RecruiterReport
