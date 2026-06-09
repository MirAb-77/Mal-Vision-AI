# MalwareVision AI — Model Registry

## Cybersecurity Model Layer

This directory contains the trained machine learning models powering the MalwareVision AI detection framework. The system is designed for static malware analysis using Portable Executable (PE) inspection and image-based binary representation learning.

It operates as a dual-intelligence detection layer within a broader cybersecurity pipeline.

---

## System Architecture

The detection engine is built on two complementary analytical streams:

### PE Static Analysis Model

This model performs structural and behavioral analysis of Windows executable files.

- Input: Extracted PE header and section-level features
- Output: Binary classification (Benign / Malicious)
- Method: Supervised machine learning classifier trained on engineered static features
- Objective: Detect anomalies in executable structure, imports, entropy, and metadata patterns

---

### Image-Based Malware Model

This model converts binary executables into grayscale image representations and applies deep learning-based classification.

- Input: Byte-level binary transformed into 2D image matrix
- Output: Malware classification label
- Method: Convolutional Neural Network (CNN)
- Objective: Capture spatial and texture-level patterns in malware binaries

---

## PE Model Evaluation Report

The PE classification model was evaluated on a held-out test dataset under controlled conditions.

### Performance Metrics

| Metric      | Score   |
|-------------|---------|
| Accuracy    | 87.1%   |
| Precision   | 94.1%   |
| Recall      | 88.0%   |
| F1 Score    | 87.5%   |
| ROC-AUC     | 93.5%   |

### Interpretation

- High precision indicates low false-positive rate, suitable for reducing alert fatigue in SOC environments
- Strong ROC-AUC reflects robust separability between benign and malicious classes
- Recall indicates reliable malware detection coverage, though minor false negatives may still occur
- Balanced F1 score confirms stable performance across both classes

---

## Inference Pipeline

1. Input file is received (PE or binary image format)
2. Feature extraction or binary transformation is applied
3. Preprocessing pipeline standardizes input distribution
4. Trained model executes inference
5. Prediction output:
   - 0 → Benign
   - 1 → Malicious

---

## Model Artifacts

This directory contains serialized components required for inference:

- PE classification model
- Image classification model
- Feature scalers
- Encoders (if applicable)
- Preprocessing pipelines

All artifacts are version-controlled for reproducibility and deployment traceability.

---

## Usage Example

```python
import joblib

# Load PE model
pe_model = joblib.load("models/pe_model.pkl")

# Load scaler
scaler = joblib.load("models/scaler.pkl")

# Preprocess input
X_test_scaled = scaler.transform(X_test)

# Prediction
pred = pe_model.predict(X_test_scaled)
