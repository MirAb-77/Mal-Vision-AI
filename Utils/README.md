# MalwareVision AI — Utilities Layer
▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣

## System Utility Core

The `utils/` directory contains the backend operational engine of MalwareVision AI. It provides model loading, inference pipelines, UI orchestration components, and system-wide styling logic.

This layer acts as the **execution backbone** connecting raw models with the interactive views interface.

---

## ▣ SYSTEM ROLE ▣
▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣

This layer is responsible for:

- Model loading and initialization
- Prediction execution pipeline
- Shared UI components
- Navigation and layout control
- Global theme and visual consistency

It ensures modularity, scalability, and clean separation between UI and ML logic.

---

## ▣ MODULES ▣
▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣

### ▣ Model Loader (`model_loader.py`)
Core inference engine interface.

- Loads trained ML and DL models
- Handles PE and image model initialization
- Provides unified prediction API
- Ensures consistent preprocessing pipeline execution

Role: Centralized model orchestration layer

---

### ▣ Sidebar Controller (`sidebar.py`)
Navigation and UI structure manager.

- Controls multi-page navigation
- Defines SOC-style sidebar layout
- Routes between detection, explainability, and reporting modules
- Maintains consistent user experience across views

Role: Interface routing and dashboard navigation engine

---

### ▣ Theme Engine (`theme.py`)
Global UI styling and visual intelligence layer.

- Dark SOC-inspired theme configuration
- Neon-accent cybersecurity visual styling
- Streamlit CSS injection system
- UI consistency across all pages

Role: Visual identity and system-wide design control

---

## ▣ DATA FLOW ARCHITECTURE ▣
▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣

User Input
   ↓
View Layer (views/)
   ↓
Utility Layer (utils/)
   ↓
Model Inference Engine
   ↓
Prediction Output + Explainability Layer
   ↓
Visualization + Report Generation

---

## ▣ ENGINE DESIGN PHILOSOPHY ▣
▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣

The utilities layer is designed with cybersecurity-grade engineering principles:

- Separation of concerns between UI and ML logic
- Stateless prediction pipelines
- Reusable inference components
- Centralized model management
- Scalable multi-model architecture support

---

## ▣ ROLE IN MALWAREVISION AI ▣
▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣

The `utils/` layer functions as the **core execution backbone** of MalwareVision AI, translating trained intelligence into real-time cybersecurity decisions and ensuring seamless interaction between analytical models and the user-facing SOC dashboard.
