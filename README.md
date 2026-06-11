<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/TensorFlow-Deep_Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-ML_Engine-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-SOC_Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/SHAP-Explainability-8A2BE2?style=for-the-badge"/>
<img src="https://img.shields.io/badge/LIME-Interpretability-00C853?style=for-the-badge"/>
<img src="https://img.shields.io/badge/VirusTotal-Threat_Intel-4285F4?style=for-the-badge&logo=virustotal&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-Data_Engine-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-Compute_Core-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>

<br/><br/>

# 💀 MalwareVision AI

### Next-Generation Cyber Threat Intelligence & SOC Simulation Engine

*PE Static Analysis · CNN Image Classification · Explainable AI · VirusTotal Integration · Automated Forensic Reports*

<br/>

[⚡ Quick Start](#-installation) · [🧠 Architecture](#-system-architecture) · [📊 Model Performance](#-model-performance) · [🔍 Explainability](#-explainable-ai-core) · [🤝 Contributing](#-contributing)

<br/>

> *"Every file is a potential threat. Every prediction is a decision."*

</div>

---

## 📌 Overview

**MalwareVision AI** is a production-grade cyber threat intelligence platform that simulates a real **Security Operations Center (SOC)**. It fuses two independent AI detection engines — static PE feature analysis and CNN-based malware image classification — into a single unified decision pipeline, enriched with explainable AI and live VirusTotal threat intelligence.

Built for cybersecurity researchers, SOC training environments, and AI explainability studies.

| Capability | Technology |
|-----------|-----------|
| 🧬 PE Static Analysis | Scikit-Learn classifier on extracted PE headers |
| 🖼️ CNN Image Classification | TensorFlow/Keras on binary visualisation images |
| 🔀 Fusion Decision Engine | Weighted ensemble vote from both models |
| 🔍 Explainability Layer | SHAP (global) + LIME (local) per-prediction |
| 🌐 Threat Intelligence | VirusTotal API enrichment & validation |
| 📋 Forensic Reporting | Automated incident report generation |

---

## 🧠 System Architecture

### Detection Pipeline

```
🟢  INPUT FILE  (PE / EXE / DLL)
        │
        ▼
┌───────────────────────────────┐
│   FEATURE EXTRACTION LAYER    │
│  PE Headers · Imports · Entropy│
└───────────┬───────────────────┘
            │
     ┌──────┴──────┐
     ▼             ▼
┌─────────┐   ┌──────────┐
│   PE    │   │   CNN    │
│CLASSIFIER│   │ IMAGE    │
│(Sklearn)│   │CLASSIFIER│
└────┬────┘   └────┬─────┘
     │              │
     └──────┬───────┘
            ▼
┌───────────────────────────────┐
│    FUSION DECISION ENGINE     │
│   Ensemble · Confidence Score │
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│   EXPLAINABILITY LAYER (XAI)  │
│     SHAP  ·  LIME  ·  Forensic│
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│  THREAT INTEL ENRICHMENT      │
│     VirusTotal API · Hash DB  │
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│   SOC DASHBOARD OUTPUT        │
│  Alert · Report · Risk Score  │
└───────────────────────────────┘
```

### Architecture Diagram

![System Architecture](https://github.com/user-attachments/assets/bf3f0781-d5cd-4987-afb1-2130b05d6cd7)

---

## 📊 Model Performance

### 🖼️ CNN Image Classifier

| Metric | Score |
|--------|-------|
| Accuracy | **87.1%** |
| Precision | **94.1%** |
| Recall | **88.0%** |
| F1 Score | **87.5%** |
| ROC-AUC | **93.5%** |

### 🧬 PE Static Classifier

| Metric | Score |
|--------|-------|
| Accuracy | **98.1%** |
| Precision | **97.6%** |
| Recall | **94.1%** |
| F1 Score | **98.1%** |
| ROC-AUC | **96.1%** |

> The PE static model significantly outperforms the CNN on structured binary inputs, while the CNN excels at detecting obfuscated samples through visual pattern recognition. The fusion engine combines both for maximum coverage.

---

## 🔍 Explainable AI Core

MalwareVision integrates a three-layer XAI pipeline to ensure every prediction is auditable and interpretable — not a black box.

### SHAP — Global Feature Attribution

![SHAP](https://img.shields.io/badge/SHAP-Feature_Attribution-8A2BE2?style=for-the-badge)

- Maps global feature contribution across all predictions
- Identifies which PE features (imports, entropy, section sizes) most strongly drive malware classification
- Provides system-wide behavioural insight for threat pattern analysis

### LIME — Local Per-Sample Explanation

![LIME](https://img.shields.io/badge/LIME-Local_Explainability-00C853?style=for-the-badge)

- Generates a local linear explanation for each individual file prediction
- Shows which specific features pushed the model toward malware or benign
- Per-sample decision transparency — critical for analyst review workflows

### Forensic Trace Engine

![FORENSIC](https://img.shields.io/badge/FORENSIC-Decision_Tracing-FF6D00?style=for-the-badge)

- Step-by-step prediction audit trail from raw input to final classification
- Maps every transformation in the feature pipeline to the output decision
- Produces audit-ready reasoning logs for compliance and incident response

### Explainability Framework

![Explainability Framework](https://github.com/user-attachments/assets/eb3b7157-d27b-4a76-84d0-096b36f41ae6)

---

## 🖥️ SOC Dashboard — Streamlit Frontend

A multi-page dark-theme Streamlit dashboard designed to simulate a real Security Operations Center interface.

### Dashboard Pages

```
app.py  ←  Entry point & navigation
│
├── 🏠  Home               System status · Module health · Quick scan
├── 🔍  File Analysis       Upload · PE extraction · Dual model inference
├── 🧠  Explainability      SHAP plots · LIME breakdown · Forensic trace
├── 🌐  Threat Intelligence VirusTotal enrichment · Hash lookup · IOC feed
├── 📊  SOC Dashboard       Live alert feed · Detection timeline · Risk map
└── 📋  Reports             Automated incident report · Export PDF / JSON
```

### UI Highlights

- **Dark cyberpunk SOC theme** — neon blue/green accent palette
- **Live attack simulation feed** — animated SOC alert stream
- **Dual model confidence bars** — side-by-side PE vs CNN scores
- **SHAP waterfall & beeswarm plots** rendered inline
- **LIME feature importance panel** with colour-coded influence
- **One-click report export** — PDF and JSON incident reports
- **VirusTotal enrichment panel** — vendor detections, file reputation

---

## 📂 Project Structure

```
malwarevision/
│
├── app.py                    ← Streamlit entry point & page router
│
├── views/
│   ├── home.py               ← System status & quick scan
│   ├── analysis.py           ← File upload & dual model inference
│   ├── explainability.py     ← SHAP + LIME + forensic trace panels
│   ├── threat_intel.py       ← VirusTotal enrichment dashboard
│   ├── soc_dashboard.py      ← Live alert feed & detection timeline
│   └── reports.py            ← Incident report generation & export
│
├── models/
│   ├── pe_classifier.pkl     ← Trained PE static model
│   ├── cnn_model.h5          ← Trained CNN image model
│   └── feature_scaler.pkl    ← Feature normalisation scaler
│
├── utils/
│   ├── pe_extractor.py       ← PE header & section feature extraction
│   ├── image_converter.py    ← Binary → visualisation image converter
│   ├── fusion_engine.py      ← Ensemble decision combiner
│   ├── xai_engine.py         ← SHAP + LIME computation
│   ├── virustotal.py         ← VirusTotal API client
│   └── report_generator.py   ← Automated incident report builder
│
├── assets/                   ← Static images, icons, CSS
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8+
- pip
- VirusTotal API key (free tier available)
- Virtual environment (recommended)

### 1 — Clone the Repository

```bash
git clone https://github.com/your-username/MalwareVision-AI.git
cd MalwareVision-AI
```

### 2 — Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>Core dependencies</summary>

```
streamlit>=1.32.0
tensorflow>=2.12.0
scikit-learn>=1.3.0
shap>=0.44.0
lime>=0.2.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
pefile>=2023.2.7
requests>=2.31.0
Pillow>=10.0.0
matplotlib>=3.7.0
```
</details>

### 4 — Configure VirusTotal API

```bash
# Create a .env file in the project root
echo "VIRUSTOTAL_API_KEY=your_api_key_here" > .env
```

### 5 — Run the Dashboard

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🛡️ Security Positioning

MalwareVision AI is designed for the following use cases:

| Use Case | Description |
|----------|-------------|
| 🔬 Research Labs | Malware analysis with explainable AI |
| 🏫 Academic Demos | FYP / thesis presentations on AI security |
| 🎓 SOC Training | Hands-on threat response simulation |
| 🧪 ML Security | Benchmarking XAI methods on malware data |
| 🏭 Industrial PoC | Prototype for enterprise endpoint security |

---

## 🚀 Roadmap

- [ ] Live malware feed integration (MalwareBazaar API)
- [ ] Real endpoint agent for file system monitoring
- [ ] Graph-based threat intelligence network (GNN)
- [ ] Adversarial malware robustness testing
- [ ] Cloud SOC deployment (Docker + AWS/GCP)
- [ ] Multi-family malware classification (beyond binary)

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. Fork and clone
git clone https://github.com/your-username/MalwareVision-AI.git

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Commit your changes
git commit -m "feat: describe your change"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

---

## 🔐 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [SHAP](https://github.com/shap/shap) — Explainable AI framework
- [LIME](https://github.com/marcotcr/lime) — Local interpretable model-agnostic explanations
- [pefile](https://github.com/erocarrera/pefile) — PE file parser
- [VirusTotal](https://www.virustotal.com/) — Threat intelligence API
- [Ultralytics](https://ultralytics.com/) — YOLO model infrastructure
- [Streamlit](https://streamlit.io/) — SOC dashboard framework

---

<div align="center">

Built for cybersecurity research · Powered by Explainable AI

⭐ Star this repo if it helped your research or project!

</div>
