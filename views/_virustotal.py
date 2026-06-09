import streamlit as st
import requests
import time
import hashlib
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime

VT_API_KEY = "509c7df9aa4f344368eb0a42734a5040c06cb39dbbe34b38f927c319606e0513"
VT_BASE    = "https://www.virustotal.com/api/v3"
HEADERS    = {"x-apikey": VT_API_KEY, "Accept": "application/json"}


def render():
    st.markdown('<h1>🌐 VIRUSTOTAL INTELLIGENCE</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-tag">// REAL-TIME THREAT INTELLIGENCE · 70+ AV ENGINES</div>',
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Analysis mode",
        ["🔗 Analyse URL", "🔍 Lookup Hash", "📂 Upload File"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("---")

    # ──────────────────────────────────────────────────────────────────────────
    if "URL" in mode:
        _url_mode()
    elif "Hash" in mode:
        _hash_mode()
    else:
        _file_mode()


# ── URL Analysis ──────────────────────────────────────────────────────────────
def _url_mode():
    st.markdown('<div class="section-tag">// URL THREAT SCAN</div>', unsafe_allow_html=True)
    url_input = st.text_input(
        "Enter URL to analyse",
        placeholder="https://suspicious-site.example.com/payload",
        label_visibility="collapsed",
    )

    if st.button("🌐 SCAN URL", use_container_width=True) and url_input:
        with st.spinner("Submitting URL to VirusTotal…"):
            try:
                # Submit
                r = requests.post(
                    f"{VT_BASE}/urls",
                    headers=HEADERS,
                    data={"url": url_input},
                    timeout=15,
                )
                r.raise_for_status()
                analysis_id = r.json()["data"]["id"]

                # Poll
                result = _poll_analysis(analysis_id)
                st.session_state["vt_result"] = result
                st.session_state["vt_target"] = url_input
            except Exception as e:
                st.error(f"VirusTotal API error: {e}")

    _show_result()


# ── Hash Lookup ───────────────────────────────────────────────────────────────
def _hash_mode():
    st.markdown('<div class="section-tag">// FILE HASH LOOKUP (MD5 / SHA1 / SHA256)</div>',
                unsafe_allow_html=True)

    examples = {
        "WannaCry (SHA256)":
            "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa",
        "Mimikatz (MD5)":
            "7c46f5bd2bb0f834da7d38917a6d4e77",
        "NotPetya (SHA256)":
            "027cc450ef5f8c5f653329641ec1fed91f694e0d229928963b30f6b0d7d3a745",
    }

    col1, col2 = st.columns([3, 1])
    with col1:
        hash_input = st.text_input(
            "File hash", placeholder="Enter MD5 / SHA1 / SHA256",
            label_visibility="collapsed"
        )
    with col2:
        preset = st.selectbox("Quick examples", ["— select —"] + list(examples.keys()),
                              label_visibility="collapsed")
        if preset != "— select —":
            hash_input = examples[preset]

    if st.button("🔍 LOOKUP HASH", use_container_width=True) and hash_input:
        with st.spinner(f"Looking up `{hash_input[:16]}…`"):
            try:
                r = requests.get(
                    f"{VT_BASE}/files/{hash_input.strip()}",
                    headers=HEADERS, timeout=15
                )
                if r.status_code == 404:
                    st.warning("Hash not found in VirusTotal database.")
                    return
                r.raise_for_status()
                data = r.json()
                st.session_state["vt_result"] = _parse_file_report(data)
                st.session_state["vt_target"] = hash_input.strip()
            except Exception as e:
                st.error(f"API error: {e}")

    _show_result()


# ── File Upload ───────────────────────────────────────────────────────────────
def _file_mode():
    st.markdown('<div class="section-tag">// SUBMIT FILE FOR SCANNING</div>',
                unsafe_allow_html=True)
    st.markdown("""
<div style="background:rgba(255,209,102,0.06);border:1px solid rgba(255,209,102,0.2);
            border-radius:6px;padding:12px;font-family:'Share Tech Mono',monospace;
            font-size:11px;color:rgba(255,209,102,0.8);letter-spacing:1px;margin-bottom:16px;">
⚠  Files are uploaded to VirusTotal's public cloud.
   Do NOT upload confidential or sensitive files.
   Max size: 32 MB (free tier).
</div>
""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop file", type=None, label_visibility="collapsed", key="vt_upload"
    )
    if uploaded and st.button("☁️ UPLOAD & SCAN", use_container_width=True):
        raw = uploaded.read()
        sha = hashlib.sha256(raw).hexdigest()
        st.markdown(f"**SHA256:** `{sha}`")

        with st.spinner("Uploading to VirusTotal…"):
            try:
                # Check if already known
                r = requests.get(f"{VT_BASE}/files/{sha}", headers=HEADERS, timeout=15)
                if r.status_code == 200:
                    st.info("File already in VT database — loading cached result.")
                    st.session_state["vt_result"] = _parse_file_report(r.json())
                else:
                    # Upload
                    r2 = requests.post(
                        f"{VT_BASE}/files",
                        headers={"x-apikey": VT_API_KEY},
                        files={"file": (uploaded.name, raw)},
                        timeout=60,
                    )
                    r2.raise_for_status()
                    analysis_id = r2.json()["data"]["id"]
                    result = _poll_analysis(analysis_id, max_wait=120)
                    st.session_state["vt_result"] = result
                st.session_state["vt_target"] = uploaded.name
            except Exception as e:
                st.error(f"Upload error: {e}")

    _show_result()


# ── Poll analysis ─────────────────────────────────────────────────────────────
def _poll_analysis(analysis_id, max_wait=60):
    waited = 0
    bar = st.progress(0, text="Waiting for analysis…")
    while waited < max_wait:
        r = requests.get(
            f"{VT_BASE}/analyses/{analysis_id}",
            headers=HEADERS, timeout=15
        )
        data = r.json()
        status = data.get("data", {}).get("attributes", {}).get("status","")
        bar.progress(min(waited / max_wait, 0.95), text=f"Status: {status}…")
        if status == "completed":
            bar.progress(1.0, text="Analysis complete ✅")
            return _parse_analysis_report(data)
        time.sleep(5); waited += 5
    raise TimeoutError("Analysis timed out")


# ── Parse helpers ─────────────────────────────────────────────────────────────
def _parse_analysis_report(data):
    attrs  = data["data"]["attributes"]
    stats  = attrs.get("stats", {})
    results= attrs.get("results", {})
    return {
        "malicious":   stats.get("malicious",   0),
        "suspicious":  stats.get("suspicious",  0),
        "undetected":  stats.get("undetected",  0),
        "harmless":    stats.get("harmless",    0),
        "total":       sum(stats.values()),
        "engines":     results,
        "type":        "analysis",
        "meta":        {},
    }

def _parse_file_report(data):
    attrs  = data["data"]["attributes"]
    stats  = attrs.get("last_analysis_stats", {})
    results= attrs.get("last_analysis_results", {})
    names  = attrs.get("meaningful_name", "Unknown")
    size   = attrs.get("size", 0)
    vhash  = attrs.get("sha256","")
    ftype  = attrs.get("type_description","")
    first  = attrs.get("first_submission_date", 0)
    last   = attrs.get("last_analysis_date", 0)
    return {
        "malicious":   stats.get("malicious",   0),
        "suspicious":  stats.get("suspicious",  0),
        "undetected":  stats.get("undetected",  0),
        "harmless":    stats.get("harmless",    0),
        "total":       sum(stats.values()),
        "engines":     results,
        "type":        "file",
        "meta": {
            "name": names, "size": size, "sha256": vhash,
            "file_type": ftype,
            "first_seen": datetime.utcfromtimestamp(first).strftime("%Y-%m-%d") if first else "N/A",
            "last_scan":  datetime.utcfromtimestamp(last).strftime("%Y-%m-%d")  if last  else "N/A",
        },
    }


# ── Display results ───────────────────────────────────────────────────────────
def _show_result():
    res = st.session_state.get("vt_result")
    if res is None:
        return

    target = st.session_state.get("vt_target","")
    mal    = res["malicious"]
    sus    = res["suspicious"]
    total  = res["total"]
    undet  = res["undetected"]
    harm   = res["harmless"]

    threat_pct = (mal + sus) / max(total, 1) * 100
    if mal == 0 and sus == 0:
        verdict, color, icon = "CLEAN", "#00FFD1", "✅"
    elif mal < 5:
        verdict, color, icon = "SUSPICIOUS", "#FFD166", "⚠️"
    else:
        verdict, color, icon = "MALICIOUS", "#FF003C", "☠️"

    st.markdown("---")
    st.markdown(f'<div class="section-tag">// SCAN RESULTS: {target[:60]}</div>',
                unsafe_allow_html=True)

    # Meta
    if res["meta"]:
        m = res["meta"]
        cols = st.columns(4)
        cols[0].metric("File Name",   m.get("name","N/A")[:20])
        cols[1].metric("File Type",   m.get("file_type","N/A"))
        cols[2].metric("First Seen",  m.get("first_seen","N/A"))
        cols[3].metric("Last Scan",   m.get("last_scan","N/A"))

    # Verdict banner
    st.markdown(f"""
<div style="background:rgba(0,0,0,0.4);border:2px solid {color};border-radius:10px;
            padding:28px;text-align:center;margin:20px 0;">
    <div style="font-size:48px;margin-bottom:8px;">{icon}</div>
    <div style="font-family:'Orbitron',monospace;font-size:36px;font-weight:900;
                color:{color};text-shadow:0 0 30px {color}88;letter-spacing:4px;">
        {verdict}
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:18px;
                color:rgba(200,230,255,0.7);margin-top:8px;">
        {mal} / {total} engines flagged as malicious
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:14px;
                color:rgba(200,230,255,0.4);margin-top:4px;">
        Threat score: {threat_pct:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Malicious",  mal,   delta=None)
    c2.metric("🟡 Suspicious", sus,   delta=None)
    c3.metric("✅ Undetected", undet, delta=None)
    c4.metric("💚 Harmless",   harm,  delta=None)

    # Charts
    col_pie, col_bar = st.columns(2)

    with col_pie:
        st.markdown("#### Engine Verdict Distribution")
        fig = go.Figure(go.Pie(
            labels=["Malicious","Suspicious","Undetected","Harmless"],
            values=[mal, sus, undet, harm],
            hole=0.55,
            marker_colors=["#FF003C","#FFD166","rgba(200,230,255,0.2)","#00FFD1"],
            textfont=dict(family="Share Tech Mono", size=11),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_color="#C8E6FF",
            legend=dict(font=dict(color="#C8E6FF")),
            height=320, margin=dict(t=20,b=10,l=10,r=10),
            annotations=[dict(
                text=f"<b>{mal}/{total}</b>",
                x=0.5, y=0.5, font_size=20,
                font_color=color, font_family="Orbitron",
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_bar:
        st.markdown("#### Top Flagging Engines")
        engines_df = [
            {"Engine": eng, "Result": v.get("result",""), "Category": v.get("category","")}
            for eng, v in res["engines"].items()
            if v.get("category") in ("malicious","suspicious")
        ][:20]
        if engines_df:
            cats   = [e["Category"] for e in engines_df]
            c_map  = {"malicious":"#FF003C","suspicious":"#FFD166"}
            colors = [c_map.get(c,"#C8E6FF") for c in cats]
            fig2 = go.Figure(go.Bar(
                x=[e["Engine"] for e in engines_df],
                y=[1]*len(engines_df),
                marker_color=colors,
                text=[e["Result"][:20] for e in engines_df],
                textposition="outside",
                textfont=dict(size=9, color="rgba(200,230,255,0.7)"),
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                font_color="#C8E6FF", height=320,
                xaxis=dict(tickangle=-45, tickfont=dict(size=10,family="Share Tech Mono")),
                yaxis=dict(visible=False),
                margin=dict(t=30,b=120,l=20,r=20),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.success("✅ No engines flagged this sample.")

    # Full engine table
    with st.expander("📋 Full Engine Results Table"):
        rows = [
            {"Engine": eng,
             "Category": v.get("category","N/A"),
             "Result": v.get("result") or "—",
             "Engine Version": v.get("engine_version","N/A"),
             "Updated": v.get("engine_update","N/A")}
            for eng, v in res["engines"].items()
        ]
        import pandas as pd
        df = pd.DataFrame(rows).sort_values("Category")

        def _color_cat(val):
            if val == "malicious":  return "color:#FF003C"
            if val == "suspicious": return "color:#FFD166"
            if val == "undetected": return "color:rgba(200,230,255,0.4)"
            return "color:#00FFD1"

        st.dataframe(df, use_container_width=True, height=400)

    # Save to report session
    st.session_state["report_vt"] = {
        "verdict": verdict, "mal": mal, "sus": sus,
        "total": total, "target": target,
    }
