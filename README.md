# VisionGuard: AI Surveillance, Intrusion Detection & Biometric Access System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-brightgreen.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, real-time Computer Vision system for automated perimeter security, unauthorized intruder detection, and biometric access verification.

Built to comply with the **VITyarthi "Build Your Own Project"** evaluation criteria and technical rubric.

---

## 1. Overview of the Project
VisionGuard transforms standard video feeds into an active, intelligent monitoring station. Rather than passively recording hours of footage, VisionGuard:
1. Normalizes ambient lighting using Contrast Limited Adaptive Histogram Equalization (CLAHE).
2. Segment moving targets and eliminates shadows using MOG2 background subtractors.
3. Evaluates facial biometrics against an enrolled authorized personnel registry.
4. Classifies situational threat levels (Normal, Caution, High, Critical) using a rules-based risk analyzer.
5. Emits real-time visual alerts and records structured incident evidence into an SQLite database.

---

## 2. Key Features
- **Multi-Stage Processing Pipeline**: Preprocessing $\rightarrow$ Motion Modeling $\rightarrow$ Biometrics $\rightarrow$ Threat Scoring $\rightarrow$ Persistence.
- **Real-Time Heads-Up Display (HUD)**: On-screen telemetry banner showing FPS, threat level, risk score, and hotkey guides.
- **Automated Incident Logging**: SQLite database recording event types, timestamps, confidence, motion area, and snapshot image paths.
- **Dual Execution Modes**:
  - **Live Webcam Studio (`run_studio.py`)**: Real-time camera feed with interactive hotkeys.
  - **Autonomous Simulation Suite (`run_simulation.py`)**: Evaluates 3 distinct security scenarios offline.
- **Zero External API Dependencies**: Completely self-contained; runs at 30+ FPS on edge CPU/GPU.

---

## 3. Technologies & Tools Used
- **Programming Language**: Python 3.11
- **Computer Vision Framework**: OpenCV (`opencv-python`)
- **Numerical Processing**: NumPy
- **Database / Persistence**: SQLite3 with standard SQL schema
- **Version Control**: Git
- **Documentation & Reporting**: Markdown, Mermaid UML diagrams, CSS-styled printable HTML reports

---

## 4. Steps to Install & Run

### Prerequisites
- Python 3.8 or newer
- Windows, macOS, or Linux

### Installation
```bash
# Navigate to the project directory
cd D:\VisionGuard_CV_Project

# Install dependencies
pip install -r requirements.txt
```

### Running the System

#### Option A: Offline Multi-Scenario Simulation (No Camera Needed)
```bash
python run_simulation.py
```
This simulates 3 security scenarios (Normal Perimeter, Authorized Officer Entry, Unauthorized Perimeter Breach), logs events to SQLite, and outputs snapshots to `output/snapshots/`.

#### Option B: Live Webcam Surveillance Studio
```bash
python run_studio.py --camera 0
```

#### Studio Hotkeys:
- `[1]`: Toggle HUD Overlays
- `[S]`: Save Manual Snapshot
- `[R]`: Reset & Recalibrate Background Model
- `[E]`: Enroll Current Face as Authorized
- `[Q]` / `[ESC]`: Exit Studio

---

## 5. Instructions for Testing

Run the automated test suite to validate all 6 modules:
```bash
python run_tests.py
```

Expected output:
```text
=========================================================
         VISIONGUARD AUTOMATED TEST SUITE                
=========================================================
[1/6] Testing Database Persistence & Schema... -> PASSED
[2/6] Testing Video Frame Preprocessor...     -> PASSED
[3/6] Testing Background Modeling Engine...   -> PASSED
[4/6] Testing Face Biometrics & Matching...   -> PASSED
[5/6] Testing Threat Analyzer & Risk Scorer.. -> PASSED
[6/6] Testing Visualizer HUD & Notifier...    -> PASSED
=========================================================
        ALL 6 VISIONGUARD UNIT TESTS PASSED!
=========================================================
```

---

## 6. Generated Screenshots & Visual Evidence
- `output/snapshots/scenario_01_normal.jpg`: Calm perimeter monitoring.
- `output/snapshots/scenario_02_authorized.jpg`: Authorized officer entry verification.
- `output/snapshots/scenario_03_intrusion.jpg`: Unauthorized perimeter breach alert.

---

## 7. Project Documentation & PDF Report
- Comprehensive academic report matching all 15 syllabus sections: [`PROJECT_REPORT.md`](PROJECT_REPORT.md)
- Formal Problem Statement: [`statement.md`](statement.md)
- System Architecture & UML Diagrams: [`docs/diagrams.md`](docs/diagrams.md)
- To generate the printable HTML/PDF project report:
  ```bash
  python generate_report.py
  ```
  Open `output/reports/VisionGuard_Project_Report.html` in your browser and press **Ctrl+P** (Save as PDF).
