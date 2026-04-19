import streamlit as st
from agents.manager import run_incident_resolver
from dotenv import load_dotenv
import os
import time

load_dotenv()

st.set_page_config(
    page_title="DevOps Incident Resolver",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Architects+Daughter&display=swap');

* { font-family: 'Nunito', sans-serif; }

.stApp {
    background: #fffdf7;
}

[data-testid="stAppViewContainer"] {
    background: #fffdf7;
}

[data-testid="stHeader"] { background: transparent; }

/* ── Doodle SVG background ── */
.doodle-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    opacity: 0.07;
}

.main-wrap {
    position: relative;
    z-index: 1;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}

.hero-tag {
    display: inline-block;
    background: #fff3cd;
    border: 2.5px solid #f0c040;
    color: #9a6f00;
    padding: 5px 18px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    font-family: 'Architects Daughter', cursive;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    color: #1a1a2e;
    line-height: 1.1;
    margin-bottom: 0.8rem;
    letter-spacing: -1px;
}

.hero-title span {
    color: #ff6b35;
    position: relative;
    display: inline-block;
}

.hero-title span::after {
    content: '';
    position: absolute;
    bottom: 2px;
    left: 0;
    width: 100%;
    height: 6px;
    background: #ffd166;
    z-index: -1;
    border-radius: 3px;
}

.hero-sub {
    font-size: 1rem;
    color: #6b7280;
    max-width: 540px;
    margin: 0 auto 1.5rem;
    line-height: 1.7;
    font-weight: 600;
}

.pills-row {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}

.pill {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 700;
    color: #374151;
    display: flex;
    align-items: center;
    gap: 6px;
}

.pill-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── Agent flow card ── */
.flow-card {
    background: white;
    border: 2.5px solid #e5e7eb;
    border-radius: 20px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 4px 4px 0px #e5e7eb;
}

.flow-card-title {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 1.2rem;
    font-family: 'Architects Daughter', cursive;
}

.flow-row {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}

.flow-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
}

.flow-icon-box {
    width: 52px; height: 52px;
    border-radius: 14px;
    border: 2.5px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    background: white;
    position: relative;
}

.flow-icon-box::after {
    content: '';
    position: absolute;
    bottom: -4px; right: -4px;
    width: 100%; height: 100%;
    border-radius: 14px;
    z-index: -1;
}

