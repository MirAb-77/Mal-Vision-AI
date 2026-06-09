import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
<div style="text-align:center; padding: 20px 0 30px;">
    <div style="font-family:'Orbitron',monospace; font-size:20px; font-weight:900;
                color:#00FFD1; text-shadow:0 0 20px rgba(0,255,209,0.5);
                letter-spacing:3px;">MALWARE</div>
    <div style="font-family:'Orbitron',monospace; font-size:20px; font-weight:900;
                color:#FF003C; text-shadow:0 0 20px rgba(255,0,60,0.5);
                letter-spacing:3px;">VISION AI</div>
    <div style="font-family:'Share Tech Mono',monospace; font-size:10px;
                color:rgba(200,230,255,0.3); letter-spacing:4px; margin-top:6px;">
        v3.1.0 // ACTIVE
    </div>
    <div style="display:flex;align-items:center;justify-content:center;gap:8px;
                margin-top:12px;">
        <div style="width:7px;height:7px;border-radius:50%;background:#00FFD1;
                    animation:none;box-shadow:0 0 8px #00FFD1;"></div>
        <span style="font-family:'Share Tech Mono',monospace;font-size:10px;
                     color:#00FFD1;letter-spacing:3px;">SYSTEM ONLINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        pages = {
            "🏠  Home":               "Home",
            "🛡️  PE Detection":       "PE Detection",
            "👁️  Image Detection":    "Image Detection",
            "🔬  LIME Explainability": "LIME Explainability",
            "🌐  VirusTotal":          "VirusTotal",
            "📋  Report":              "Report",
            "🧠  Model Architecture":  "Model Architecture",
        }

        if "page" not in st.session_state:
            st.session_state.page = "Home"

        for label, key in pages.items():
            active = st.session_state.page == key
            if st.sidebar.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if active else "secondary"
            ):
                st.session_state.page = key
                st.rerun()

        st.markdown("---")
        st.markdown("""
<div style="font-family:'Share Tech Mono',monospace; font-size:10px;
            color:rgba(200,230,255,0.25); letter-spacing:2px;
            text-align:center; padding:12px 0;">
    © 2026 CYBER SECURITY<br>RESEARCH PROJECT
</div>
""", unsafe_allow_html=True)

    return st.session_state.get("page", "Home")
