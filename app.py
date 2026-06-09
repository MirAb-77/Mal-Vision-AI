import streamlit as st
import importlib
import time

st.set_page_config(
    page_title="MalwareVision AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Session State ─────────────────────────────────────────────────────────────
if "logged_in"       not in st.session_state: st.session_state.logged_in       = False
if "user"            not in st.session_state: st.session_state.user             = ""
if "show_login"      not in st.session_state: st.session_state.show_login       = False
if "page"            not in st.session_state: st.session_state.page             = "Home"

SHOW_SIDEBAR = st.session_state.get("logged_in", False)

if not SHOW_SIDEBAR:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
from utils.theme import inject_css
inject_css()

# ── Hide Streamlit default nav/sidebar flicker before custom UI loads ─────────
st.markdown("""
<style>
/* Hide default Streamlit MPA nav links instantly on load */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] > div:first-child > div:first-child ul,
.st-emotion-cache-pbk9r8,
.st-emotion-cache-1cypcdb,
nav[data-testid="stSidebarNav"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}
/* Prevent sidebar flash — keep bg solid on first paint */
[data-testid="stSidebar"] {
    background: #030D1A !important;
}
/* Hide the auto-generated page links at top of sidebar */
[data-testid="stSidebarNavLink"],
[data-testid="collapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS  (keyframes + shared classes used everywhere)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

/* ── keyframes ── */
@keyframes glowPulse   {0%,100%{box-shadow:0 0 8px rgba(0,255,209,0.35)}50%{box-shadow:0 0 28px rgba(0,255,209,0.9),0 0 50px rgba(0,255,209,0.3)}}
@keyframes greenPulse  {0%,100%{box-shadow:0 0 6px rgba(0,255,209,0.3),0 0 12px rgba(0,200,150,0.15)}50%{box-shadow:0 0 20px rgba(0,255,209,0.75),0 0 40px rgba(0,200,150,0.3)}}
@keyframes borderGlow  {0%,100%{border-color:rgba(0,255,209,0.2)}50%{border-color:rgba(0,255,209,0.65)}}
@keyframes fadeSlideUp {from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes rotate360   {from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes scanAcross  {0%{left:-100%}100%{left:150%}}
@keyframes blinkDot    {0%,100%{opacity:1}50%{opacity:0.25}}
@keyframes hintBlink   {0%,100%{opacity:0.4}50%{opacity:1}}
@keyframes bounceArrow {0%,100%{transform:translateY(0)}50%{transform:translateY(7px)}}
@keyframes wbStrip     {0%{left:-100%}100%{left:150%}}
@keyframes shPulse     {0%,100%{box-shadow:0 0 0 0 rgba(0,255,209,0.25)}50%{box-shadow:0 0 0 10px rgba(0,255,209,0)}}
@keyframes glitchMove  {0%{transform:translate(0)}20%{transform:translate(-3px,2px)}40%{transform:translate(3px,-2px)}60%{transform:translate(-2px,1px)}80%{transform:translate(2px,1px)}100%{transform:translate(0)}}
@keyframes cubeEntrance{from{opacity:0;transform:scale(0.4) rotateY(180deg)}to{opacity:1;transform:scale(1) rotateY(0deg)}}

/* ── glitch overlay ── */
.glitch-screen{position:fixed;top:0;left:0;width:100%;height:100%;background:#000;z-index:99999;display:flex;align-items:center;justify-content:center;}
.glitch-text{font-family:'Orbitron',monospace;font-size:28px;color:#00FFD1;letter-spacing:6px;text-transform:uppercase;text-shadow:2px 0 red,-2px 0 cyan,0 0 20px #00FFD1;animation:glitchMove 0.25s infinite;}

/* ── app background ── */
.stApp{
  background:#020b18 !important;
  background-image:
    radial-gradient(ellipse 80% 40% at 50% 0%,rgba(0,255,180,0.055) 0%,transparent 70%),
    radial-gradient(ellipse 50% 35% at 0% 100%,rgba(0,200,150,0.04) 0%,transparent 60%),
    linear-gradient(rgba(0,255,209,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,255,209,0.03) 1px,transparent 1px) !important;
  background-size:100% 100%,100% 100%,40px 40px,40px 40px !important;
}

/* ── sidebar ── */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,rgba(0,10,22,0.98) 0%,rgba(0,6,18,0.98) 100%) !important;
  border-right:1px solid rgba(0,255,209,0.12) !important;
  box-shadow:3px 0 25px rgba(0,200,150,0.07) !important;
}

/* ── sidebar nav buttons ── */
[data-testid="stSidebar"] .stButton>button{
  background:transparent !important;
  border:1px solid rgba(0,255,209,0.08) !important;
  border-radius:3px !important;
  color:rgba(180,230,210,0.55) !important;
  font-family:'Share Tech Mono',monospace !important;
  font-size:11px !important;letter-spacing:2px !important;
  transition:all 0.25s ease !important;
}
[data-testid="stSidebar"] .stButton>button:hover{
  background:rgba(0,255,209,0.06) !important;
  border-color:rgba(0,255,209,0.4) !important;
  color:#00FFD1 !important;
  box-shadow:0 0 12px rgba(0,255,209,0.18),inset 0 0 8px rgba(0,200,150,0.05) !important;
  text-shadow:0 0 8px rgba(0,255,209,0.6) !important;
}

/* ── active nav ── */
.nav-active>button{
  background:rgba(0,255,209,0.08) !important;
  border-left:3px solid #00FFD1 !important;
  border-color:rgba(0,255,209,0.25) !important;
  color:#00FFD1 !important;
  box-shadow:0 0 14px rgba(0,255,209,0.18),inset 0 0 10px rgba(0,200,150,0.06) !important;
  text-shadow:0 0 10px rgba(0,255,209,0.65) !important;
}

/* ── main buttons ── */
.stButton>button{
  background:transparent !important;
  border:1px solid rgba(0,255,209,0.35) !important;
  border-radius:2px !important;
  color:#00FFD1 !important;
  font-family:'Orbitron',monospace !important;
  font-size:11px !important;letter-spacing:4px !important;
  transition:all 0.3s ease !important;
  position:relative !important;overflow:hidden !important;
}
.stButton>button:hover{
  border-color:rgba(0,255,209,0.85) !important;
  color:#fff !important;
  box-shadow:0 0 20px rgba(0,255,209,0.35),0 0 40px rgba(0,200,150,0.15) !important;
  text-shadow:0 0 12px rgba(0,255,209,0.9) !important;
}

/* ── inputs ── */
.stTextInput input,.stTextArea textarea{
  background:rgba(0,255,209,0.03) !important;
  border:1px solid rgba(0,255,209,0.14) !important;
  border-radius:2px !important;
  color:rgba(200,245,230,0.9) !important;
  font-family:'Share Tech Mono',monospace !important;
  letter-spacing:1px !important;
  transition:all 0.25s ease !important;
}
.stTextInput input:focus,.stTextArea textarea:focus{
  border-color:rgba(0,255,209,0.55) !important;
  box-shadow:0 0 0 1px rgba(0,255,209,0.18),0 0 14px rgba(0,200,150,0.18) !important;
  background:rgba(0,255,209,0.05) !important;
}

/* ── metrics ── */
[data-testid="stMetricValue"]{font-size:32px !important;color:#00FFD1 !important;text-shadow:0 0 20px rgba(0,255,209,0.55),0 0 40px rgba(0,200,150,0.2) !important;}
[data-testid="stMetricLabel"]{color:rgba(0,255,209,0.5) !important;letter-spacing:2px !important;}

/* ── spinner ── */
.spinner-ring{display:inline-block;width:16px;height:16px;border:2px solid rgba(0,255,209,0.2);border-top-color:#00FFD1;border-radius:50%;animation:rotate360 0.8s linear infinite;vertical-align:middle;margin-right:8px;}

/* ── widget cards ── */
.widget-card{
  background:rgba(2,12,25,0.88);
  border:1px solid rgba(0,255,209,0.1);
  border-radius:6px;padding:20px;
  animation:fadeSlideUp 0.5s ease both;
  transition:border-color 0.3s,box-shadow 0.3s;
  position:relative;overflow:hidden;
}
.widget-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(0,255,209,0.35),transparent);}
.widget-card:hover{border-color:rgba(0,255,209,0.35) !important;box-shadow:0 0 20px rgba(0,200,150,0.12),0 0 40px rgba(0,150,100,0.06) !important;}

/* ── tabs ── */
[data-testid="stTabs"] [role="tab"]{font-family:'Share Tech Mono',monospace !important;font-size:11px !important;letter-spacing:3px !important;text-transform:uppercase !important;color:rgba(200,230,215,0.4) !important;transition:all 0.25s !important;}
[data-testid="stTabs"] [role="tab"]:hover{color:#00FFD1 !important;text-shadow:0 0 8px rgba(0,255,209,0.5) !important;}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{color:#00FFD1 !important;border-bottom:2px solid #00FFD1 !important;text-shadow:0 0 10px rgba(0,255,209,0.65) !important;}

/* ── scrollbar ── */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:rgba(0,5,15,0.8);}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#00FFD1,#00a878);border-radius:2px;box-shadow:0 0 6px rgba(0,255,209,0.4);}

/* ── file uploader ── */
[data-testid="stFileUploader"]{border:1px dashed rgba(0,255,209,0.2) !important;border-radius:4px !important;background:rgba(0,255,209,0.02) !important;transition:all 0.3s !important;}
[data-testid="stFileUploader"]:hover{border-color:rgba(0,255,209,0.45) !important;box-shadow:0 0 14px rgba(0,200,150,0.12) !important;}

/* ── hide streamlit chrome ── */
#MainMenu{visibility:hidden}footer{visibility:hidden}header{visibility:hidden}
[data-testid="stSidebarNav"]{display:none !important;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  STAGE 1 — 3D CUBE INTRO
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in and not st.session_state.show_login:

    st.markdown("""<style>
    /* hide all streamlit padding so cube is full-screen */
    .block-container{padding:0 !important;max-width:100% !important;}
    </style>""", unsafe_allow_html=True)

    st.markdown("""
<style>
.cube-page{
  min-height:90vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:32px;
  font-family:'Share Tech Mono',monospace;
}
/* top scan line across full viewport */
.top-scanline{
  position:fixed;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(0,255,209,0.7),rgba(0,200,150,0.5),transparent);
  animation:scanAcross 3s ease-in-out infinite;
  pointer-events:none;z-index:9999;
}
/* corner brackets */
.corner{position:fixed;width:20px;height:20px;}
.c-tl{top:16px;left:16px;border-top:2px solid rgba(0,255,209,0.5);border-left:2px solid rgba(0,255,209,0.5);}
.c-tr{top:16px;right:16px;border-top:2px solid rgba(0,255,209,0.5);border-right:2px solid rgba(0,255,209,0.5);}
.c-bl{bottom:16px;left:16px;border-bottom:2px solid rgba(0,255,209,0.5);border-left:2px solid rgba(0,255,209,0.5);}
.c-br{bottom:16px;right:16px;border-bottom:2px solid rgba(0,255,209,0.5);border-right:2px solid rgba(0,255,209,0.5);}

/* brand */
.cube-brand h1{
  font-family:'Orbitron',monospace;font-size:26px;font-weight:900;
  letter-spacing:6px;text-align:center;
  background:linear-gradient(90deg,#00FFD1,#00e0aa,#00FFD1);
  background-size:200%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:shimmer 3s linear infinite;
  filter:drop-shadow(0 0 8px rgba(0,255,209,0.4));
}
@keyframes shimmer{0%{background-position:0%}100%{background-position:200%}}
.cube-brand h1 span{-webkit-text-fill-color:#ff003c;filter:none;}
.cube-brand p{font-size:9px;letter-spacing:5px;color:rgba(0,255,209,0.4);text-align:center;margin-top:6px;}

/* 3D scene */
.scene{
  width:180px;height:180px;perspective:700px;cursor:pointer;
  animation:cubeEntrance 0.8s cubic-bezier(0.34,1.56,0.64,1) both;
}
.cube{
  width:100%;height:100%;position:relative;
  transform-style:preserve-3d;
  animation:spinSlow 10s linear infinite;
  transition:animation 0.3s;
}
.scene:hover .cube{animation:spinFast 2s linear infinite;}
@keyframes spinSlow{from{transform:rotateX(18deg) rotateY(0deg)}to{transform:rotateX(18deg) rotateY(360deg)}}
@keyframes spinFast{from{transform:rotateX(22deg) rotateY(0deg)}to{transform:rotateX(22deg) rotateY(360deg)}}

.face{
  position:absolute;width:180px;height:180px;
  border:1px solid rgba(0,255,209,0.2);
  background:rgba(1,10,22,0.8);
  display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(2px);
}
.face.front {transform:translateZ(90px);
  background:rgba(0,255,209,0.05);
  border-color:rgba(0,255,209,0.6);
  box-shadow:0 0 40px rgba(0,255,209,0.25) inset,0 0 60px rgba(0,255,209,0.15);}
.face.back  {transform:rotateY(180deg) translateZ(90px);}
.face.left  {transform:rotateY(-90deg) translateZ(90px);}
.face.right {transform:rotateY(90deg)  translateZ(90px);}
.face.top   {transform:rotateX(90deg)  translateZ(90px);}
.face.bot   {transform:rotateX(-90deg) translateZ(90px);}

.face-logo{font-size:58px;line-height:1;filter:drop-shadow(0 0 12px rgba(0,255,209,0.5));}
.face-txt{
  font-family:'Orbitron',monospace;font-size:10px;font-weight:900;
  letter-spacing:3px;text-align:center;padding:10px;line-height:1.6;
  background:linear-gradient(135deg,#00FFD1,#00c090);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.face-txt span{display:block;-webkit-text-fill-color:#ff003c;}
.face-sm{font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:rgba(0,255,209,0.5);text-align:center;}

/* pulse ring around cube */
.cube-ring{
  position:absolute;width:220px;height:220px;
  border-radius:50%;border:1px solid rgba(0,255,209,0.08);
  animation:greenPulse 3s ease-in-out infinite;
  pointer-events:none;
}
.cube-ring2{
  position:absolute;width:260px;height:260px;
  border-radius:50%;border:1px solid rgba(0,255,209,0.04);
  animation:greenPulse 3s ease-in-out infinite 0.8s;
  pointer-events:none;
}

/* hint */
.hint-txt{font-size:10px;letter-spacing:5px;color:rgba(0,255,209,0.45);text-align:center;animation:hintBlink 2s ease-in-out infinite;}
.hint-arrow{font-size:22px;color:rgba(0,255,209,0.3);text-align:center;animation:bounceArrow 1.5s ease-in-out infinite;margin-top:4px;}

/* particles strip */
.particle-strip{
  position:fixed;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(0,255,209,0.3),transparent);
}
</style>

<div class="top-scanline"></div>
<div class="particle-strip"></div>
<div class="corner c-tl"></div><div class="corner c-tr"></div>
<div class="corner c-bl"></div><div class="corner c-br"></div>

<div class="cube-page">
  <div class="cube-brand">
    <h1>MALWARE<span>VISION</span> AI</h1>
    <p>ADVANCED CYBER THREAT INTELLIGENCE SYSTEM</p>
  </div>

  <div style="position:relative;display:flex;align-items:center;justify-content:center;">
    <div class="cube-ring"></div>
    <div class="cube-ring2"></div>
    <div class="scene">
      <div class="cube">
        <div class="face front"><div class="face-logo">🛡️</div></div>
        <div class="face back" ><div class="face-txt">MALWARE<span>VISION</span><br>AI</div></div>
        <div class="face left" ><div class="face-sm">THREAT<br>INTEL</div></div>
        <div class="face right"><div class="face-sm">AI<br>CORE</div></div>
        <div class="face top"  ><div class="face-sm">v3.1.0</div></div>
        <div class="face bot"  ><div class="face-sm">SEC</div></div>
      </div>
    </div>
  </div>

  <div>
    <div class="hint-txt">// CLICK BELOW TO INITIALIZE SYSTEM //</div>
    <div class="hint-arrow">↓</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Streamlit button acts as the cube click (HTML clicks can't trigger rerun)
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        if st.button("⬡  INITIALIZE", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  STAGE 2 — LOGIN FORM
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    st.markdown("""<style>
    .block-container{padding-top:40px !important;}
    </style>""", unsafe_allow_html=True)

    st.markdown("""
<style>
/* full-page green ambient */
.stApp{
  background-image:
    radial-gradient(ellipse 70% 50% at 50% 0%,rgba(0,255,209,0.07) 0%,transparent 65%),
    radial-gradient(ellipse 50% 40% at 100% 100%,rgba(0,200,150,0.05) 0%,transparent 60%),
    linear-gradient(rgba(0,255,209,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,255,209,0.03) 1px,transparent 1px) !important;
  background-size:100% 100%,100% 100%,40px 40px,40px 40px !important;
}
/* top neon edge */
.stApp::before{
  content:'';position:fixed;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(0,255,209,0.8),rgba(0,220,180,0.5),transparent);
  pointer-events:none;z-index:9999;
}

/* login card */
.login-card{
  max-width:480px;margin:0 auto;padding:44px 40px 36px;
  background:rgba(0,8,20,0.93);
  border:1px solid rgba(0,255,209,0.22);
  border-radius:4px;position:relative;
  box-shadow:0 0 30px rgba(0,200,150,0.1),0 0 70px rgba(0,150,100,0.05),inset 0 0 20px rgba(0,200,150,0.03);
  animation:fadeSlideUp 0.5s ease both;
}
.login-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(0,255,209,0.8),rgba(0,220,180,0.5),transparent);
}
.login-card::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(0,200,150,0.25),transparent);
}
/* card corner brackets */
.lc-tl,.lc-br{position:absolute;width:14px;height:14px;}
.lc-tl{top:0;left:0;border-top:2px solid rgba(0,255,209,0.6);border-left:2px solid rgba(0,255,209,0.6);}
.lc-br{bottom:0;right:0;border-bottom:2px solid rgba(0,255,209,0.6);border-right:2px solid rgba(0,255,209,0.6);}

/* scan sweep on card */
.lc-scan{
  position:absolute;top:0;left:-100%;width:60%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(0,255,209,0.04),transparent);
  animation:scanAcross 4s ease-in-out infinite;pointer-events:none;
}

/* shield */
.lc-logo{
  width:68px;height:68px;border-radius:50%;margin:0 auto 16px;
  background:rgba(0,255,209,0.05);border:1px solid rgba(0,255,209,0.28);
  display:flex;align-items:center;justify-content:center;font-size:30px;
  animation:glowPulse 2.5s ease-in-out infinite;
  filter:drop-shadow(0 0 8px rgba(0,255,209,0.3));
}
/* brand */
.lc-name{
  font-family:'Orbitron',monospace;font-size:20px;font-weight:900;letter-spacing:4px;
  text-align:center;
  background:linear-gradient(90deg,#00FFD1,#00c090,#00FFD1);
  background-size:200%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:shimmer 3s linear infinite;
  filter:drop-shadow(0 0 6px rgba(0,255,209,0.35));
}
.lc-name span{-webkit-text-fill-color:#ff003c;filter:none;}
.lc-tag{font-size:8px;letter-spacing:5px;color:rgba(0,255,209,0.4);text-align:center;margin-top:6px;text-shadow:0 0 8px rgba(0,200,150,0.3);}
.lc-status{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:10px;margin-bottom:26px;}
.lc-dot{width:7px;height:7px;border-radius:50%;background:#00FFD1;box-shadow:0 0 10px #00FFD1,0 0 20px rgba(0,255,209,0.4);animation:blinkDot 1.5s ease-in-out infinite;display:inline-block;}
.lc-stxt{font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:3px;color:#00FFD1;text-shadow:0 0 8px rgba(0,255,209,0.5);}

/* divider */
.lc-div{display:flex;align-items:center;gap:10px;margin-bottom:22px;}
.lc-divl{flex:1;height:1px;background:rgba(0,255,209,0.12);}
.lc-divt{font-size:9px;letter-spacing:3px;color:rgba(0,255,209,0.3);}

/* credit */
.lc-credit{font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:3px;color:rgba(100,180,160,0.25);text-align:center;margin-top:22px;border-top:1px solid rgba(0,255,209,0.07);padding-top:16px;}
.lc-credit span{color:rgba(0,255,209,0.4);text-shadow:0 0 8px rgba(0,200,150,0.2);}

/* input label override */
.stTextInput label{color:rgba(0,255,209,0.5) !important;font-family:'Share Tech Mono',monospace !important;font-size:9px !important;letter-spacing:3px !important;}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="login-card">
  <div class="lc-scan"></div>
  <div class="lc-tl"></div><div class="lc-br"></div>
  <div class="lc-logo">🛡️</div>
  <div class="lc-name">MALWARE<span>VISION</span> AI</div>
  <div class="lc-tag">ADVANCED CYBER THREAT INTELLIGENCE SYSTEM</div>
  <div class="lc-status"><span class="lc-dot"></span><span class="lc-stxt">SYSTEM ONLINE // CLASSIFIED</span></div>
  <div class="lc-div"><div class="lc-divl"></div><div class="lc-divt">// AUTHENTICATE</div><div class="lc-divl"></div></div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("PROJECT ID / USERNAME", placeholder="ENTER IDENTIFIER")
        password = st.text_input("PASSWORD / ACCESS KEY", type="password", placeholder="ENTER ACCESS KEY")

        if st.button("⬡  ACCESS SYSTEM", use_container_width=True):
            if username == "admin" and password == "1234":
                # ⚡ GLITCH TRANSITION
                glitch_ph = st.empty()
                glitch_ph.markdown("""
                <div class="glitch-screen">
                  <div class="glitch-text">ACCESS GRANTED // SYSTEM BREACH SUCCESS</div>
                </div>""", unsafe_allow_html=True)
                time.sleep(2.5)
                glitch_ph.empty()
                st.session_state.logged_in  = True
                st.session_state.user       = username
                st.session_state.page       = "Home"
                st.session_state.show_login = False
                st.rerun()
            else:
                st.error("⚠ ACCESS DENIED — INVALID CREDENTIALS")

    st.markdown("""<div class="lc-credit">DESIGNED BY <span>ABDULLAH IMRAN</span> // 2026</div>""", unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  STAGE 3 — AUTHENTICATED APP
# ══════════════════════════════════════════════════════════════════════════════

# ── Welcome Banner ────────────────────────────────────────────────────────────
from datetime import datetime
now = datetime.now().strftime("%H:%M:%S")

st.markdown(f"""
<style>
.wb-banner{{
  position:relative;overflow:hidden;
  background:rgba(0,8,20,0.96);
  border:1px solid rgba(0,255,209,0.18);
  border-radius:6px;padding:22px 28px;
  display:flex;align-items:center;justify-content:space-between;
  gap:20px;flex-wrap:wrap;margin-bottom:15px;
  font-family:'Share Tech Mono',monospace;
  box-shadow:0 0 20px rgba(0,200,150,0.08),0 0 50px rgba(0,150,100,0.04);
}}
.wb-banner::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(0,255,209,0.7),rgba(0,200,150,0.4),transparent);}}
.wb-banner::after {{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(0,200,150,0.18),transparent);}}
.wb-scan{{position:absolute;top:0;left:-100%;width:60%;height:100%;background:linear-gradient(90deg,transparent,rgba(0,255,209,0.04),transparent);animation:wbStrip 4s ease-in-out infinite;pointer-events:none;}}
.wb-ctl{{top:0;left:0;position:absolute;width:12px;height:12px;border-top:2px solid rgba(0,255,209,0.55);border-left:2px solid rgba(0,255,209,0.55);}}
.wb-cbr{{bottom:0;right:0;position:absolute;width:12px;height:12px;border-bottom:2px solid rgba(0,255,209,0.55);border-right:2px solid rgba(0,255,209,0.55);}}
.wb-left{{display:flex;align-items:center;gap:18px;}}
.wb-shield{{width:52px;height:52px;border-radius:50%;flex-shrink:0;border:1px solid rgba(0,255,209,0.28);background:rgba(0,255,209,0.05);display:flex;align-items:center;justify-content:center;font-size:22px;animation:shPulse 2.5s ease-in-out infinite;position:relative;}}
.wb-check{{position:absolute;bottom:-1px;right:-1px;width:14px;height:14px;border-radius:50%;background:#00FFD1;border:2px solid #020b18;font-size:8px;color:#020b18;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 0 8px rgba(0,255,209,0.6);}}
.wb-h2{{font-family:'Orbitron',monospace;font-size:14px;font-weight:900;letter-spacing:3px;color:#00FFD1;margin-bottom:4px;text-shadow:0 0 12px rgba(0,255,209,0.5);}}
.wb-user{{font-size:12px;letter-spacing:2px;color:rgba(200,245,230,0.85);margin-bottom:3px;}}
.wb-sub{{font-size:9px;letter-spacing:3px;color:rgba(0,255,209,0.4);}}
.wb-right{{display:flex;flex-direction:column;align-items:flex-end;gap:7px;}}
.wb-badge{{display:flex;align-items:center;gap:6px;background:rgba(0,255,209,0.04);border:1px solid rgba(0,255,209,0.11);border-radius:2px;padding:4px 10px;transition:border-color 0.3s,box-shadow 0.3s;}}
.wb-badge:hover{{border-color:rgba(0,255,209,0.35);box-shadow:0 0 10px rgba(0,200,150,0.12);}}
.wb-dot-g{{width:5px;height:5px;border-radius:50%;background:#00FFD1;box-shadow:0 0 6px #00FFD1;animation:blinkDot 2s ease-in-out infinite;}}
.wb-dot-r{{width:5px;height:5px;border-radius:50%;background:#ff003c;box-shadow:0 0 4px rgba(255,0,60,0.5);}}
.wb-bl{{font-size:9px;letter-spacing:2px;color:rgba(0,255,209,0.45);}}
.wb-bv{{font-size:9px;letter-spacing:1px;color:rgba(200,240,225,0.85);}}
.wb-time{{font-size:8px;letter-spacing:3px;color:rgba(0,255,209,0.28);text-align:right;}}
</style>

<div class="wb-banner">
  <div class="wb-scan"></div>
  <div class="wb-ctl"></div><div class="wb-cbr"></div>
  <div class="wb-left">
    <div class="wb-shield">🛡️<div class="wb-check">✓</div></div>
    <div>
      <div class="wb-h2">⬡ ACCESS GRANTED</div>
      <div class="wb-user">Welcome back, <b style="color:#fff;">{st.session_state.user}</b></div>
      <div class="wb-sub">// CYBER THREAT INTELLIGENCE PLATFORM ONLINE</div>
    </div>
  </div>
  <div class="wb-right">
    <div class="wb-badge"><div class="wb-dot-g"></div><span class="wb-bl">SYSTEM</span><span class="wb-bv">&nbsp;ONLINE</span></div>
    <div class="wb-badge"><div class="wb-dot-g"></div><span class="wb-bl">SESSION</span><span class="wb-bv">&nbsp;ACTIVE</span></div>
    <div class="wb-badge"><div class="wb-dot-r"></div><span class="wb-bl">THREATS</span><span class="wb-bv">&nbsp;1,247</span></div>
    <div class="wb-time">// {now} LOCAL</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<style>
@keyframes sideSweep{0%{top:-2px}100%{top:calc(100% + 2px)}}
.sb-sweep{position:absolute;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(0,255,209,0.5),transparent);
  animation:sideSweep 5s ease-in-out infinite;pointer-events:none;}
</style>
<div style="text-align:center;padding:24px 0 20px;position:relative;">
  <div class="sb-sweep"></div>
  <div style="font-family:'Orbitron',monospace;font-size:22px;font-weight:900;
              background:linear-gradient(90deg,#00FFD1,#00c090);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;letter-spacing:4px;line-height:1.1;
              filter:drop-shadow(0 0 6px rgba(0,255,209,0.4));">MALWARE</div>
  <div style="font-family:'Orbitron',monospace;font-size:22px;font-weight:900;
              color:#FF003C;text-shadow:0 0 20px rgba(255,0,60,0.6);
              letter-spacing:4px;line-height:1.1;">VISION AI</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:9px;
              color:rgba(0,255,209,0.28);letter-spacing:5px;margin-top:8px;">
    v3.1.0 // CLASSIFIED</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;">
    <div style="width:8px;height:8px;border-radius:50%;background:#00FFD1;
                box-shadow:0 0 12px #00FFD1,0 0 24px rgba(0,255,209,0.4);
                animation:glowPulse 1.5s ease infinite;"></div>
    <span style="font-family:'Share Tech Mono',monospace;font-size:10px;
                 color:#00FFD1;letter-spacing:3px;text-shadow:0 0 8px rgba(0,255,209,0.55);">SYSTEM ONLINE</span>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:rgba(0,255,209,0.04);border:1px solid rgba(0,255,209,0.1);
            border-radius:6px;padding:10px 12px;margin-bottom:16px;
            font-family:'Share Tech Mono',monospace;font-size:10px;
            color:rgba(0,255,209,0.35);letter-spacing:1px;line-height:1.8;">
  I Gotcha Ya :) <span style="color:#FF003C;"></span>
</div>
""", unsafe_allow_html=True)

    PAGES = [
        ("🏠  Home",               "Home"),
        ("🛡️  PE Detection",       "PE Detection"),
        ("👁️  Image Detection",    "Image Detection"),
        ("🔬  LIME Explainability", "LIME Explainability"),
        ("🌐  VirusTotal",          "VirusTotal"),
        ("📋  Report",              "Report"),
        ("🧠  Model Architecture",  "Model Architecture"),
    ]

    cur = st.session_state["page"]
    for label, key in PAGES:
        active = cur == key
        if active:
            st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state["page"] = key
            st.rerun()
        if active:
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.logged_in  = False
        st.session_state.user       = ""
        st.session_state.page       = "Home"
        st.session_state.show_login = False
        st.rerun()

    st.markdown("""
<div style="font-family:'Share Tech Mono',monospace;font-size:9px;
            color:rgba(0,255,209,0.18);letter-spacing:2px;
            text-align:center;padding:8px 0;line-height:2;">
  © 2026 CYBER SECURITY<br>RESEARCH PROJECT<br>
  <span style="color:rgba(0,255,209,0.3);">CLASSIFIED // TOP SECRET</span>
</div>
""", unsafe_allow_html=True)


# ── Route ─────────────────────────────────────────────────────────────────────
page = st.session_state["page"]

if   page == "Home":               import views._home              as mod
elif page == "PE Detection":       import views._pe_detection      as mod
elif page == "Image Detection":    import views._image_detection   as mod
elif page == "LIME Explainability":import views._lime_explainability as mod
elif page == "VirusTotal":         import views._virustotal        as mod
elif page == "Report":             import views._report            as mod
elif page == "Model Architecture": import views._model_architecture as mod
else:                              import views._home              as mod

importlib.reload(mod)
mod.render()
