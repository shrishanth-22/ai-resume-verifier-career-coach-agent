# AI Resume Verifier + Career Coach Agent 💼

A secure, enterprise-grade **Resume Intelligence Platform** and **Multi-Agent Recruitment System** built as a production-ready Business Agent for the Kaggle AI Agents Capstone. 

This platform parses resumes, validates engineering claims using live API checks, scores candidate capabilities against target job roles, and synthesizes recruiter assessments (including strength scores, readiness metrics, and risk items) along with an interactive practice arena.

---

## 1. Project Overview & Business Problem
Technical recruiting is plagued by:
- **Exaggerated Claims:** Reviewing and auditing engineering portfolios (e.g. verifying GitHub stars, commit histories, and deployment hashes) is manual and time-consuming.
- **Privacy Compliance Risks:** Retaining candidate PII permanently creates liability under GDPR, CCPA, and similar data residency laws.
- **Ambiguous Alignment:** Standard resumes do not highlight semantic skill gaps, upskilling milestones, or detailed recruiter recommendations.

## 2. The Solution: Resume Intelligence Platform
This platform addresses these gaps via a decoupled, multi-agent pipeline:
- **Zero-Retention Ephemeral Storage:** Reads files strictly in volatile memory. Upload byte streams are immediately parsed and discarded.
- **Multi-Agent Recruitment System:** Orchestrates seven specialized agents that exchange structured JSON schemas to construct a candidate scorecard.
- **Claim Verification Registry:** Dynamically checks GitHub repositories and claims via live API checks and checks.
- **Executive Recruiter Scorecards:** Reports Strength Scores, Career Readiness percentages, and mitigable risk logs instantly.

---

## 3. Multi-Agent System Architecture

Below is the orchestration and data flow between the independent agents:

```
                  [ User Upload File ] ---> (app.py Streamlit UI) 
                                                  |
                                           (UploadFile Stream)
                                                  v
                                         [ Root main.py Entry ]
                                                  |
                                                  v
                                        (backend.main FastAPI)
                                                  |
                                                  v
                                     [ MultiAgentAnalysisService ]
                                                  |
  +-----------------------+-----------------------+-----------------------+-----------------------+
  |                       |                       |                       |                       |
  v                       v                       v                       v                       v
(Resume Parser)    (ATS Optimizer)      (Verification Agent)       (Skill Gap Agent)       (Career Coach)
  * Extracts text    * Scores keyword     * Verifies GitHub API    * Maps present &        * Formulates
  * Outputs JSON       density & format     & registry claims        missing priority gaps   milestones & tips
  +-----------------------+-----------------------+-----------------------+-----------------------+
                                                  |
                                                  +-----------------------+-----------------------+
                                                                          |                       |
                                                                          v                       v
                                                                  (Interview Coach)      (Recruiter Assistant)
                                                                  * Generates targeted   * Synthesizes fit scores,
                                                                    Q&A practice deck      risk metrics & summaries
                                                                          |                       |
                                                                          +-----------+-----------+
                                                                                      |
                                                                                      v
                                                                       [ Unified BusinessAgentResponse ]
                                                                                      |
                                                                                      v
                                                                             (Interactive UI Grid)
```

---

## 4. Technology Stack
- **Frontend Dashboard:** Streamlit, CSS Grid, Custom SVG (Radar Charts), HTML/CSS Timelines
- **Backend API Engine:** FastAPI, Uvicorn, Python-Multipart
- **AI Core:** OpenAI GPT-4o-mini API (utilizing strict JSON schema output formats)
- **PDF Extraction:** PyPDF
- **Networking & Verification:** HTTPX (asynchronous client verification hooks)
- **Orchestration:** Pydantic (data exchange validation)

---

## 5. Structured API Overview

### `POST /api/v1/analyze`
Accepts a resume document, executes the multi-agent pipeline, and returns the unified scorecard.

- **Content-Type:** `multipart/form-data`
- **Request Body:**
  - `file`: PDF or image file (PNG/JPG/JPEG, max 5MB)
  - `target_role`: String target job title (default: `Senior Staff Engineer`)
- **Response Format:** `BusinessAgentResponse` (JSON conforming to schema)

### `GET /health`
Verifies if configuration credentials (OpenAI API Key, GitHub Token) are correctly initialized.

---

## 6. Installation & Local Setup

### Prerequisites
- Python 3.11+
- OpenAI API Key
- (Optional) GitHub PAT (Personal Access Token) to prevent API rate limits

### Manual Installation
1. **Clone the repository and enter directory:**
   ```bash
   cd ai-resume-concierge
   ```
2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and insert your keys:
   ```env
   OPENAI_API_KEY=sk-proj-yourActualKey...
   GITHUB_TOKEN=ghp_yourGithubToken...
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Start the FastAPI Backend:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
5. **Start the Streamlit Frontend (in a new terminal tab):**
   ```bash
   streamlit run app.py --server.port 8501
   ```
   Open `http://localhost:8501` to access the application dashboard.

---

## 7. Containerized Deployment

### Decoupled Stack via Docker Compose
Build and launch both Streamlit and FastAPI containers locally:
```bash
docker-compose up --build
```
- **Backend API Docs:** `http://localhost:8000/docs`
- **Streamlit Frontend Dashboard:** `http://localhost:8501`

### Cloud Run Deployment (GCP)
Deploy individual containers to Google Cloud Run:
```bash
# Build and deploy Backend
docker build -t gcr.io/YOUR_PROJECT/resume-backend -f Dockerfile.backend .
docker push gcr.io/YOUR_PROJECT/resume-backend
gcloud run deploy resume-verifier-api --image gcr.io/YOUR_PROJECT/resume-backend --set-env-vars="OPENAI_API_KEY=your_key" --allow-unauthenticated

# Build and deploy Frontend
docker build -t gcr.io/YOUR_PROJECT/resume-frontend -f Dockerfile.frontend .
docker push gcr.io/YOUR_PROJECT/resume-frontend
gcloud run deploy resume-verifier-ui --image gcr.io/YOUR_PROJECT/resume-frontend --set-env-vars="BACKEND_URL=https://resume-verifier-api-xxxx.run.app" --allow-unauthenticated
```

---

## 8. Future Roadmap
- **Real-Time LinkedIn Credential API:** Interface registry hooks to verify work histories.
- **Multimodal Video Mock Interviews:** Integrate speech-to-text validation and visual sentiment indicators in the Interview Coach.
- **Self-Hosting Model Weights:** Support local deployment of Llama-3/Mistral weights to ensure 100% on-premises data containment.