.fi-yellow { border-color: #f0c040; }
.fi-yellow::after { background: #fef3c7; }
.fi-orange { border-color: #fb923c; }
.fi-orange::after { background: #ffedd5; }
.fi-blue { border-color: #60a5fa; }
.fi-blue::after { background: #dbeafe; }
.fi-green { border-color: #34d399; }
.fi-green::after { background: #d1fae5; }
.fi-red { border-color: #f87171; }
.fi-red::after { background: #fee2e2; }
.fi-purple { border-color: #a78bfa; }
.fi-purple::after { background: #ede9fe; }

.flow-node-label {
    font-size: 10px;
    font-weight: 800;
    color: #6b7280;
    text-align: center;
    line-height: 1.3;
    font-family: 'Architects Daughter', cursive;
}

.flow-arrow-txt {
    font-size: 20px;
    color: #d1d5db;
    margin: 0 2px;
    margin-bottom: 18px;
    font-weight: 900;
}

/* ── Input card ── */
.input-card {
    background: white;
    border: 2.5px solid #e5e7eb;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 4px 4px 0px #e5e7eb;
    margin-bottom: 1rem;
}

.card-title {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 1rem;
    font-family: 'Architects Daughter', cursive;
}

.log-box {
    background: #f9fafb;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    line-height: 1.9;
    max-height: 200px;
    overflow-y: auto;
}

.le { color: #ef4444; font-weight: 700; }
.lc { color: #dc2626; font-weight: 800; }
.lw { color: #f59e0b; font-weight: 700; }
.ln { color: #374151; }

/* ── Action card ── */
.action-card {
    background: white;
    border: 2.5px solid #e5e7eb;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 4px 4px 0px #e5e7eb;
}

.checklist-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1.5px dashed #f3f4f6;
    font-size: 13px;
    font-weight: 700;
    color: #374151;
}

.checklist-item:last-child { border-bottom: none; }

.check-icon {
    width: 26px; height: 26px;
    border-radius: 8px;
    border: 2px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
}

/* ── Button ── */
.stButton > button {
    background: #ff6b35 !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    border: 2.5px solid #e85a26 !important;
    border-radius: 14px !important;
    padding: 0.7rem 2rem !important;
    box-shadow: 4px 4px 0px #e85a26 !important;
    transition: all 0.1s ease !important;
    font-family: 'Nunito', sans-serif !important;
    letter-spacing: 0.3px !important;
}

.stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px #e85a26 !important;
}

.stButton > button:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px #e85a26 !important;
}

/* ── Result cards ── */
.res-card {
    background: white;
    border: 2.5px solid #e5e7eb;
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 4px 4px 0px #e5e7eb;
    height: 100%;
}

.res-card-title {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9ca3af;
    padding-bottom: 0.8rem;
    border-bottom: 2px dashed #f3f4f6;
    margin-bottom: 1rem;
    font-family: 'Architects Daughter', cursive;
}

.field-label {
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #9ca3af;
    margin-bottom: 4px;
}

.field-value {
    font-size: 13px;
    font-weight: 600;
    color: #1f2937;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.sev-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 800;
    border: 2px solid;
    font-family: 'Architects Daughter', cursive;
}

.sev-critical { background: #fee2e2; border-color: #fca5a5; color: #dc2626; }
.sev-high { background: #fff3cd; border-color: #f0c040; color: #9a6f00; }
.sev-low { background: #d1fae5; border-color: #6ee7b7; color: #059669; }

.role-badge {
    display: inline-block;
    background: #ede9fe;
    border: 2px solid #c4b5fd;
    color: #7c3aed;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 800;
    font-family: 'Architects Daughter', cursive;
}

.fix-step-row {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 8px 0;
    border-bottom: 1.5px dashed #f3f4f6;
}

.fix-step-row:last-child { border-bottom: none; }

.step-num {
    width: 24px; height: 24px;
    border-radius: 8px;
    background: #fff3cd;
    border: 2px solid #f0c040;
    color: #9a6f00;
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-family: 'Architects Daughter', cursive;
}

.step-txt {
    font-size: 12px;
    font-weight: 600;
    color: #374151;
    line-height: 1.5;
}

.conf-bar-bg {
    height: 8px;
    background: #f3f4f6;
    border-radius: 100px;
    border: 1.5px solid #e5e7eb;
    overflow: hidden;
    margin-top: 6px;
}

.conf-bar-fill {
    height: 100%;
    border-radius: 100px;
}

.github-box {
    background: #f0fdf4;
    border: 2.5px solid #86efac;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 3px 3px 0px #86efac;
}

.github-circle {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: #dcfce7;
    border: 2px solid #86efac;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.self-fix-banner {
    background: #fff3cd;
    border: 2px solid #f0c040;
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 13px;
    font-weight: 700;
    color: #9a6f00;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Architects Daughter', cursive;
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, #ff6b35, #ffd166) !important;
    border-radius: 100px !important;
}

/* Radio */
.stRadio > div > label {
    background: white !important;
    border: 2px solid #e5e7eb !important;
    border-radius: 10px !important;
    padding: 7px 16px !important;
    color: #374151 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
}

.stRadio > div > label > div {
    color: #374151 !important;
}

.stRadio label p {
    color: #374151 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

[data-testid="stMarkdownContainer"] p {
    color: #374151 !important;
}

div[role="radiogroup"] label span {
    color: #374151 !important;
}

/* TextArea */
.stTextArea textarea {
    background: #f9fafb !important;
    border: 2px solid #e5e7eb !important;
    border-radius: 12px !important;
    color: #1f2937 !important;
    font-size: 12px !important;
}

/* status text */
.status-txt {
    font-size: 13px;
    font-weight: 700;
    color: #ff6b35;
    font-family: 'Architects Daughter', cursive;
    padding: 8px 0;
}

/* scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f9fafb; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 100px; }

/* footer */
.footer-txt {
    text-align: center;
    font-size: 12px;
    color: #d1d5db;
    font-family: 'Architects Daughter', cursive;
    padding: 2rem 0 1rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ── Doodle background SVG ──
st.markdown("""
<svg class="doodle-bg" viewBox="0 0 1400 900" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#374151" fill="none" stroke-width="2.5" stroke-linecap="round">
    <!-- Stars -->
    <path d="M80 80 L83 70 L86 80 L96 83 L86 86 L83 96 L80 86 L70 83 Z"/>
    <path d="M1320 120 L1323 110 L1326 120 L1336 123 L1326 126 L1323 136 L1320 126 L1310 123 Z"/>
    <path d="M200 750 L202 743 L204 750 L211 752 L204 754 L202 761 L200 754 L193 752 Z"/>
    <path d="M1100 800 L1102 793 L1104 800 L1111 802 L1104 804 L1102 811 L1100 804 L1093 802 Z"/>
    <!-- Circles -->
    <circle cx="150" cy="300" r="30"/>
    <circle cx="150" cy="300" r="18"/>
    <circle cx="1250" cy="200" r="25"/>
    <circle cx="1250" cy="200" r="14"/>
    <circle cx="50" cy="600" r="20"/>
    <circle cx="1350" cy="600" r="35"/>
    <circle cx="1350" cy="600" r="22"/>
    <!-- Zigzag lines -->
    <polyline points="0,180 30,160 60,180 90,160 120,180 150,160"/>
    <polyline points="1250,700 1280,680 1310,700 1340,680 1370,700 1400,680"/>
    <polyline points="0,450 30,430 60,450 90,430 120,450"/>
    <!-- Squares -->
    <rect x="1300" y="350" width="40" height="40" rx="6" transform="rotate(15,1320,370)"/>
    <rect x="30" y="700" width="32" height="32" rx="4" transform="rotate(-10,46,716)"/>
    <rect x="680" y="30" width="28" height="28" rx="4" transform="rotate(20,694,44)"/>
    <rect x="700" y="850" width="35" height="35" rx="5" transform="rotate(-15,717,867)"/>
    <!-- Dotted lines -->
    <line x1="300" y1="50" x2="500" y2="50" stroke-dasharray="6,8"/>
    <line x1="900" y1="850" x2="1100" y2="850" stroke-dasharray="6,8"/>
    <line x1="50" y1="400" x2="50" y2="550" stroke-dasharray="6,8"/>
    <line x1="1350" y1="250" x2="1350" y2="450" stroke-dasharray="6,8"/>
    <!-- Arrows -->
    <path d="M1150 100 Q1180 80 1210 100" stroke-dasharray="4,5"/>
    <path d="M1205 95 L1210 100 L1204 104"/>
    <path d="M180 650 Q210 630 240 650" stroke-dasharray="4,5"/>
    <path d="M235 645 L240 650 L234 654"/>
    <!-- Cross marks -->
    <path d="M400 800 L414 814 M414 800 L400 814"/>
    <path d="M980 60 L994 74 M994 60 L980 74"/>
    <!-- Triangles -->
    <polygon points="1380,750 1400,790 1360,790"/>
    <polygon points="20,200 40,240 0,240"/>
    <!-- Small dots cluster -->
    <circle cx="600" cy="870" r="3" fill="#374151"/>
    <circle cx="615" cy="875" r="3" fill="#374151"/>
    <circle cx="630" cy="868" r="3" fill="#374151"/>
    <circle cx="645" cy="873" r="3" fill="#374151"/>
    <circle cx="800" cy="40" r="3" fill="#374151"/>
    <circle cx="815" cy="45" r="3" fill="#374151"/>
    <circle cx="830" cy="38" r="3" fill="#374151"/>
    <!-- Spiral-like -->
    <path d="M1050 150 Q1070 130 1090 150 Q1110 170 1090 190 Q1070 210 1050 190"/>
    <!-- Lightning bolt -->
    <path d="M350 750 L340 775 L352 775 L342 800"/>
    <path d="M1060 700 L1050 725 L1062 725 L1052 750"/>
  </g>
</svg>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero">
    <div class="hero-tag">⚡ Multi-Agent AI System</div>
    <div class="hero-title">DevOps Incident<br/><span>Resolver Agent</span></div>
    <div class="hero-sub">Drop your error logs. Three AI agents collaborate to find the root cause, research a fix, and file a GitHub issue — all by themselves.</div>
    <div class="pills-row">
        <div class="pill"><div class="pill-dot" style="background:#ff6b35;"></div>3 Specialized Agents</div>
        <div class="pill"><div class="pill-dot" style="background:#ffd166;"></div>Under 2 Minutes</div>
        <div class="pill"><div class="pill-dot" style="background:#34d399;"></div>Auto GitHub Issues</div>
        <div class="pill"><div class="pill-dot" style="background:#a78bfa;"></div>Self-Correcting</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Flow card ──
st.markdown("""
<div class="flow-card">
    <div class="flow-card-title">✏️ How It Works</div>
    <div class="flow-row">
        <div class="flow-node">
            <div class="flow-icon-box fi-yellow">📂</div>
            <div class="flow-node-label">Log<br/>Input</div>
        </div>
        <div class="flow-arrow-txt">→</div>
        <div class="flow-node">
            <div class="flow-icon-box fi-purple">🧠</div>
            <div class="flow-node-label">Manager<br/>Agent</div>
        </div>
        <div class="flow-arrow-txt">→</div>
        <div class="flow-node">
            <div class="flow-icon-box fi-blue">🔍</div>
            <div class="flow-node-label">Log<br/>Analyzer</div>
        </div>
        <div class="flow-arrow-txt">→</div>
        <div class="flow-node">
            <div class="flow-icon-box fi-green">🌐</div>
            <div class="flow-node-label">Web Search<br/>Agent</div>
        </div>
        <div class="flow-arrow-txt">→</div>
        <div class="flow-node">
            <div class="flow-icon-box fi-orange">🔁</div>
            <div class="flow-node-label">Self<br/>Correct</div>
        </div>
        <div class="flow-arrow-txt">→</div>
        <div class="flow-node">
            <div class="flow-icon-box fi-green">📝</div>
            <div class="flow-node-label">GitHub<br/>Issue</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.15, 0.85], gap="large")

with col_left:
    st.markdown('<div class="card-title">📋 Log Input</div>', unsafe_allow_html=True)
    input_method = st.radio(
        "method",
        ["Use Sample Log", "Upload Log File", "Paste Manually"],
        horizontal=True,
        label_visibility="collapsed"
    )
    log_content = ""

    if input_method == "Use Sample Log":
        try:
            with open("sample_logs/error.log", "r") as f:
                log_content = f.read()
            colored = ""
            for line in log_content.split("\n"):
                if "CRITICAL" in line:
                    colored += f'<div class="lc">{line}</div>'
                elif "ERROR" in line:
                    colored += f'<div class="le">{line}</div>'
                elif "WARNING" in line:
                    colored += f'<div class="lw">{line}</div>'
                elif line.strip():
                    colored += f'<div class="ln">{line}</div>'
            st.markdown(f'<div class="log-box">{colored}</div>', unsafe_allow_html=True)
        except:
            st.error("sample_logs/error.log not found")

    elif input_method == "Upload Log File":
        uploaded = st.file_uploader("Upload", type=["log","txt"], label_visibility="collapsed")
        if uploaded:
            log_content = uploaded.read().decode("utf-8")
            st.markdown(f'<div class="log-box">{log_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="border: 2px dashed #d1d5db; border-radius: 14px; padding: 2rem; text-align: center; color: #9ca3af; font-size: 13px; font-weight: 700; background: #f9fafb;">
                📁 Drop a .log or .txt file here
            </div>""", unsafe_allow_html=True)

    elif input_method == "Paste Manually":
        log_content = st.text_area("Paste", height=180,
            placeholder="[ERROR] NullPointerException at line 42...",
            label_visibility="collapsed")

with col_right:
    st.markdown("""
    <div class="action-card">
        <div class="card-title">⚡ What The Agent Does</div>
        <div class="checklist-item">
            <div class="check-icon" style="border-color:#f0c040; background:#fff3cd; color:#9a6f00;">🔍</div>
            Detect the most critical error
        </div>
        <div class="checklist-item">
            <div class="check-icon" style="border-color:#fb923c; background:#ffedd5; color:#c2410c;">⚠️</div>
            Assign severity + responsible team
        </div>
        <div class="checklist-item">
            <div class="check-icon" style="border-color:#60a5fa; background:#dbeafe; color:#1d4ed8;">🌐</div>
            Search web for real fixes
        </div>
        <div class="checklist-item">
            <div class="check-icon" style="border-color:#a78bfa; background:#ede9fe; color:#6d28d9;">🔁</div>
            Self-correct if confidence is low
        </div>
        <div class="checklist-item">
            <div class="check-icon" style="border-color:#34d399; background:#d1fae5; color:#065f46;">📝</div>
            File GitHub Issue automatically
        </div>
    </div>
    <br/>
    """, unsafe_allow_html=True)
    run_btn = st.button("⚡  Run Incident Resolver", use_container_width=True)

# ── Results ──
if run_btn:
    if not log_content.strip():
        st.error("Please provide a log file first!")
    else:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">🤖 Agent Running</div>', unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_box = st.empty()

        status_box.markdown('<div class="status-txt">✏️ Initializing agents...</div>', unsafe_allow_html=True)
        time.sleep(0.3)
        progress_bar.progress(10)

        status_box.markdown('<div class="status-txt">🔍 Log Analyzer Agent scanning errors...</div>', unsafe_allow_html=True)
        progress_bar.progress(25)

        try:
            results = run_incident_resolver(log_content)

            progress_bar.progress(65)
            status_box.markdown('<div class="status-txt">🌐 Web Search Agent fetching fixes...</div>', unsafe_allow_html=True)
            time.sleep(0.4)

            progress_bar.progress(85)
            status_box.markdown('<div class="status-txt">📝 Filing GitHub Issue...</div>', unsafe_allow_html=True)
            time.sleep(0.3)

            progress_bar.progress(100)
            status_box.markdown('<div class="status-txt">✅ All agents completed!</div>', unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)

            log_data = results.get("log_analysis", {})
            fix_data  = results.get("fix", {})
            severity   = log_data.get("severity", "High")
            confidence = fix_data.get("confidence", "Medium")

            sev_class  = "sev-critical" if severity=="Critical" else "sev-high" if severity=="High" else "sev-low"
            conf_w     = "90%" if confidence=="High" else "60%" if confidence=="Medium" else "30%"
            conf_color = "#34d399" if confidence=="High" else "#f59e0b" if confidence=="Medium" else "#ef4444"

            if results.get("self_correction"):
                st.markdown("""
                <div class="self-fix-banner">
                    🔁 Self-correction triggered — Agent retried with a smarter search and found a better fix!
                </div>""", unsafe_allow_html=True)

            r1, r2 = st.columns(2, gap="medium")

            with r1:
                st.markdown(f"""
                <div class="res-card">
                    <div class="res-card-title">🔍 Log Analysis</div>
                    <div style="margin-bottom:1rem;">
                        <span class="sev-badge {sev_class}">● {severity}</span>
                    </div>
                    <div class="field-label">Error Detected</div>
                    <div class="field-value" style="font-family:Courier New,monospace; color:#dc2626; font-size:12px;">{log_data.get('error','N/A')}</div>
                    <div class="field-label">Source File</div>
                    <div class="field-value" style="font-family:Courier New,monospace; color:#059669; font-size:12px;">{log_data.get('file','N/A')}</div>
                    <div class="field-label">Summary</div>
                    <div class="field-value">{log_data.get('summary','N/A')}</div>
                    <div class="field-label">Assign To</div>
                    <div style="margin-top:4px;"><span class="role-badge">{log_data.get('role','N/A')} Team</span></div>
                </div>""", unsafe_allow_html=True)

            with r2:
                steps_raw = fix_data.get("steps","")
                steps_html = ""
                for i, line in enumerate([l for l in steps_raw.split("\n") if l.strip()], 1):
                    clean = line.lstrip("0123456789.-) ").strip()
                    if clean:
                        steps_html += f'<div class="fix-step-row"><div class="step-num">{i}</div><div class="step-txt">{clean}</div></div>'

                st.markdown(f"""
                <div class="res-card">
                    <div class="res-card-title">🛠 Proposed Fix</div>
                    <div class="field-label">Primary Fix</div>
                    <div class="field-value" style="color:#059669;">{fix_data.get('fix1','N/A')}</div>
                    <div class="field-label">Backup Fix</div>
                    <div class="field-value">{fix_data.get('fix2','N/A')}</div>
                    <div class="field-label">Confidence</div>
                    <div style="margin-bottom:1rem;">
                        <div style="font-size:12px;font-weight:800;color:{conf_color};margin-bottom:4px;">{confidence}</div>
                        <div class="conf-bar-bg">
                            <div class="conf-bar-fill" style="width:{conf_w};background:{conf_color};"></div>
                        </div>
                    </div>
                    <div class="field-label">Steps to Fix</div>
                    <div style="margin-top:6px;">{steps_html if steps_html else '<div style="color:#9ca3af;font-size:12px;">No steps extracted</div>'}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)
            github_result = results.get("github_issue","")
            if "✅" in github_result or "github.com" in github_result.lower():
                url = next((w for w in github_result.split() if "github.com" in w), github_result)
                st.markdown(f"""
                <div class="github-box">
                    <div class="github-circle">✓</div>
                    <div>
                        <div style="font-size:11px;font-weight:800;color:#15803d;text-transform:uppercase;letter-spacing:1px;font-family:'Architects Daughter',cursive;">GitHub Issue Created!</div>
                        <div style="font-size:13px;font-weight:700;color:#166534;font-family:Courier New,monospace;margin-top:3px;">{url}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.error(f"GitHub Issue Error: {github_result}")

        except Exception as e:
            progress_bar.progress(0)
            status_box.markdown(f'<div class="status-txt" style="color:#ef4444;">✗ Error: {str(e)}</div>', unsafe_allow_html=True)
            st.error(str(e))

st.markdown("""
<div class="footer-txt">
    DevOps Incident Resolver · Built with CrewAI · Powered by Groq ✏️
</div>""", unsafe_allow_html=True)