import streamlit as st

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600;700&family=Orbitron:wght@400;700;900&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background-color: #020A14 !important;
    color: #C8E6FF !important;
}
.stApp {
    background: radial-gradient(ellipse at top, #0B1A2E, #020A14) !important;
}

/* SCANLINES */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #030D1A !important;
    border-right: 1px solid rgba(0,255,209,0.12) !important;
}
[data-testid="stSidebar"] * { color: #C8E6FF !important; }

/* ── HEADINGS ── */
h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: #00FFD1 !important;
    text-shadow: 0 0 20px rgba(0,255,209,0.4) !important;
    letter-spacing: 2px;
}
h4, h5, h6 {
    font-family: 'Rajdhani', sans-serif !important;
    color: #00B4FF !important;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: rgba(0,255,209,0.04) !important;
    border: 1px solid rgba(0,255,209,0.15) !important;
    border-radius: 8px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: rgba(200,230,255,0.5) !important; font-family: 'Share Tech Mono', monospace !important; font-size: 11px !important; letter-spacing: 3px !important; }
[data-testid="stMetricValue"] { color: #00FFD1 !important; font-family: 'Orbitron', monospace !important; font-size: 28px !important; text-shadow: 0 0 15px rgba(0,255,209,0.4) !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #00FFD1 !important;
    color: #00FFD1 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    transition: all 0.3s ease !important;
    clip-path: polygon(8px 0%, 100% 0%, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0% 100%, 0% 8px) !important;
}
.stButton > button:hover {
    background: rgba(0,255,209,0.1) !important;
    box-shadow: 0 0 25px rgba(0,255,209,0.3) !important;
    text-shadow: 0 0 8px rgba(0,255,209,0.8) !important;
}
.stButton > button[kind="primary"] {
    border-color: #FF003C !important;
    color: #FF003C !important;
}
.stButton > button[kind="primary"]:hover {
    background: rgba(255,0,60,0.1) !important;
    box-shadow: 0 0 25px rgba(255,0,60,0.3) !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(0,180,255,0.04) !important;
    border: 1px dashed rgba(0,180,255,0.3) !important;
    border-radius: 8px !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,255,209,0.15) !important;
}

/* ── INPUT FIELDS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid rgba(0,180,255,0.2) !important;
    border-radius: 4px !important;
    color: #C8E6FF !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── DIVIDER ── */
hr { border-color: rgba(0,255,209,0.1) !important; }

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: rgba(0,255,209,0.03) !important;
    border: 1px solid rgba(0,255,209,0.12) !important;
    border-radius: 8px !important;
}

/* ── ALERTS / INFO ── */
.stAlert { border-radius: 4px !important; border-left: 3px solid !important; }

/* ── CODE BLOCKS ── */
code, pre {
    background: #030D1A !important;
    color: #00FFD1 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border: 1px solid rgba(0,255,209,0.1) !important;
}

/* ── PROGRESS BAR ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #00FFD1, #00B4FF) !important;
}

/* ── CUSTOM COMPONENTS ── */
.cyber-card {
    background: rgba(0,255,209,0.03);
    border: 1px solid rgba(0,255,209,0.12);
    border-radius: 8px;
    padding: 24px;
    margin: 12px 0;
    position: relative;
}
.cyber-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00FFD1, transparent);
}
.cyber-card.red::before { background: linear-gradient(90deg, #FF003C, transparent); }
.cyber-card.blue::before { background: linear-gradient(90deg, #00B4FF, transparent); }
.cyber-card.purple::before { background: linear-gradient(90deg, #7B2FFF, transparent); }

.threat-badge {
    display: inline-block;
    padding: 4px 16px;
    border-radius: 2px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.badge-malicious { background: rgba(255,0,60,0.15); color: #FF003C; border: 1px solid rgba(255,0,60,0.3); }
.badge-benign    { background: rgba(0,255,209,0.1);  color: #00FFD1; border: 1px solid rgba(0,255,209,0.3); }
.badge-warn      { background: rgba(255,209,102,0.1);color: #FFD166; border: 1px solid rgba(255,209,102,0.3); }

.section-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 4px;
    color: #00FFD1;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(0,255,209,0.15);
    padding-bottom: 8px;
    margin-bottom: 20px;
}

.result-box {
    background: #020A14;
    border: 1px solid rgba(0,255,209,0.2);
    border-radius: 4px;
    padding: 24px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 14px;
    line-height: 2;
    margin: 16px 0;
}
.result-box.malicious { border-color: rgba(255,0,60,0.4); }
.result-box.benign    { border-color: rgba(0,255,209,0.4); }

.mono-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: rgba(200,230,255,0.4);
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)
