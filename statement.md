# Project Problem Statement & Scope

## 1. Problem Statement
Traditional CCTV surveillance systems in facilities, campuses, and secure zones suffer from heavy reliance on manual human operators. Security personnel watching multiple video streams experience cognitive fatigue, resulting in high false-negative rates, delayed incident response times, and failure to track unauthorized intrusions. Furthermore, conventional systems lack real-time biometric verification to distinguish authorized staff from unknown visitors, and they produce unstructured video recordings that are cumbersome to audit after security breaches occur.

## 2. Scope of the Project
VisionGuard provides an intelligent, automated Computer Vision surveillance and access control system designed to process live video streams at the edge. The project encompasses:
- Real-time video ingestion, adaptive illumination normalization, and Gaussian noise suppression.
- Foreground motion modeling using Gaussian Mixture Models (MOG2) to detect moving targets and analyze spatial loitering.
- Biometric facial feature extraction and verification against an enrolled database of authorized personnel.
- Automated multi-factor security threat classification (Normal, Caution, High, Critical) with perimeter breach detection.
- Relational audit logging in an ACID-compliant SQLite database storing structured telemetry, personnel records, and incident event logs.
- Automatic capture and timestamping of incident visual evidence snapshots.

## 3. Target Users
1. **Facility Security Officers**: Receive instant visual alerts, threat scores, and bounding box telemetry.
2. **Access Control Administrators**: Enroll and manage personnel biometric access permissions and badges.
3. **Compliance & Audit Investigators**: Query historical security events, examine tamper-evident incident snapshots, and audit breach timelines.

## 4. High-Level Features
- **Adaptive Frame Preprocessor**: CLAHE luminance enhancement and noise filtering for varied lighting conditions.
- **MOG2 Background Motion Engine**: Dynamic shadow elimination and contour area tracking.
- **Facial Biometrics & Access Control**: Real-time face detection, color histogram signature representation, and identity verification.
- **Rule-Based Threat Classification**: Real-time multi-factor risk scoring engine.
- **Relational Persistence & Audit Ledger**: SQLite database recording every alert, timestamp, and personnel entry.
- **Dual Operating Modes**: Interactive real-time webcam studio (`run_studio.py`) and reproducible offline multi-scenario simulator (`run_simulation.py`).
