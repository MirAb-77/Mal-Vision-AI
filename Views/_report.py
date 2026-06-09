import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import json, os


def render():
    st.markdown('<h1>📋 THREAT INTELLIGENCE REPORT</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-tag">// AUTO-GENERATED SECURITY ANALYSIS REPORT</div>',
        unsafe_allow_html=True,
    )

    # ── Gather data from session ───────────────────────────────────────────────
    pe_res  = st.session_state.get("pe_result")
    cnn_res = st.session_state.get("cnn_result")
    vt_res  = st.session_state.get("report_vt")
    ts      = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    has_data = any([pe_res, cnn_res, vt_res])

    if not has_data:
        st.markdown("""
<div style="background:rgba(0,180,255,0.05);border:1px solid rgba(0,180,255,0.2);
            border-radius:8px;padding:32px;text-align:center;">
    <div style="font-size:48px;margin-bottom:16px;">📋</div>
    <div style="font-family:'Orbitron',monospace;font-size:16px;color:#00B4FF;
                margin-bottom:8px;">NO ANALYSIS DATA YET</div>
    <div style="font-size:14px;color:rgba(200,230,255,0.5);line-height:1.8;">
        Run a PE detection, image detection, or VirusTotal scan first.<br>
        Results will be automatically collected and displayed here.
    </div>
</div>
""", unsafe_allow_html=True)
        return

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(0,255,209,0.06),rgba(0,180,255,0.04));
            border:1px solid rgba(0,255,209,0.15);border-radius:10px;
            padding:32px;margin-bottom:24px;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div>
            <div style="font-family:'Orbitron',monospace;font-size:22px;
                        font-weight:900;color:#fff;letter-spacing:3px;">
                MALWAREVISION AI
            </div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:12px;
                        color:#00FFD1;letter-spacing:4px;margin-top:4px;">
                THREAT INTELLIGENCE REPORT
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                        color:rgba(200,230,255,0.4);letter-spacing:2px;">
                Generated: {ts}
            </div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                        color:rgba(200,230,255,0.4);letter-spacing:2px;margin-top:4px;">
                Report ID: MVR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Executive Summary ─────────────────────────────────────────────────────
    st.markdown('<div class="section-tag">// EXECUTIVE SUMMARY</div>', unsafe_allow_html=True)

    pe_verdict  = pe_res["label"]  if pe_res  else "N/A"
    cnn_verdict = cnn_res["label"] if cnn_res else "N/A"
    vt_verdict  = vt_res["verdict"]if vt_res  else "N/A"

    verdicts = [v for v in [pe_verdict, cnn_verdict, vt_verdict]
                if v not in ("N/A",)]
    overall  = "MALICIOUS" if "Malicious" in verdicts or "MALICIOUS" in verdicts else \
               "SUSPICIOUS" if "SUSPICIOUS" in verdicts else "CLEAN"
    ov_color = "#FF003C" if overall == "MALICIOUS" else \
               "#FFD166" if overall == "SUSPICIOUS" else "#00FFD1"

    st.markdown(f"""
<div style="background:rgba(0,0,0,0.3);border:2px solid {ov_color};border-radius:10px;
            padding:24px;text-align:center;margin-bottom:24px;">
    <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                color:rgba(200,230,255,0.4);letter-spacing:4px;margin-bottom:8px;">
        OVERALL THREAT ASSESSMENT
    </div>
    <div style="font-family:'Orbitron',monospace;font-size:44px;font-weight:900;
                color:{ov_color};text-shadow:0 0 30px {ov_color}88;letter-spacing:6px;">
        {overall}
    </div>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    _verdict_card(c1, "🛡️ PE Model",   pe_verdict,
                  f"{pe_res['conf']*100:.2f}%" if pe_res else "—")
    _verdict_card(c2, "👁️ CNN Model",  cnn_verdict,
                  f"{cnn_res['conf']*100:.2f}%" if cnn_res else "—")
    _verdict_card(c3, "🌐 VirusTotal", vt_verdict,
                  f"{vt_res['mal']}/{vt_res['total']}" if vt_res else "—")

    # ── Confidence Radar ──────────────────────────────────────────────────────
    if pe_res or cnn_res:
        st.markdown("---")
        st.markdown('<div class="section-tag">// CONFIDENCE ANALYSIS</div>',
                    unsafe_allow_html=True)

        categories = ["PE Model\nConfidence","CNN Model\nConfidence",
                      "VT\nDetection","Overall\nRisk","Threat\nCertainty"]
        pe_conf  = pe_res["conf"]  if pe_res  else 0
        cnn_conf = cnn_res["conf"] if cnn_res else 0
        vt_conf  = vt_res["mal"]/max(vt_res["total"],1) if vt_res else 0
        overall_risk = (pe_conf + cnn_conf + vt_conf) / 3
        certainty    = min(pe_conf, cnn_conf) if (pe_res and cnn_res) else max(pe_conf,cnn_conf)

        vals = [pe_conf, cnn_conf, vt_conf, overall_risk, certainty]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[v*100 for v in vals] + [vals[0]*100],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(255,0,60,0.12)",
            line=dict(color="#FF003C", width=2),
            name="Threat Score",
        ))
        fig.add_trace(go.Scatterpolar(
            r=[50]*len(categories) + [50],
            theta=categories + [categories[0]],
            line=dict(color="rgba(200,230,255,0.1)", width=1, dash="dot"),
            name="Threshold (50%)",
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(range=[0,100], visible=True,
                                tickfont=dict(color="rgba(200,230,255,0.4)",size=9),
                                gridcolor="rgba(200,230,255,0.06)"),
                angularaxis=dict(tickfont=dict(color="rgba(200,230,255,0.6)",
                                               family="Share Tech Mono",size=10),
                                 gridcolor="rgba(200,230,255,0.06)"),
            ),
            paper_bgcolor="rgba(0,0,0,0)", font_color="#C8E6FF",
            legend=dict(font=dict(color="#C8E6FF")),
            height=380, margin=dict(t=20,b=20,l=20,r=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── PE Details ────────────────────────────────────────────────────────────
    if pe_res:
        st.markdown("---")
        st.markdown('<div class="section-tag">// PE STATIC ANALYSIS DETAILS</div>',
                    unsafe_allow_html=True)

        from utils.model_loader import PE_FEATURES
        import pandas as pd
        fv = pe_res["fv"]

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
<div class="cyber-card {'red' if pe_res['label']=='Malicious' else ''}">
    <div class="mono-label">VERDICT</div>
    <div style="font-family:'Orbitron',monospace;font-size:24px;font-weight:900;
                color:{'#FF003C' if pe_res['label']=='Malicious' else '#00FFD1'};">
        {pe_res['label'].upper()}
    </div>
    <div class="mono-label" style="margin-top:12px;">CONFIDENCE</div>
    <div style="font-family:'Orbitron',monospace;font-size:20px;color:#fff;">
        {pe_res['conf']*100:.2f}%
    </div>
</div>
""", unsafe_allow_html=True)

        with col_b:
            key_feats = {
                "SectionMaxEntropy": fv[PE_FEATURES.index("SectionMaxEntropy")],
                "SuspiciousImportFunctions": fv[PE_FEATURES.index("SuspiciousImportFunctions")],
                "NumberOfSections": fv[PE_FEATURES.index("NumberOfSections")],
                "CheckSum": fv[PE_FEATURES.index("CheckSum")],
                "DllCharacteristics": fv[PE_FEATURES.index("DllCharacteristics")],
            }
            for feat, val in key_feats.items():
                st.markdown(f"""
<div style="display:flex;justify-content:space-between;padding:6px 0;
            border-bottom:1px solid rgba(0,255,209,0.06);
            font-family:'Share Tech Mono',monospace;font-size:12px;">
    <span style="color:rgba(200,230,255,0.5);">{feat}</span>
    <span style="color:#00FFD1;">{val:.2f}</span>
</div>
""", unsafe_allow_html=True)

    # ── CNN Details ───────────────────────────────────────────────────────────
    if cnn_res:
        st.markdown("---")
        st.markdown('<div class="section-tag">// CNN IMAGE ANALYSIS DETAILS</div>',
                    unsafe_allow_html=True)
        col_x, col_y = st.columns(2)
        with col_x:
            st.markdown(f"""
<div class="cyber-card {'red' if cnn_res['label']=='Malicious' else ''}">
    <div class="mono-label">VERDICT</div>
    <div style="font-family:'Orbitron',monospace;font-size:24px;font-weight:900;
                color:{'#FF003C' if cnn_res['label']=='Malicious' else '#00FFD1'};">
        {cnn_res['label'].upper()}
    </div>
    <div class="mono-label" style="margin-top:12px;">CONFIDENCE</div>
    <div style="font-family:'Orbitron',monospace;font-size:20px;color:#fff;">
        {cnn_res['conf']*100:.2f}%
    </div>
    <div class="mono-label" style="margin-top:12px;">RAW SCORE</div>
    <div style="font-family:'Orbitron',monospace;font-size:16px;
                color:rgba(200,230,255,0.6);">
        {cnn_res['raw']:.4f}
    </div>
</div>
""", unsafe_allow_html=True)

    # ── VT Details ────────────────────────────────────────────────────────────
    if vt_res:
        st.markdown("---")
        st.markdown('<div class="section-tag">// VIRUSTOTAL THREAT INTELLIGENCE</div>',
                    unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Verdict",    vt_res["verdict"])
        c2.metric("Malicious",  vt_res["mal"])
        c3.metric("Total Engines", vt_res["total"])
        c4.metric("Target",     str(vt_res["target"])[:20])

    # ── Recommendations ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-tag">// RECOMMENDATIONS</div>', unsafe_allow_html=True)

    if overall == "MALICIOUS":
        recs = [
            ("🚫 ISOLATE", "Immediately isolate the system from the network."),
            ("🔒 QUARANTINE", "Move the file to a sandboxed quarantine environment."),
            ("🔍 FORENSICS", "Capture memory dump and disk image for forensic analysis."),
            ("🛡️ PATCH", "Review and patch any exploited vulnerabilities."),
            ("📢 REPORT", "Report to your CSIRT/SOC team and document the incident."),
        ]
    elif overall == "SUSPICIOUS":
        recs = [
            ("🧪 SANDBOX", "Execute in a sandboxed environment for dynamic analysis."),
            ("🔍 REVIEW", "Manual review of suspicious sections and imports."),
            ("📊 MONITOR", "Enable enhanced monitoring on the affected system."),
            ("🔄 RESCAN", "Rescan in 24h — new AV signatures may detect this."),
        ]
    else:
        recs = [
            ("✅ SAFE", "No immediate action required — file appears clean."),
            ("📋 LOG", "Log the scan result for compliance records."),
            ("🔄 PERIODIC", "Schedule periodic rescans for continuous protection."),
        ]

    for tag, text in recs:
        col_a = "#FF003C" if overall=="MALICIOUS" else "#FFD166" if overall=="SUSPICIOUS" else "#00FFD1"
        st.markdown(f"""
<div style="display:flex;gap:16px;padding:12px 16px;margin-bottom:8px;
            background:rgba(0,255,209,0.03);border:1px solid rgba(0,255,209,0.08);
            border-left:3px solid {col_a};border-radius:4px;">
    <span style="font-family:'Orbitron',monospace;font-size:11px;color:{col_a};
                 min-width:100px;">{tag}</span>
    <span style="font-size:14px;color:rgba(200,230,255,0.7);">{text}</span>
</div>
""", unsafe_allow_html=True)

    # ── Export ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-tag">// EXPORT REPORT</div>', unsafe_allow_html=True)

    report_data = {
        "report_id":   f"MVR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "generated":   ts,
        "overall":     overall,
        "pe_result":   {"label": pe_res["label"], "confidence": pe_res["conf"]} if pe_res else None,
        "cnn_result":  {"label": cnn_res["label"], "confidence": cnn_res["conf"]} if cnn_res else None,
        "vt_result":   vt_res,
    }

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️  DOWNLOAD JSON REPORT",
            data=json.dumps(report_data, indent=2),
            file_name=f"malwarevision_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col2:
        md_report = _build_markdown_report(report_data, ts, overall, recs)
        st.download_button(
            "⬇️  DOWNLOAD MARKDOWN REPORT",
            data=md_report,
            file_name=f"malwarevision_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True,
        )


def _verdict_card(col, title, verdict, extra):
    color = "#FF003C" if verdict == "Malicious" or verdict == "MALICIOUS" else \
            "#FFD166" if verdict == "SUSPICIOUS" else \
            "#00FFD1" if verdict in ("Benign","CLEAN","N/A") else "#C8E6FF"
    col.markdown(f"""
<div style="background:rgba(0,0,0,0.3);border:1px solid {color}33;
            border-top:2px solid {color};border-radius:8px;
            padding:20px;text-align:center;">
    <div style="font-size:20px;margin-bottom:6px;">{title}</div>
    <div style="font-family:'Orbitron',monospace;font-size:16px;
                font-weight:700;color:{color};">{verdict}</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:13px;
                color:rgba(200,230,255,0.5);margin-top:6px;">{extra}</div>
</div>
""", unsafe_allow_html=True)


def _build_markdown_report(data, ts, overall, recs):
    lines = [
        "# MalwareVision AI — Threat Intelligence Report",
        f"",
        f"**Report ID:** {data['report_id']}  ",
        f"**Generated:** {ts}  ",
        f"**Overall Assessment:** **{overall}**",
        "",
        "---",
        "",
        "## Analysis Results",
        "",
    ]
    if data["pe_result"]:
        p = data["pe_result"]
        lines += [f"### PE Static Analysis",
                  f"- Verdict: **{p['label']}**",
                  f"- Confidence: **{p['confidence']*100:.2f}%**", ""]
    if data["cnn_result"]:
        c = data["cnn_result"]
        lines += [f"### CNN Image Analysis",
                  f"- Verdict: **{c['label']}**",
                  f"- Confidence: **{c['confidence']*100:.2f}%**", ""]
    if data["vt_result"]:
        v = data["vt_result"]
        lines += [f"### VirusTotal",
                  f"- Verdict: **{v['verdict']}**",
                  f"- Engines flagged: **{v['mal']}/{v['total']}**", ""]
    lines += ["---", "## Recommendations", ""]
    for tag, text in recs:
        lines.append(f"- **{tag}**: {text}")
    return "\n".join(lines)
