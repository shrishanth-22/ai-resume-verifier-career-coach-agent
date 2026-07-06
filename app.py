import os
import time
import json
import textwrap
import streamlit as st
import httpx
from dotenv import load_dotenv

from backend.utils.helpers import get_demo_results

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
  page_title="AI Resume Verifier + Career Coach Agent",
  page_icon="⚡",
  layout="wide",
  initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
  st.session_state.page = "landing"
if "results" not in st.session_state:
  st.session_state.results = None
if "selected_tab" not in st.session_state:
  st.session_state.selected_tab = "Dashboard Overview"
if "interview_answers" not in st.session_state:
  st.session_state.interview_answers = {}
if "favorites" not in st.session_state:
  st.session_state.favorites = set()

def render_html(html_content: str):
  """Centralized HTML compiler ensuring markdown parser doesn't break styling blocks."""
  cleaned = "\n".join(line.strip() for line in html_content.splitlines())
  st.markdown(cleaned, unsafe_allow_html=True)

def glass_card(content_html: str, style: str = "", extra_classes: str = "") -> str:
  """Constructs a premium frosted glass card container."""
  classes = f"glass-card {extra_classes}".strip()
  style_attr = f'style="{style}"' if style else ''
  return f'<div class="{classes}" {style_attr}>{content_html}</div>'

def skill_chip(label: str, is_present: bool = True, extra_style: str = "") -> str:
  """Constructs a colored skill credential tag."""
  chip_class = "skill-chip-present" if is_present else "skill-chip-missing"
  style_attr = f'style="{extra_style}"' if extra_style else ''
  return f'<span class="{chip_class}" {style_attr}>{label}</span>'

def status_badge(status_text: str, badge_class: str = "") -> str:
  """Constructs a validation badge based on verification outcomes."""
  if not badge_class:
    if "Verified" in status_text or "Simulated" in status_text:
      badge_class = "badge-verified"
    elif "Warning" in status_text or "Mismatch" in status_text or "Unverified" in status_text:
      badge_class = "badge-unverified"
    else:
      badge_class = "badge-warning"
  return f'<span class="{badge_class}">{status_text}</span>'

def severity_badge(severity: str) -> str:
  """Renders risk severity tags."""
  sev_class = f"badge-{severity.lower()}"
  return f'<span class="{sev_class}">{severity.upper()}</span>'

def generate_radar_chart_svg(scores: dict) -> str:
  import math
  cx, cy = 170, 160
  r_max = 95
  axes = list(scores.keys())
  num_axes = len(axes)
  
  grid_svg = ""
  for level in [0.2, 0.4, 0.6, 0.8, 1.0]:
    r = r_max * level
    pts = []
    for i in range(num_axes):
      angle = -math.pi/2 + (2 * math.pi * i / num_axes)
      x = cx + r * math.cos(angle)
      y = cy + r * math.sin(angle)
      pts.append(f"{x},{y}")
    pts_str = " ".join(pts)
    grid_svg += f'<polygon points="{pts_str}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>\n'
    
  lines_labels_svg = ""
  for i, axis_name in enumerate(axes):
    angle = -math.pi/2 + (2 * math.pi * i / num_axes)
    x_end = cx + r_max * math.cos(angle)
    y_end = cy + r_max * math.sin(angle)
    lines_labels_svg += f'<line x1="{cx}" y1="{cy}" x2="{x_end}" y2="{y_end}" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>\n'
    
    label_r = r_max + 22
    lx = cx + label_r * math.cos(angle)
    ly = cy + label_r * math.sin(angle)
    
    text_anchor = "middle"
    if math.cos(angle) > 0.1:
      text_anchor = "start"
    elif math.cos(angle) < -0.1:
      text_anchor = "end"
      
    lines_labels_svg += f'<text x="{lx}" y="{ly}" fill="#CBD5E1" font-size="10.5" font-weight="600" text-anchor="{text_anchor}" dominant-baseline="middle" font-family="Outfit">{axis_name}</text>\n'

  data_pts = []
  for i, axis_name in enumerate(axes):
    score = scores.get(axis_name, 50)
    angle = -math.pi/2 + (2 * math.pi * i / num_axes)
    r = r_max * (score / 100.0)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    data_pts.append(f"{x},{y}")
    
  data_pts_str = " ".join(data_pts)
  
  polygon_svg = f'<polygon points="{data_pts_str}" fill="url(#radarGrad)" fill-opacity="0.32" stroke="#8B5CF6" stroke-width="2"/>\n'
  
  dots_svg = ""
  for i, axis_name in enumerate(axes):
    score = scores.get(axis_name, 50)
    angle = -math.pi/2 + (2 * math.pi * i / num_axes)
    r = r_max * (score / 100.0)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    dots_svg += f'<circle cx="{x}" cy="{y}" r="4" fill="#2563EB" stroke="#FFFFFF" stroke-width="1"/>\n'

  svg = f"""
  <svg width="340" height="320" viewBox="0 0 340 320" style="display: block; margin: 0 auto;">
      <defs>
          <radialGradient id="radarGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#2563EB" stop-opacity="0.4"/>
              <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.75"/>
          </radialGradient>
      </defs>
      {grid_svg}
      {lines_labels_svg}
      {polygon_svg}
      {dots_svg}
  </svg>
  """
  return svg

