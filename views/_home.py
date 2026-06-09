import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import random, time
from datetime import datetime, timedelta

def render():
    # Dashboard State
    if "files_scanned" not in st.session_state:
       st.session_state.files_scanned = 0
    if "threats_detected" not in st.session_state:
       st.session_state.threats_detected = 0
    if "benign_files" not in st.session_state:
       st.session_state.benign_files = 0
    if "current_threat_score" not in st.session_state:
       st.session_state.current_threat_score = 0
    if "last_prediction" not in st.session_state:
       st.session_state.last_prediction = "No Scan"
    if "last_confidence" not in st.session_state:
       st.session_state.last_confidence = 0
   



    # ── HERO ──────────────────────────────────────────────────────────────────
    st.markdown("""
<div style="position:relative;padding:56px 48px 48px;border-radius:16px;
            background:linear-gradient(135deg,rgba(0,255,209,0.07) 0%,
            rgba(0,180,255,0.04) 50%,rgba(123,47,255,0.06) 100%);
            border:1px solid rgba(0,255,209,0.15);overflow:hidden;margin-bottom:28px;">
  <!-- corner accents -->
  <div style="position:absolute;top:0;left:0;width:24px;height:24px;
              border-top:2px solid #00FFD1;border-left:2px solid #00FFD1;"></div>
  <div style="position:absolute;top:0;right:0;width:24px;height:24px;
              border-top:2px solid #FF003C;border-right:2px solid #FF003C;"></div>
  <div style="position:absolute;bottom:0;left:0;width:24px;height:24px;
              border-bottom:2px solid #7B2FFF;border-left:2px solid #7B2FFF;"></div>
  <div style="position:absolute;bottom:0;right:0;width:24px;height:24px;
              border-bottom:2px solid #00B4FF;border-right:2px solid #00B4FF;"></div>

  <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:6px;
              color:#00B4FF;margin-bottom:14px;animation:fadeSlideUp 0.6s ease both;">
    // NEXT-GEN THREAT INTELLIGENCE PLATFORM v3.1.0 // CLASSIFIED
  </div>
  <div style="font-family:'Orbitron',monospace;font-weight:900;
              font-size:clamp(36px,6vw,76px);line-height:1;
              background:linear-gradient(90deg,#fff 30%,#00FFD1 70%,#00B4FF 100%);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;letter-spacing:4px;margin-bottom:6px;
              animation:fadeSlideUp 0.6s 0.1s ease both;">
    MALWAREVISION
  </div>
  <div style="font-family:'Orbitron',monospace;font-weight:900;
              font-size:clamp(28px,4vw,52px);line-height:1;color:#FF003C;
              text-shadow:0 0 40px rgba(255,0,60,0.5);letter-spacing:6px;
              margin-bottom:28px;animation:fadeSlideUp 0.6s 0.15s ease both;">
    ARTIFICIAL INTELLIGENCE
  </div>
  <p style="font-size:17px;color:rgba(200,230,255,0.6);max-width:680px;
            line-height:1.8;margin-bottom:32px;font-family:'Rajdhani',sans-serif;
            animation:fadeSlideUp 0.6s 0.2s ease both;">
    Enterprise-grade AI threat detection combining static PE analysis,
    binary visualisation CNN, SHAP · LIME · Grad-CAM explainability,
    and live VirusTotal threat intelligence — all in one classified platform.
  </p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;animation:fadeSlideUp 0.6s 0.25s ease both;">
    <span style="padding:6px 18px;border:1px solid rgba(255,0,60,0.4);border-radius:3px;
                 font-family:'Share Tech Mono',monospace;font-size:11px;
                 color:#FF003C;letter-spacing:3px;background:rgba(255,0,60,0.06);">
      ⚡ THREAT DETECTION</span>
    <span style="padding:6px 18px;border:1px solid rgba(0,255,209,0.3);border-radius:3px;
                 font-family:'Share Tech Mono',monospace;font-size:11px;
                 color:#00FFD1;letter-spacing:3px;background:rgba(0,255,209,0.05);">
      🔬 EXPLAINABLE AI</span>
    <span style="padding:6px 18px;border:1px solid rgba(123,47,255,0.4);border-radius:3px;
                 font-family:'Share Tech Mono',monospace;font-size:11px;
                 color:#A87FFF;letter-spacing:3px;background:rgba(123,47,255,0.06);">
      🌐 THREAT INTEL</span>
    <span style="padding:6px 18px;border:1px solid rgba(0,180,255,0.3);border-radius:3px;
                 font-family:'Share Tech Mono',monospace;font-size:11px;
                 color:#00B4FF;letter-spacing:3px;background:rgba(0,180,255,0.05);">
      🧠 DATA ANALYTICS</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── LIVE KPI METRICS ──────────────────────────────────────────────────────
    st.markdown(
    '<div class="section-tag">// LIVE SYSTEM METRICS</div>',
    unsafe_allow_html=True
)
    detection_rate = (
        st.session_state.threats_detected /
        st.session_state.files_scanned * 100
    )if st.session_state.files_scanned > 0 else 0
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.metric(
            "Files Scanned",
            st.session_state.files_scanned
    )
    with c2:
        st.metric(
            "Threats Detected",
             st.session_state.threats_detected
    )

    with c3:
        st.metric(
            "Detection Rate",
            f"{detection_rate:.1f}%"
    )

    with c4:
        st.metric(
            "Last Scan",
            st.session_state.last_prediction
    )

    with c5:
        st.metric(
            "PE Accuracy",
             "98.4%"
    )

    with c6:
         st.metric(
             "CNN Accuracy",
             "87.1%"
    )
    st.markdown("---")

    # ── WORLD THREAT MAP + GAUGE ──────────────────────────────────────────────
    st.markdown('<div class="section-tag">// GLOBAL THREAT INTELLIGENCE MAP</div>',
                unsafe_allow_html=True)

    col_map, col_gauge = st.columns([3, 1])

    with col_map:
        # Generate realistic threat origins
        threat_data = {
            "country": ["United States","China","Russia","Brazil","India",
                        "Germany","United Kingdom","Ukraine","Iran","North Korea",
                        "Nigeria","Romania","Netherlands","France","Turkey",
                        "South Korea","Japan","Canada","Australia","Pakistan"],
            "lat":  [37.1, 35.9, 61.5, -14.2, 20.6,
                     51.2, 54.4, 49.0, 32.4, 40.0,
                     9.1,  45.9, 52.1, 46.2, 38.9,
                     35.9, 36.2, 56.1, -25.3, 30.4],
            "lon":  [-95.7, 104.2, 105.3, -51.9, 78.9,
                     10.5, -3.4,  31.2,  53.7, 127.5,
                     8.7,  24.9,  5.3,   2.2,  35.2,
                     127.8,138.3,-106.3, 133.8, 69.3],
            "threats": [312, 287, 245, 89, 134,
                        67,  58,  201, 178, 156,
                        43,  92,  61,  48,  73,
                        54,  31,  28,  19,  87],
            "malware_type": ["Ransomware","APT","Botnet","Adware","Spyware",
                             "Trojan","Ransomware","APT","Worm","APT",
                             "Phishing","Banker","C2","Ransomware","Adware",
                             "APT","Spyware","Ransomware","Botnet","Worm"],
        }
        df_map = pd.DataFrame(threat_data)

        fig_map = go.Figure()

        # Choropleth base layer
        fig_map.add_trace(go.Choropleth(
            locations=df_map["country"],
            locationmode="country names",
            z=df_map["threats"],
            colorscale=[[0,"rgba(0,20,40,0.6)"],
                        [0.3,"rgba(123,47,255,0.4)"],
                        [0.7,"rgba(255,100,0,0.6)"],
                        [1.0,"rgba(255,0,60,0.85)"]],
            showscale=False,
            hovertemplate="<b>%{location}</b><br>Threats: %{z}<extra></extra>",
        ))

        # Bubble scatter
        fig_map.add_trace(go.Scattergeo(
            lat=df_map["lat"],
            lon=df_map["lon"],
            mode="markers+text",
            marker=dict(
                size=df_map["threats"] / 8,
                color=df_map["threats"],
                colorscale=[[0,"#00B4FF"],[0.5,"#FF8C00"],[1,"#FF003C"]],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Threats", font=dict(color="#C8E6FF", size=11)),
                    tickfont=dict(color="rgba(200,230,255,0.5)", size=9),
                    x=1.0, thickness=10,
                ),
                line=dict(color="rgba(0,0,0,0.5)", width=1),
                opacity=0.85,
            ),
            text=df_map["country"],
            textfont=dict(color="rgba(200,230,255,0)", size=1),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Threat Count: %{marker.color}<br>"
                "Lat: %{lat:.1f} | Lon: %{lon:.1f}<extra></extra>"
            ),
            name="",
        ))

        fig_map.update_geos(
            bgcolor="rgba(0,0,0,0)",
            showland=True,  landcolor="rgba(5,15,30,0.95)",
            showocean=True, oceancolor="rgba(0,10,30,0.85)",
            showlakes=True, lakecolor="rgba(0,20,50,0.7)",
            showcoastlines=True, coastlinecolor="rgba(0,255,209,0.15)",
            showcountries=True, countrycolor="rgba(0,255,209,0.08)",
            showframe=False,
            projection_type="natural earth",
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            geo=dict(bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=0,b=0,l=0,r=0),
            height=420,
            showlegend=False,
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_gauge:
        st.markdown('<div class="section-tag">// THREAT SCORE</div>', unsafe_allow_html=True)

        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=st.session_state.current_threat_score,
            delta={"reference": 72.0, "increasing": {"color": "#FF003C"},
                   "font": {"family": "Share Tech Mono", "size": 12}},
            number={"font": {"color": "#FF003C", "family": "Orbitron", "size": 38},
                    "suffix": ""},
            title={"text": "GLOBAL<br>THREAT LEVEL",
                   "font": {"color": "rgba(200,230,255,0.5)",
                             "family": "Share Tech Mono", "size": 10}},
            gauge={
                "axis": {"range": [0,100],
                         "tickfont": {"color":"rgba(200,230,255,0.3)","size":9}},
                "bar":  {"color": "#FF003C", "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range":[0,33],  "color":"rgba(0,255,100,0.08)"},
                    {"range":[33,66], "color":"rgba(255,209,0,0.08)"},
                    {"range":[66,100],"color":"rgba(255,0,60,0.10)"},
                ],
                "threshold": {"line": {"color":"#FF003C","width":3}, "value": st.session_state.current_threat_score},
            }
        ))
        fig_g.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#C8E6FF",
            height=260, margin=dict(t=30,b=0,l=10,r=10)
        )
        st.plotly_chart(fig_g, use_container_width=True)

        # Top threat countries mini list
        st.markdown('<div class="mono-label" style="margin-top:8px;">TOP THREAT ORIGINS</div>',
                    unsafe_allow_html=True)
        top5 = df_map.nlargest(5, "threats")[["country","threats","malware_type"]]
        for _, row in top5.iterrows():
            pct = row["threats"] / df_map["threats"].max()
            st.markdown(f"""
<div style="margin-bottom:8px;">
  <div style="display:flex;justify-content:space-between;
              font-family:'Share Tech Mono',monospace;font-size:10px;
              color:rgba(200,230,255,0.7);margin-bottom:3px;">
    <span>{row['country']}</span>
    <span style="color:#FF003C;">{row['threats']}</span>
  </div>
  <div style="height:3px;background:rgba(255,0,60,0.1);border-radius:2px;">
    <div style="height:3px;width:{pct*100:.0f}%;
                background:linear-gradient(90deg,#FF003C,#FF8C00);border-radius:2px;"></div>
  </div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:9px;
              color:rgba(200,230,255,0.3);margin-top:2px;">{row['malware_type']}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # ── LIVE THREAT FEED + MALWARE FAMILY CHART ───────────────────────────────
    st.markdown('<div class="section-tag">// LIVE THREAT FEED & INTELLIGENCE</div>',
                unsafe_allow_html=True)

    col_feed, col_fam = st.columns([1, 1])

    with col_feed:
        st.markdown("#### 📡 Real-Time Detection Feed")
        feed_events = [
            ("14:31:02","THREAT","sample_0xA3F.exe","Ransomware.LockBit","Russia",    "99.2%"),
            ("14:31:07","CLEAN", "update_kb4023.dll","—",                 "USA",       "3.1%"),
            ("14:31:12","WARN",  "inject_tool.bin",  "Suspicious Packer", "Ukraine",   "61.7%"),
            ("14:31:19","THREAT","dropper_v4.exe",   "Trojan.Agent.Gen",  "China",     "97.4%"),
            ("14:31:24","CLEAN", "runtime_x64.sys",  "—",                 "Germany",   "1.8%"),
            ("14:31:31","THREAT","payload_enc.bin",  "Malware.Emotet",    "Nigeria",   "94.8%"),
            ("14:31:38","WARN",  "net_scanner.py",   "PUA.NetTool",       "Romania",   "52.3%"),
            ("14:31:45","CLEAN", "setup_v2.msi",     "—",                 "UK",        "2.4%"),
            ("14:31:52","THREAT","crypt_stub.exe",   "Ransomware.WannaCry","Iran",     "98.9%"),
            ("14:32:01","CLEAN", "chrome_upd.exe",   "—",                 "Japan",     "0.9%"),
        ]
        colors = {"THREAT":"#FF003C","CLEAN":"#00FFD1","WARN":"#FFD166"}
        bg     = {"THREAT":"rgba(255,0,60,0.06)","CLEAN":"rgba(0,255,209,0.04)","WARN":"rgba(255,209,102,0.06)"}

        for ts, verdict, fname, mtype, origin, conf in feed_events:
            c = colors[verdict]
            b = bg[verdict]
            st.markdown(f"""
<div style="background:{b};border-left:3px solid {c};border-radius:0 4px 4px 0;
            padding:8px 12px;margin-bottom:6px;display:grid;
            grid-template-columns:70px 60px 1fr 80px 60px;gap:8px;align-items:center;">
  <span style="font-family:'Share Tech Mono',monospace;font-size:10px;
               color:rgba(200,230,255,0.35);">{ts}</span>
  <span style="font-family:'Share Tech Mono',monospace;font-size:10px;
               color:{c};letter-spacing:2px;">{verdict}</span>
  <div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                color:rgba(200,230,255,0.8);">{fname}</div>
    <div style="font-size:10px;color:rgba(200,230,255,0.35);">{mtype} · {origin}</div>
  </div>
  <span style="font-family:'Orbitron',monospace;font-size:12px;
               color:{c};text-align:right;">{conf}</span>
</div>
""", unsafe_allow_html=True)

    with col_fam:
        st.markdown("#### 🦠 Malware Family Distribution")
        families = ["Ransomware","Trojan","Botnet","Worm","Spyware",
                    "Adware","Rootkit","Banker","APT","PUA"]
        counts   = [342, 287, 201, 156, 134, 98, 87, 76, 62, 43]
        colors_f = ["#FF003C","#FF5733","#FF8C00","#FFD166","#00B4FF",
                    "#00FFD1","#7B2FFF","#A87FFF","#FF003C","#00FFD1"]

        fig_fam = go.Figure(go.Bar(
            x=counts, y=families, orientation="h",
            marker=dict(color=colors_f, opacity=0.85,
                        line=dict(color="rgba(0,0,0,0)")),
            text=[f" {c:,}" for c in counts],
            textposition="outside",
            textfont=dict(color="#C8E6FF", family="Share Tech Mono", size=11),
            hovertemplate="<b>%{y}</b>: %{x:,} detections<extra></extra>",
        ))
        fig_fam.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#C8E6FF",
            xaxis=dict(gridcolor="rgba(200,230,255,0.05)", title="Detections (30d)"),
            yaxis=dict(tickfont=dict(family="Share Tech Mono", size=11),
                       autorange="reversed"),
            height=420, margin=dict(t=20,b=40,l=100,r=60),
            showlegend=False,
        )
        st.plotly_chart(fig_fam, use_container_width=True)

    st.markdown("---")

    # ── DETECTION TIMELINE ────────────────────────────────────────────────────
    st.markdown('<div class="section-tag">// 30-DAY DETECTION TIMELINE</div>',
                unsafe_allow_html=True)

    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=29-i) for i in range(30)]
    mal   = np.random.randint(280,420,30).tolist()
    ben   = np.random.randint(600,900,30).tolist()
    sus   = np.random.randint(40,120,30).tolist()

    fig_tl = go.Figure()
    fig_tl.add_trace(go.Scatter(
        x=dates, y=mal, name="Malicious",
        fill="tozeroy", fillcolor="rgba(255,0,60,0.08)",
        line=dict(color="#FF003C", width=2),
        hovertemplate="%{x|%b %d}<br>Malicious: %{y}<extra></extra>",
    ))
    fig_tl.add_trace(go.Scatter(
        x=dates, y=sus, name="Suspicious",
        fill="tozeroy", fillcolor="rgba(255,209,102,0.06)",
        line=dict(color="#FFD166", width=1.5, dash="dot"),
        hovertemplate="%{x|%b %d}<br>Suspicious: %{y}<extra></extra>",
    ))
    fig_tl.add_trace(go.Scatter(
        x=dates, y=ben, name="Clean",
        fill="tozeroy", fillcolor="rgba(0,255,209,0.05)",
        line=dict(color="#00FFD1", width=2),
        hovertemplate="%{x|%b %d}<br>Clean: %{y}<extra></extra>",
    ))
    fig_tl.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#C8E6FF",
        xaxis=dict(gridcolor="rgba(200,230,255,0.04)",
                   tickfont=dict(family="Share Tech Mono", size=10)),
        yaxis=dict(gridcolor="rgba(200,230,255,0.04)", title="File Count"),
        legend=dict(font=dict(color="#C8E6FF",family="Share Tech Mono",size=11),
                    bgcolor="rgba(0,0,0,0.4)", bordercolor="rgba(0,255,209,0.15)",
                    borderwidth=1),
        height=300, margin=dict(t=20,b=40,l=60,r=20),
        hovermode="x unified",
    )
    st.plotly_chart(fig_tl, use_container_width=True)

    st.markdown("---")

    # ── TECH STACK ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-tag">// TECHNOLOGY STACK</div>', unsafe_allow_html=True)
    techs = [
        ("🐍","Python",      "Core Engine",   "#00FFD1"),
        ("⚡","FastAPI",     "REST Backend",  "#00B4FF"),
        ("🧠","TensorFlow",  "Deep Learning", "#FF003C"),
        ("🌲","Scikit-Learn","ML Engine",     "#00FFD1"),
        ("📊","SHAP",        "Explainability","#7B2FFF"),
        ("🔬","LIME",        "Interpretability","#A87FFF"),
        ("🎯","Grad-CAM",   "Visual XAI",    "#FF8C00"),
        ("🦠","VirusTotal", "Threat Intel",  "#FF003C"),
        ("📈","Plotly",     "Visualization", "#00B4FF"),
        ("🖥️","Streamlit",  "Frontend UI",   "#00FFD1"),
        ("🔒","LIEF",       "PE Parsing",    "#FFD166"),
        ("🕸️","YARA",       "Pattern Rules", "#A87FFF"),
    ]
    cols = st.columns(6)
    for i,(icon,name,typ,color) in enumerate(techs):
        with cols[i%6]:
            st.markdown(f"""
<div style="background:rgba(0,20,40,0.6);border:1px solid {color}22;
            border-top:2px solid {color}55;border-radius:8px;padding:16px 10px;
            text-align:center;margin-bottom:10px;transition:0.3s;">
  <div style="font-size:28px;margin-bottom:8px;">{icon}</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:10px;
              color:{color};letter-spacing:2px;">{name}</div>
  <div style="font-size:10px;color:rgba(200,230,255,0.3);margin-top:4px;">{typ}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # ── PIPELINE + MODEL PERF SIDE BY SIDE ───────────────────────────────────
    col_pipe, col_perf = st.columns([1,2])

    with col_pipe:
        st.markdown('<div class="section-tag">// ANALYSIS PIPELINE</div>',
                    unsafe_allow_html=True)
        steps = [
            ("📁","Upload File",      "#00B4FF"),
            ("⚙️","Feature Extract", "#7B2FFF"),
            ("🧠","ML / CNN Predict","#FF003C"),
            ("🔬","XAI Layer",       "#A87FFF"),
            ("🌐","VirusTotal API",  "#FF8C00"),
            ("📋","Threat Report",   "#00FFD1"),
        ]
        for i,(icon,label,color) in enumerate(steps):
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;">
  <div style="width:36px;height:36px;border-radius:50%;
              background:rgba(0,20,40,0.8);border:1px solid {color}55;
              display:flex;align-items:center;justify-content:center;
              font-size:16px;flex-shrink:0;">{icon}</div>
  <div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                color:{color};letter-spacing:2px;">{label}</div>
  </div>
</div>
{('<div style="margin-left:18px;width:1px;height:12px;background:rgba(200,230,255,0.1);"></div>') if i < len(steps)-1 else ''}
""", unsafe_allow_html=True)

    with col_perf:
        st.markdown('<div class="section-tag">// MODEL PERFORMANCE COMPARISON</div>',
                    unsafe_allow_html=True)
        cats   = ["Accuracy","Precision","Recall","F1-Score","AUC-ROC"]
        rf_v   = [98.4, 97.9, 98.1, 98.0, 99.2]
        cnn_v  = [87.1, 94.1, 88.0, 87.5, 93.4]

        fig_perf = go.Figure()
        fig_perf.add_trace(go.Bar(
            name="🌲 Random Forest", x=cats, y=rf_v,
            marker_color="#00FFD1", opacity=0.85,
            text=[f"{v}%" for v in rf_v], textposition="outside",
            textfont=dict(color="#00FFD1", size=11, family="Share Tech Mono"),
        ))
        fig_perf.add_trace(go.Bar(
            name="🧠 CNN", x=cats, y=cnn_v,
            marker_color="#FF003C", opacity=0.85,
            text=[f"{v}%" for v in cnn_v], textposition="outside",
            textfont=dict(color="#FF003C", size=11, family="Share Tech Mono"),
        ))
        fig_perf.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#C8E6FF",
            yaxis=dict(gridcolor="rgba(200,230,255,0.04)"),
            xaxis=dict(tickfont=dict(family="Share Tech Mono",size=11)),
            legend=dict(font=dict(color="#C8E6FF",family="Share Tech Mono"),
                        bgcolor="rgba(0,0,0,0)"),
            height=320, margin=dict(t=30,b=40,l=40,r=20),
            bargap=0.25, bargroupgap=0.08,
        )
        st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("---")

    # ── RADAR COMPARISON ──────────────────────────────────────────────────────
    st.markdown('<div class="section-tag">// SYSTEM CAPABILITY RADAR</div>',
                unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    radar_cats = ["Detection Rate","Speed","Explainability",
                  "Coverage","Accuracy","Scalability"]

    with col_r1:
        fig_r = go.Figure()
        for name, vals, color in [
            ("RF Model",  [98,99,95,85,98,90], "#00FFD1"),
            ("CNN Model", [87,94,88,97,93,85], "#FF003C"),
        ]:
            v = vals + [vals[0]]
            c = radar_cats + [radar_cats[0]]
            fig_r.add_trace(go.Scatterpolar(
                r=v, theta=c, name=name, fill="toself",
                fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)",
                line=dict(color=color, width=2),
                marker=dict(size=6, color=color),
            ))
        fig_r.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(range=[70,100],visible=True,
                                tickfont=dict(color="rgba(200,230,255,0.3)",size=8),
                                gridcolor="rgba(200,230,255,0.05)"),
                angularaxis=dict(tickfont=dict(color="rgba(200,230,255,0.6)",
                                               family="Share Tech Mono",size=10),
                                 gridcolor="rgba(200,230,255,0.05)"),
            ),
            paper_bgcolor="rgba(0,0,0,0)", font_color="#C8E6FF",
            legend=dict(font=dict(color="#C8E6FF",family="Share Tech Mono"),
                        bgcolor="rgba(0,0,0,0)"),
            height=340, margin=dict(t=20,b=20,l=20,r=20),
            title=dict(text="Model Capability Radar",
                       font=dict(color="rgba(200,230,255,0.5)",
                                 family="Share Tech Mono",size=11)),
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with col_r2:
        # Sunburst of threat taxonomy
        fig_sun = go.Figure(go.Sunburst(
            labels=["Malware","Ransomware","Trojan","Botnet","Worm",
                    "LockBit","WannaCry","Ryuk","Agent","RAT",
                    "Mirai","Necurs","ILOVEYOU","Conficker",
                    "Spyware","Adware","PUA","Keylogger","Stalkerware","Junkware"],
            parents=["","Malware","Malware","Malware","Malware",
                     "Ransomware","Ransomware","Ransomware","Trojan","Trojan",
                     "Botnet","Botnet","Worm","Worm",
                     "Malware","Malware","Malware","Spyware","Spyware","Adware"],
            values=[0,342,287,201,156,
                    189,98,55,187,100,
                    131,70,86,70,
                    134,98,43,90,44,98],
            branchvalues="total",
            marker=dict(
                colors=["#020A14","#FF003C","#FF5733","#7B2FFF","#FF8C00",
                        "#FF0050","#FF3366","#FF6680","#FF7043","#FFAB91",
                        "#9C27B0","#CE93D8","#FFB300","#FFD54F",
                        "#00B4FF","#00FFD1","#A87FFF","#29B6F6","#81D4FA","#B2EBF2"],
                line=dict(color="rgba(2,10,20,0.8)", width=1),
            ),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
            textfont=dict(family="Share Tech Mono", size=10, color="rgba(255,255,255,0.85)"),
        ))
        fig_sun.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#C8E6FF",
            height=340, margin=dict(t=20,b=20,l=20,r=20),
            title=dict(text="Malware Taxonomy Sunburst",
                       font=dict(color="rgba(200,230,255,0.5)",
                                 family="Share Tech Mono",size=11)),
        )
        st.plotly_chart(fig_sun, use_container_width=True)

    st.markdown("---")

    # ── FOOTER ────────────────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;padding:24px 0 8px;">
  <div style="font-family:'Orbitron',monospace;font-size:16px;font-weight:900;
              color:#00FFD1;text-shadow:0 0 15px rgba(0,255,209,0.3);
              letter-spacing:4px;margin-bottom:8px;">MALWAREVISION AI</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:10px;
              color:rgba(200,230,255,0.2);letter-spacing:3px;">
    ADVANCED MALWARE DETECTION & EXPLAINABILITY PLATFORM
    · BUILT WITH STREAMLIT · TENSORFLOW · SHAP · LIME · GRADCAM
    · © 2026 CYBER SECURITY RESEARCH
  </div>
</div>
""", unsafe_allow_html=True)