render_html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp, .main {
        font-family: 'Outfit', sans-serif !important;
        background: radial-gradient(ellipse at 15% 20%, rgba(37, 99, 235, 0.16), transparent 50%),
                    radial-gradient(ellipse at 85% 80%, rgba(139, 92, 246, 0.12), transparent 50%),
                    #070f24 !important;
        background-color: #070f24 !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* premium UI cards */
    .glass-card, .profile-card, .state-container {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.4) !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .glass-card:hover {
        border-color: rgba(37, 99, 235, 0.35) !important;
        box-shadow: 0 12px 40px 0 rgba(37, 99, 235, 0.18) !important;
        transform: translateY(-2px) !important;
    }
    
    h1, h2, .header-title {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #cbd5e1 60%, #2563EB 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 8px !important;
        line-height: 1.25 !important;
    }
    
    h3, h4, h5, h6 {
        color: #2563EB !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        margin-top: 5px;
    }
    
    p, li, span, label, div {
        color: #FFFFFF !important;
    }
    
    .muted-text {
        color: #94A3B8 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stFileUploaderDropzone"], .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px !important;
        padding: 35px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover, .stFileUploader > div:hover {
        border-color: #2563EB !important;
        background-color: rgba(37, 99, 235, 0.04) !important;
    }
    
    /* Credentials, Risk factors & Validation Badges */
    .skill-chip-present {
        background: rgba(34, 197, 94, 0.08) !important;
        border: 1px solid rgba(34, 197, 94, 0.25) !important;
        color: #4ADE80 !important;
        border-radius: 20px !important;
        padding: 5px 12px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        display: inline-flex !important;
        align-items: center !important;
        margin: 4px !important;
    }
    .skill-chip-missing {
        background: rgba(245, 158, 11, 0.08) !important;
        border: 1px solid rgba(245, 158, 11, 0.25) !important;
        color: #FBBF24 !important;
        border-radius: 20px !important;
        padding: 5px 12px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        display: inline-flex !important;
        align-items: center !important;
        margin: 4px !important;
    }
    
    .badge-verified {
        color: #4ADE80 !important;
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.25) !important;
        padding: 3px 10px !important;
        border-radius: 12px !important;
        font-size: 0.72rem !important;
        font-weight: bold !important;
        display: inline-block !important;
    }
    .badge-unverified {
        color: #F87171 !important;
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.25) !important;
        padding: 3px 10px !important;
        border-radius: 12px !important;
        font-size: 0.72rem !important;
        font-weight: bold !important;
        display: inline-block !important;
    }
    .badge-warning {
        color: #FBBF24 !important;
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.25) !important;
        padding: 3px 10px !important;
        border-radius: 12px !important;
        font-size: 0.72rem !important;
        font-weight: bold !important;
        display: inline-block !important;
    }
    
    .badge-high {
        color: #EF4444 !important;
        background: rgba(239, 68, 68, 0.12) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        font-size: 0.7rem !important;
        font-weight: bold !important;
    }
    .badge-medium {
        color: #F59E0B !important;
        background: rgba(245, 158, 11, 0.12) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        font-size: 0.7rem !important;
        font-weight: bold !important;
    }
    .badge-low {
        color: #60A5FA !important;
        background: rgba(96, 165, 250, 0.12) !important;
        border: 1px solid rgba(96, 165, 250, 0.3) !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        font-size: 0.7rem !important;
        font-weight: bold !important;
    }
    
    /* interactive timelines */
    .timeline {
        position: relative;
        padding-left: 28px;
        margin-left: 10px;
        border-left: 1.5px solid rgba(255, 255, 255, 0.1);
    }
    .timeline-item {
        position: relative;
        margin-bottom: 22px;
    }
    .timeline-dot {
        position: absolute;
        left: -35.5px;
        top: 6px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #2563EB;
        border: 2px solid #070f24;
    }
    .timeline-dot.warning-dot {
        background: #FBBF24;
    }
    .timeline-content {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        transition: all 0.25s ease;
    }
    .timeline-content:hover {
        border-color: rgba(37, 99, 235, 0.25);
        background: rgba(255, 255, 255, 0.04);
    }
    
    /* buttons styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB, #8B5CF6) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25) !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #7c3aed) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35) !important;
    }
    
    /* Secondary navbar buttons override */
    div.stButton > button[key*="demo"], div.stButton > button[key*="cancel"], div.stButton > button[key*="tab"] {
        background: rgba(255, 255, 255, 0.02) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: none !important;
    }
    div.stButton > button[key*="demo"]:hover, div.stButton > button[key*="cancel"]:hover, div.stButton > button[key*="tab"]:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
    }
    
    div.stButton > button[key*="active_tab"] {
        background: rgba(37, 99, 235, 0.12) !important;
        color: #3B82F6 !important;
        border: 1px solid rgba(37, 99, 235, 0.35) !important;
    }
    </style>
    """)

if st.session_state.page == "landing":
  
  nav_col1, nav_col2, nav_col3 = st.columns([5, 2, 2])
  with nav_col1:
    render_html("<h2 style='margin:0; font-weight:800; display:flex; align-items:center; gap:8px;'><span style='color:#2563EB;'>⚡</span> <span style='background:linear-gradient(90deg, #FFFFFF, #3B82F6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>AI Resume Verifier + Career Coach Agent</span></h2>")
  with nav_col2:
    if st.button("Try Demo →", key="nav_try_demo", use_container_width=True):
      st.session_state.results = get_demo_results()
      st.session_state.page = "results"
      st.rerun()
  with nav_col3:
    if st.button("Launch App", key="nav_upload", use_container_width=True):
      st.session_state.page = "upload"
      st.rerun()
      
  st.write("")
  st.write("")

  hero_col1, hero_col2 = st.columns([1.15, 0.85], gap="large")
  
  with hero_col1:
    render_html("""
      <div style="margin-bottom: 22px;">
          <span style="display: inline-block; background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.25); border-radius: 20px; padding: 4px 14px; font-size: 0.82rem; font-weight: 600; color: #3B82F6; font-family: 'Outfit';">
              • Resume Intelligence Platform & Multi-Agent System •
          </span>
      </div>
    """)
    render_html("<h1 style='font-size: 3.4rem; line-height: 1.15; margin-bottom: 22px;'>Advance Your Career with <br>Automated Agent Audits</h1>")
    render_html("<p class='muted-text' style='font-size:1.12rem; line-height: 1.6; margin-bottom: 30px;'>Integrate independent verification and parsing agents to validate claims, scan ATS compliance metrics, and unlock structured recruiter report scorecards instantly.</p>")
    
    btn_col1, btn_col2, _ = st.columns([2.2, 2.2, 3.2])
    with btn_col1:
      if st.button("Upload Resume", key="hero_cta_upload", use_container_width=True):
        st.session_state.page = "upload"
        st.rerun()
    with btn_col2:
      if st.button("View Demo", key="hero_cta_demo", use_container_width=True):
        st.session_state.results = get_demo_results()
        st.session_state.page = "results"
        st.rerun()
        
    render_html("""
      <div style="display:flex; gap:25px; margin-top:40px; font-family:'Outfit'; font-size:0.85rem; color:#94A3B8;">
          <span>🛡️ Ephemeral Zero Retention</span>
          <span>⚡ Live Repository Verification</span>
          <span>💼 Target Career Roadmapping</span>
      </div>
    """)
    
  with hero_col2:
    card_content = f"""
          <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom:20px;">
              <div style="display:flex; gap:6px;">
                  <span style="width:12px; height:12px; border-radius:50%; background-color:#FF5F56; display:inline-block;"></span>
                  <span style="width:12px; height:12px; border-radius:50%; background-color:#FFBD2E; display:inline-block;"></span>
                  <span style="width:12px; height:12px; border-radius:50%; background-color:#27C93F; display:inline-block;"></span>
              </div>
              <span style="font-family:monospace; font-size:0.75rem; color:rgba(255,255,255,0.45);">RECRUITER_EVAL_MATRIX.JSON</span>
          </div>
          
          <div style="display:grid; grid-template-columns:1fr 1.3fr; gap:20px; align-items:center;">
              <div style="text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                  <div style="position:relative; width:110px; height:110px; display:flex; align-items:center; justify-content:center;">
                      <svg style="position:absolute; width:100%; height:100%; transform:rotate(-90deg);">
                          <circle cx="55" cy="55" r="46" stroke="rgba(255,255,255,0.04)" stroke-width="8" fill="transparent"></circle>
                          <circle cx="55" cy="55" r="46" stroke="url(#heroGrad)" stroke-width="8" fill="transparent" stroke-dasharray="289" stroke-dashoffset="23" stroke-linecap="round"></circle>
                          <defs>
                              <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                  <stop offset="0%" stop-color="#2563EB"></stop>
                                  <stop offset="100%" stop-color="#8B5CF6"></stop>
                              </linearGradient>
                          </defs>
                      </svg>
                      <div>
                          <span style="font-size:2.1rem; font-weight:800; color:#FFFFFF;">92</span>
                          <span style="display:block; font-size:0.7rem; color:#94A3B8; font-weight:bold; margin-top:-5px;">STRENGTH</span>
                      </div>
                  </div>
              </div>
              
              <div style="display:flex; flex-direction:column; gap:12px;">
                  <div>
                      <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:3px;">
                          <span style="color:#94A3B8;">Career Readiness</span>
                          <span style="color:#2563EB; font-weight:bold;">75%</span>
                      </div>
                      <div style="background:rgba(255,255,255,0.04); height:5px; border-radius:3px;">
                          <div style="background:linear-gradient(90deg, #2563EB, #8B5CF6); height:100%; width:75%; border-radius:3px;"></div>
                      </div>
                  </div>
                  <div>
                      <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:3px;">
                          <span style="color:#94A3B8;">ATS Keyword Fit</span>
                          <span style="color:#4ADE80; font-weight:bold;">87%</span>
                      </div>
                      <div style="background:rgba(255,255,255,0.04); height:5px; border-radius:3px;">
                          <div style="background:#4ADE80; height:100%; width:87%; border-radius:3px;"></div>
                      </div>
                  </div>
              </div>
          </div>
          
          <hr style="border-color:rgba(255,255,255,0.08); margin:20px 0;">
          
          <div>
              <span style="font-size:0.75rem; color:rgba(255,255,255,0.4); font-family:monospace; display:block; margin-bottom:8px;">VERIFIED SYSTEM HIGHLIGHTS</span>
              <div style="display:flex; flex-wrap:wrap; gap:6px;">
                  {skill_chip("React Native")}
                  {skill_chip("TypeScript")}
                  {skill_chip("Kubernetes")}
              </div>
          </div>
    """
    render_html(glass_card(card_content, style="padding: 24px; border-radius: 16px; margin-top: 10px;"))

  st.write("---")

  st.write("")
  feat_col1, feat_col2, feat_col3 = st.columns(3)
  with feat_col1:
    render_html(glass_card("""
          <h4 style="color:#2563EB; margin-top:0;">📊 ATS & Keyword Calibration</h4>
          <p style="font-size:0.9rem; line-height:1.5; color:#CBD5E1; margin:0;">Optimize formatting matrices and score keyword alignment indices against target enterprise parameters.</p>
    """, style="min-height:170px;"))
  with feat_col2:
    render_html(glass_card("""
          <h4 style="color:#8B5CF6; margin-top:0;">🛡️ Claim Registry Verification</h4>
          <p style="font-size:0.9rem; line-height:1.5; color:#CBD5E1; margin:0;">Leverage automated agent checkers indexing live public repositories and APIs to audit applicant credentials.</p>
    """, style="min-height:170px;"))
  with feat_col3:
    render_html(glass_card("""
          <h4 style="color:#00D8F6; margin-top:0;">💬 Upskilling roadmap</h4>
          <p style="font-size:0.9rem; line-height:1.5; color:#CBD5E1; margin:0;">Generate custom practice interviews and milestone pathways loaded with learning resources.</p>
    """, style="min-height:170px;"))

  st.write("---")

  st.markdown("### ❔ Frequently Asked Questions")
  with st.expander("How does the Business Agent preserve data security?", expanded=False):
    render_html("<p style='color:#CBD5E1;'>The system operates ephemerally inside active memory blocks. Uploaded data frames and files are permanently discarded when the analysis terminates.</p>")
  with st.expander("Does this platform integrate with live repository APIs?", expanded=False):
    render_html("<p style='color:#CBD5E1;'>Yes. If provided, the verification agent triggers lookup hooks checking commit history records, star counts, and language footprints using the GitHub API.</p>")

elif st.session_state.page == "upload":
  
  if st.button("← Back to Home", key="back_home_btn"):
    st.session_state.page = "landing"
    st.rerun()

  render_html("<h1 style='text-align: center; margin-top: 10px;'>Upload Resume Profile</h1>")
  render_html("<p style='text-align: center; color: #CBD5E1; margin-bottom: 30px;'>Select your profile document and define target career objectives.</p>")

  up_col1, up_col2 = st.columns([1.2, 0.8], gap="large")

  with up_col1:
    st.markdown("### 📁 Select Resume File")
    uploaded_file = st.file_uploader(
      "Drag and drop PDF, PNG, JPG, or JPEG file (Max 5MB)",
      type=["pdf", "png", "jpg", "jpeg"]
    )
    
    st.write("")
    st.markdown("### 🎯 Define Target Career Goal")
    target_role = st.text_input(
      "Target Job Title",
      value="Senior Staff Engineer",
      help="The Multi-Agent System will calibrate your metrics and skills against this title."
    )

  with up_col2:
    render_html(glass_card("""
          <h4 style="margin-top:0; color:#2563EB;">📋 Agent Precheck List</h4>
          <ul style="color:#CBD5E1; padding-left: 20px; font-size: 0.9rem; line-height: 1.8;">
              <li>File is strictly PDF or standard image format</li>
              <li>Size does not exceed 5MB gateway bounds</li>
              <li>Includes direct github repository handles</li>
              <li>Target job title matches goal specifications</li>
          </ul>
    """, style="height: 100%;"))

  st.write("---")

  if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_size_mb = len(file_bytes) / (1024 * 1024)
    
    if len(file_bytes) > 5 * 1024 * 1024:
      st.error(f"File size exceeds 5MB gateway limits (Current size: {file_size_mb:.2f}MB)")
    else:
      if st.button("🚀 Execute Multi-Agent Verification Pipeline", key="start_analyze_btn", use_container_width=True):
        st.session_state.page = "processing"
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.uploaded_file_bytes = file_bytes
        st.session_state.target_role = target_role
        st.rerun()

elif st.session_state.page == "processing":
  render_html("<h2 style='text-align:center; margin-top:40px;'>⚡ Multi-Agent Recruitment Pipeline running</h2>")
  render_html("<p style='text-align:center; color:#94A3B8;'>Synthesizing independent parsing, ATS checks, verification, and upskilling coach agents...</p>")
  
  st.write("")
  progress_placeholder = st.empty()
  
  steps = [
    ("Resume Parser Agent parsing metadata...", "████░░░░░░ 40%"),
    ("ATS Optimization Agent scoring formatting...", "██████░░░░ 60%"),
    ("Resume Verification Agent auditing repositories...", "████████░░ 80%"),
    ("Skill Gap Agent mapping gap matrix...", "██████████ 100%"),
    ("Career & Interview Coach Agents packaging roadmaps...", "██████████ 100%"),
    ("Recruiter Assistant Agent compiling scorecard...", "██████████ 100%")
  ]
  
  for idx, (label, bar) in enumerate(steps):
    with progress_placeholder.container():
      inner_html = ""
      for p_idx in range(idx):
        inner_html += f"<span style='color:#4ADE80;'>✓ {steps[p_idx][0]}</span><br><code style='color:#4ADE80;'>[██████████] 100%</code><br>"
      
      inner_html += f"<span style='color:#8B5CF6;'>🔄 {label}</span><br><code style='color:#8B5CF6;'>[{bar}]</code><br>"
      
      for f_idx in range(idx + 1, len(steps)):
        inner_html += f"<span style='color:rgba(255,255,255,0.3);'>⏳ {steps[f_idx][0]}</span><br>"
        
      card_content = f"""
            <h4 style="margin-top:0; color:#2563EB;">Active Pipeline Steps:</h4>
            <div style="font-family: monospace; font-size:1.05rem; line-height: 1.8; color:#FFFFFF;">
                {inner_html}
            </div>
      """
      render_html(glass_card(card_content, style="max-width: 620px; margin: 0 auto; text-align: left;"))
      
    time.sleep(0.7)
    
  progress_placeholder.empty()
  
  try:
    mime_type = "application/pdf"
    if st.session_state.uploaded_file_name.lower().endswith(".png"):
      mime_type = "image/png"
    elif st.session_state.uploaded_file_name.lower().endswith((".jpg", ".jpeg")):
      mime_type = "image/jpeg"
      
    files = {"file": (st.session_state.uploaded_file_name, st.session_state.uploaded_file_bytes, mime_type)}
    data = {"target_role": st.session_state.target_role}
    
    api_url = f"{BACKEND_URL}/api/v1/analyze"
    with httpx.Client(timeout=60.0) as client:
      response = client.post(api_url, files=files, data=data)
      
    if response.status_code == 200:
      st.session_state.results = response.json()
      st.session_state.page = "results"
      st.rerun()
    else:
      st.error(f"Error from Backend Service (Status {response.status_code}): {response.text}")
      if st.button("Return to Upload"):
        st.session_state.page = "upload"
        st.rerun()
  except Exception as e:
    st.error(f"Failed to connect to backend service at {BACKEND_URL}. Check if the backend API is running. Error: {e}")
    if st.button("Return to Upload"):
      st.session_state.page = "upload"
      st.rerun()

elif st.session_state.page == "results":
  
  parsed_resume = st.session_state.results["parsed_resume"]
  ats_report = st.session_state.results["ats_report"]
  validation_report = st.session_state.results["validation_report"]
  skill_gap_report = st.session_state.results["skill_gap_report"]
  career_roadmap = st.session_state.results["career_roadmap"]
  interview_coach_report = st.session_state.results["interview_coach_report"]
  recruiter_report = st.session_state.results["recruiter_report"]
  
  header_col1, header_col2 = st.columns([6, 2])
  with header_col1:
    st.markdown("<h2 style='margin:0; font-weight:800;'><span style='color:#2563EB;'>⚡</span> Resume Intelligence Platform</h2>", unsafe_allow_html=True)
  with header_col2:
    if st.button("← Reset Workspace", key="results_reset_btn", use_container_width=True):
      st.session_state.page = "upload"
      st.session_state.results = None
      st.session_state.interview_answers = {}
      st.rerun()
      
  st.write("")
  
  tabs_cols = st.columns(5)
  tab_options = ["Dashboard Overview", "Skill Gap Analysis", "Career Roadmap", "AI Interview Coach", "Candidate Profile"]
  
  for idx, tab_name in enumerate(tab_options):
    with tabs_cols[idx]:
      btn_key = f"active_tab_{tab_name}" if st.session_state.selected_tab == tab_name else f"tab_{tab_name}"
      if st.button(tab_name, key=btn_key, use_container_width=True):
        st.session_state.selected_tab = tab_name
        st.rerun()
        
  st.write("---")

  if st.session_state.selected_tab == "Dashboard Overview":
    
    met_col1, met_col2, met_col3, met_col4 = st.columns(4)
    with met_col1:
      ats_dial = f"""
            <div style="position: relative; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; margin: 0 auto 5px auto;">
                <svg style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
                    <circle cx="50" cy="50" r="42" stroke="rgba(255,255,255,0.04)" stroke-width="7" fill="transparent"></circle>
                    <circle cx="50" cy="50" r="42" stroke="url(#atsGrad)" stroke-width="7" fill="transparent" stroke-dasharray="264" stroke-dashoffset="{264 - (264 * ats_report['ats_score'] / 100)}" stroke-linecap="round"></circle>
                    <defs>
                        <linearGradient id="atsGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#2563EB"></stop>
                            <stop offset="100%" stop-color="#8B5CF6"></stop>
                        </linearGradient>
                    </defs>
                </svg>
                <div>
                    <span style="font-size: 2rem; font-weight: 800; color: #FFFFFF; font-family: 'Outfit';">{ats_report['ats_score']}</span>
                </div>
            </div>
            <p style="font-size:0.8rem; color:#94A3B8; text-align:center; font-weight:bold; margin:0;">ATS OPTIMIZATION SCORE</p>
      """
      render_html(glass_card(ats_dial, style="text-align: center; padding: 15px 10px;"))
      
    with met_col2:
      strength_dial = f"""
            <div style="position: relative; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; margin: 0 auto 5px auto;">
                <svg style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
                    <circle cx="50" cy="50" r="42" stroke="rgba(255,255,255,0.04)" stroke-width="7" fill="transparent"></circle>
                    <circle cx="50" cy="50" r="42" stroke="url(#strengthGrad)" stroke-width="7" fill="transparent" stroke-dasharray="264" stroke-dashoffset="{264 - (264 * recruiter_report['resume_strength_score'] / 100)}" stroke-linecap="round"></circle>
                    <defs>
                        <linearGradient id="strengthGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#3B82F6"></stop>
                            <stop offset="100%" stop-color="#00D8F6"></stop>
                        </linearGradient>
                    </defs>
                </svg>
                <div>
                    <span style="font-size: 2rem; font-weight: 800; color: #FFFFFF; font-family: 'Outfit';">{recruiter_report['resume_strength_score']}</span>
                </div>
            </div>
            <p style="font-size:0.8rem; color:#94A3B8; text-align:center; font-weight:bold; margin:0;">RESUME STRENGTH SCORE</p>
      """
      render_html(glass_card(strength_dial, style="text-align: center; padding: 15px 10px;"))
      
    with met_col3:
      readiness_dial = f"""
            <div style="position: relative; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; margin: 0 auto 5px auto;">
                <svg style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
                    <circle cx="50" cy="50" r="42" stroke="rgba(255,255,255,0.04)" stroke-width="7" fill="transparent"></circle>
                    <circle cx="50" cy="50" r="42" stroke="url(#readyGrad)" stroke-width="7" fill="transparent" stroke-dasharray="264" stroke-dashoffset="{264 - (264 * recruiter_report['career_readiness_score'] / 100)}" stroke-linecap="round"></circle>
                    <defs>
                        <linearGradient id="readyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#8B5CF6"></stop>
                            <stop offset="100%" stop-color="#EC4899"></stop>
                        </linearGradient>
                    </defs>
                </svg>
                <div>
                    <span style="font-size: 2rem; font-weight: 800; color: #FFFFFF; font-family: 'Outfit';">{recruiter_report['career_readiness_score']}</span>
                </div>
            </div>
            <p style="font-size:0.8rem; color:#94A3B8; text-align:center; font-weight:bold; margin:0;">CAREER READINESS SCORE</p>
      """
      render_html(glass_card(readiness_dial, style="text-align: center; padding: 15px 10px;"))
      
    with met_col4:
      rec_html = f"""
            <div style="height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <span style="font-size: 0.95rem; font-weight: 800; color: #4ADE80; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.25); padding: 8px 14px; border-radius: 12px; font-family: 'Outfit'; max-width: 100%;">
                    {recruiter_report['hiring_recommendation']}
                </span>
            </div>
            <p style="font-size:0.8rem; color:#94A3B8; text-align:center; font-weight:bold; margin:0;">HIRING RECOMMENDATION</p>
      """
      render_html(glass_card(rec_html, style="padding: 15px 10px;"))

    st.write("")
    
    dash_col1, dash_col2 = st.columns([1.1, 0.9], gap="large")
    
    with dash_col1:
      st.markdown("### 📝 Recruiter Summary & Fit Analysis")
      summary_content = f"""
            <h4 style="margin-top:0; color:#2563EB;">Executive Summary</h4>
            <p style="font-size:0.95rem; line-height:1.6; color:#E2E8F0; margin-bottom:15px;">{recruiter_report['executive_summary']}</p>
            
            <h4 style="color:#2563EB;">Key Resume Insights</h4>
            <ul style="color:#E2E8F0; padding-left: 20px; font-size: 0.92rem; line-height: 1.7;">
                {"".join(f"<li>{insight}</li>" for insight in recruiter_report['resume_insights'])}
            </ul>
      """
      render_html(glass_card(summary_content, style="padding: 24px;"))
      
    with dash_col2:
      st.markdown("### ⚠️ Recruiter Risk Assessment")
      
      risk_html = "<div style='display:flex; flex-direction:column; gap:12px;'>"
      for risk in recruiter_report['risk_assessment']:
        risk_card = f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <b style="font-size: 0.9rem; color:#EF4444;">{risk['risk_factor']}</b>
                {severity_badge(risk['severity'])}
            </div>
            <p style="font-size:0.85rem; margin:0; color:#CBD5E1;"><b>Mitigation:</b> {risk['mitigation']}</p>
        """
        risk_html += glass_card(risk_card, style="padding: 15px !important; margin-bottom: 0px !important;")
      risk_html += "</div>"
      render_html(risk_html)

  elif st.session_state.selected_tab == "Skill Gap Analysis":
    
    st.markdown("### 📊 Skills Calibration & Gap Matrix")
    
    gap_col1, gap_col2 = st.columns([0.8, 1.2], gap="large")
    
    with gap_col1:
      st.markdown("#### Skill Radar Chart")
      all_radar_vals = {
          "Frontend": 65,
          "Backend": 65,
          "System Design": 50,
          "DevOps": 40,
          "Leadership": 50
      }
      
      p_skills = [s.lower() for s in skill_gap_report["present_skills"]]
      if "react" in p_skills or "typescript" in p_skills:
          all_radar_vals["Frontend"] = 92
      if "node.js" in p_skills or "python" in p_skills or "fastapi" in p_skills:
          all_radar_vals["Backend"] = 85
      if "kubernetes" in p_skills or "docker" in p_skills:
          all_radar_vals["DevOps"] = 80
      if "vercel" in p_skills or len(parsed_resume.get("experiences", [])) > 1:
          all_radar_vals["Leadership"] = 75
          all_radar_vals["System Design"] = 70
          
      radar_svg = generate_radar_chart_svg(all_radar_vals)
      render_html(glass_card(radar_svg, style="padding: 10px 0; min-height:340px; display:flex; align-items:center; justify-content:center;"))
      
    with gap_col2:
      st.markdown("#### Prioritized Skill Gaps")
      
      matrix_html = "<div style='display:flex; flex-direction:column; gap:12px;'>"
      for item in skill_gap_report.get("skill_gap_matrix", []):
        matrix_card = f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="display:inline-block;">{skill_chip(item['skill'], is_present=False)}</span>
                <span style="font-size:0.8rem; background:rgba(245,158,11,0.12); color:#F59E0B; font-weight:bold; padding:3px 10px; border-radius:10px;">Priority Score: {item['priority']}%</span>
            </div>
            <p style="font-size:0.88rem; margin:0; color:#CBD5E1;"><b>Context:</b> {item['gap_reason']}</p>
        """
        matrix_html += glass_card(matrix_card, style="padding: 15px !important; margin-bottom: 0px !important;")
      matrix_html += "</div>"
      render_html(matrix_html)

    st.write("---")
    
    match_col1, match_col2 = st.columns(2)
    with match_col1:
      st.markdown("#### Present Credentials")
      chips = "".join(skill_chip(s, is_present=True) for s in skill_gap_report["present_skills"])
      render_html(glass_card(f"<div style='flex-wrap:wrap; display:flex;'>{chips}</div>", style="min-height: 120px;"))
    with match_col2:
      st.markdown("#### Missing Target Competencies")
      chips = "".join(skill_chip(s, is_present=False) for s in skill_gap_report["missing_skills"])
      render_html(glass_card(f"<div style='flex-wrap:wrap; display:flex;'>{chips}</div>", style="min-height: 120px;"))

  elif st.session_state.selected_tab == "Career Roadmap":
    
    st.markdown(f"### 🚀 Chronological Upskilling Roadmap for {parsed_resume['candidate_info']['name']}")
    
    road_col1, road_col2 = st.columns([1.1, 0.9], gap="large")
    
    with road_col1:
      st.markdown("#### Chronological Milestones")
      
      timeline_html = "<div class='timeline'>"
      for idx, milestone in enumerate(career_roadmap["milestones"]):
        items_list = "".join(f"<li style='margin-bottom:5px;'>{item}</li>" for item in milestone["items"])
        resources_list = "".join(f"<li style='margin-bottom:5px;'>📖 {res}</li>" for res in milestone["resources"])
        
        timeline_card = f"""
            <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap;">
                        <h4 style="margin:0; color:#2563EB; font-size:1.02rem;">📍 Milestone {idx+1}: {milestone['name']}</h4>
                        <span style="font-size:0.75rem; background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.25); color:#3B82F6; font-weight:bold; padding:2px 8px; border-radius:10px;">{milestone['timeline']}</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:8px;">
                        <div>
                            <span style="font-size:0.78rem; color:#94A3B8; font-weight:bold; display:block; margin-bottom:4px;">ACTION ITEMS</span>
                            <ul style="color:#FFFFFF; font-size:0.85rem; padding-left:15px; margin:0;">
                                {items_list}
                            </ul>
                        </div>
                        <div>
                            <span style="font-size:0.78rem; color:#94A3B8; font-weight:bold; display:block; margin-bottom:4px;">COACH RESOURCES</span>
                            <ul style="color:#FFFFFF; font-size:0.85rem; padding-left:15px; margin:0; list-style-type:none;">
                                {resources_list}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        """
        timeline_html += timeline_card
      timeline_html += "</div>"
      render_html(timeline_html)
      
    with road_col2:
      st.markdown("#### Learning Progress Tracks")
      
      progress_html = "<div style='display:flex; flex-direction:column; gap:15px;'>"
      for prog in career_roadmap.get("learning_progress", []):
        prog_bar = f"""
            <div style="margin-bottom:2px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="color:#FFFFFF; font-weight:600;">{prog['milestone']}</span>
                    <span style="color:#8B5CF6; font-weight:bold;">{prog['percentage']}% Completed</span>
                </div>
                <div style="background:rgba(255,255,255,0.04); height:8px; border-radius:4px; overflow:hidden;">
                    <div style="background:linear-gradient(90deg, #2563EB, #8B5CF6); height:100%; width:{prog['percentage']}%;"></div>
                </div>
            </div>
        """
        progress_html += glass_card(prog_bar, style="padding:16px !important; margin-bottom:0 !important;")
      progress_html += "</div>"
      render_html(progress_html)
      
      st.write("")
      st.markdown("#### General Resume Optimization Tips")
      tips_list = "".join(f"<li style='margin-bottom:8px; font-size:0.9rem; color:#CBD5E1;'>{tip}</li>" for tip in career_roadmap["general_resume_tips"])
      render_html(glass_card(f"<ul style='margin:0; padding-left:20px;'>{tips_list}</ul>"))

  elif st.session_state.selected_tab == "AI Interview Coach":
    
    st.markdown("### 💬 AI Interview Coaching Arena")
    render_html("<p class='muted-text'>Practice targeted questions generated by the Interview Coach Agent corresponding to candidate gaps.</p>")
    
    coach_col1, coach_col2 = st.columns([1.3, 0.7], gap="large")
    
    with coach_col1:
      for idx, item in enumerate(interview_coach_report.get("questions", [])):
        q_card = f"""
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                  <span style="font-size:0.75rem; background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.25); color:#3B82F6; font-weight:bold; padding:2px 8px; border-radius:10px;">Q{idx+1}: {item['category']}</span>
                  <span style="font-size:0.75rem; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.25); color:#F87171; font-weight:bold; padding:2px 8px; border-radius:10px;">{item['difficulty']}</span>
              </div>
              <h4 style="margin:0 0 12px 0; color:#FFFFFF; font-size:1.02rem;">{item['question']}</h4>
        """
        render_html(glass_card(q_card, style="margin-bottom: 20px;"))
        
        is_fav = item["id"] in st.session_state.favorites
        fav_label = "★ Favorited" if is_fav else "☆ Favorite Question"
        
        btn_cols = st.columns([2, 2.5, 3])
        
        with btn_cols[0]:
          if st.button(fav_label, key=f"fav_btn_{item['id']}", use_container_width=True):
            if is_fav:
              st.session_state.favorites.remove(item["id"])
            else:
              st.session_state.favorites.add(item["id"])
            st.rerun()
            
        with btn_cols[1]:
          show_ans = st.session_state.interview_answers.get(item["id"], False)
          ans_label = "Hide Suggested Answer" if show_ans else "Reveal Suggested Answer"
          if st.button(ans_label, key=f"reveal_btn_{item['id']}", use_container_width=True):
            st.session_state.interview_answers[item["id"]] = not show_ans
            st.rerun()
            
        if st.session_state.interview_answers.get(item["id"], False):
          ans_card = f"""
                <b style="color:#4ADE80; font-size:0.85rem;">IDEAL ANSWER SUGGESTION:</b>
                <p style="font-size:0.88rem; color:#CBD5E1; line-height:1.5; margin-top:5px; margin-bottom:0;">{item['answer']}</p>
          """
          render_html(glass_card(ans_card, style="margin-top:15px; border-color:#4ADE80 !important; padding:15px !important;"))
          
        answer_input = st.text_area("Draft practice response:", key=f"practice_txt_{item['id']}", placeholder="Draft candidate response to run real-time key term checks...")
        if len(answer_input) > 0:
          if st.button("Evaluate Response", key=f"eval_btn_{item['id']}"):
            matched_keywords = [w for w in item["answer"].lower().split() if len(w) > 4 and w in answer_input.lower()]
            if len(matched_keywords) > 2:
              st.success(f"Excellent concepts matched: {', '.join(set(matched_keywords[:4]))}.")
            else:
              st.warning("Concept match score low. Incorporate more technical details from the ideal answer.")
              
        st.write("---")
        
    with coach_col2:
      tips_content = """
            <h4 style="margin-top:0; color:#2563EB;">💡 Practice Guidelines</h4>
            <p style="font-size:0.9rem; color:#CBD5E1; line-height:1.6; margin:0;">
                1. <b>Concept Precision:</b> Name specific network configurations or database topologies where applicable.<br><br>
                2. <b>The STAR Method:</b> Frame behavioral scenarios around (Situation, Task, Action, Result) paradigms.<br><br>
                3. <b>System Scale:</b> Highlight memory boundaries, partition limits, and redundancy fail-safes.
            </p>
      """
      render_html(glass_card(tips_content))

  elif st.session_state.selected_tab == "Candidate Profile":
    
    st.markdown("### 👤 Candidate Registry & Timeline Verification")
    
    prof_col1, prof_col2 = st.columns([1.1, 0.9], gap="large")
    info = parsed_resume["candidate_info"]
    
    with prof_col1:
      st.markdown("#### Candidate Details")
      identity_content = f"""
            <h4 style="color:#2563EB; margin-top:0;">Identity Coordinates</h4>
            <p style="margin-bottom:8px;">📧 <b>Email:</b> {info['email'] or 'N/A'}</p>
            <p style="margin-bottom:8px;">📞 <b>Phone:</b> {info['phone'] or 'N/A'}</p>
            <p style="margin-bottom:8px;">🐙 <b>GitHub Username:</b> {info['github_username'] or 'N/A'}</p>
      """
      render_html(glass_card(identity_content, style="padding: 20px;", extra_classes="profile-card"))
      
      if info.get("websites"):
        links_content = "<h4>🔗 Portfolio Links</h4>"
        for w in info["websites"]:
          links_content += f"<a href='{w}' target='_blank' style='color:#3B82F6; font-size:0.92rem;'>{w}</a><br>"
        render_html(glass_card(links_content))
        
      st.markdown("#### Career Timeline")
      exp_inner = "<div class='timeline'>"
      for exp in parsed_resume.get("experiences", []):
        exp_inner += f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content" style="padding: 12px 16px;">
                <b style="color:#8B5CF6; font-size:0.95rem;">{exp['role']}</b> at <b>{exp['company']}</b><br>
                <span style="font-size:0.8rem; color:#94A3B8;">{exp['start_date']} - {exp['end_date']}</span><br>
                <p style="font-size:0.88rem; margin-top:6px; color:#E2E8F0; margin-bottom:0;">{exp['description']}</p>
            </div>
        </div>
        """
      exp_inner += "</div>"
      render_html(exp_inner)
      
    with prof_col2:
      st.markdown("#### Verification Claim Logs")
      
      claims_html = "<div style='display:flex; flex-direction:column; gap:12px;'>"
      for claim in validation_report.get("claims", []):
        claim_content = f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <b style="font-size: 0.9rem; color:#2563EB;">{claim['claim_type']}</b>
                {status_badge(claim['status'])}
            </div>
            <p style="font-size:0.88rem; margin:0 0 4px 0; color:#FFFFFF;">Target: <code>{claim['target']}</code></p>
            <span style="font-size:0.8rem; color:#94A3B8;">{claim['notes']}</span>
        """
        claims_html += glass_card(claim_content, style="padding: 14px !important; margin-bottom: 0px !important;")
      claims_html += "</div>"
      render_html(claims_html)
      
      st.write("")
      
      st.markdown("#### Verification Run Timeline")
      timeline_html = "<div class='timeline'>"
      for evt in validation_report.get("verification_timeline", []):
        dot_class = "warning-dot" if "Warning" in evt["status"] else ""
        timeline_card = f"""
            <div class="timeline-item">
                <div class="timeline-dot {dot_class}"></div>
                <div class="timeline-content" style="padding: 10px 14px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                        <span style="font-size:0.85rem; color:#FFFFFF; font-weight:600;">{evt['event']}</span>
                        <span style="font-size:0.72rem; color:#94A3B8;">{evt['date']}</span>
                    </div>
                </div>
            </div>
        """
        timeline_html += timeline_card
      timeline_html += "</div>"
      render_html(timeline_html)
