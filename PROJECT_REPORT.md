# VisionGuard: AI-Powered Autonomous Surveillance, Intrusion Detection & Biometric Access System

**Course Evaluation Submission: Build Your Own Project**  
**Institution**: VITyarthi Learning Destination  
**Author**: Student Project Submission  
**Date**: September 2026  
**Project Repository**: `D:\VisionGuard_CV_Project`  

---

## 1. Cover Page

```text
================================================================================
                                 PROJECT REPORT
                                  VISIONGUARD
              AI-Powered Autonomous Surveillance & Biometric Security
================================================================================
Course: Computer Vision & Machine Intelligence
Evaluation: Flipped Course Project Evaluation ("Build Your Own Project")
Submission Format: PDF / GitHub Repository
Repository Path: D:\VisionGuard_CV_Project
Target Platform: Windows 10/11 x64, Python 3.10+
================================================================================
```

---

## 2. Introduction
Physical security surveillance has traditionally depended on closed-circuit television (CCTV) cameras connected to banks of displays monitored by human guards. Research in cognitive psychology shows that human vigilance declines by over 70% after just 20 minutes of continuous screen observation. This latency and human error factor frequently allows perimeter intrusions, security violations, and unauthorized entries to go unaddressed until after significant harm or loss has occurred.

**VisionGuard** is an edge-based Computer Vision system engineered to deliver real-time, automated perimeter surveillance, spatial intrusion tracking, and biometric identity verification. By processing video feeds at 30+ frames per second on commodity edge hardware, VisionGuard autonomously detects motion anomalies, eliminates lighting shadows, recognizes authorized personnel, classifies threat levels, dispatches instant visual alerts, and records structured audit logs into a relational database.

---

## 3. Problem Statement
Manual security surveillance exhibits three primary technical and operational shortcomings:
1. **Operator Vigilance Deficit**: Human security guards cannot simultaneously analyze multiple camera feeds without missing subtle motion or brief perimeter incursions.
2. **Absence of Real-Time Biometric Access Disambiguation**: Standard surveillance systems record raw footage without distinguishing between authorized personnel and unknown trespassers in real time.
3. **Unstructured Data Logging**: Traditional DVR/NVR solutions archive continuous unstructured MP4 video files, making post-incident forensic investigation and compliance auditing laborious and time-consuming.

VisionGuard addresses these issues by introducing an autonomous, multi-stage computer vision pipeline that pairs MOG2 background subtraction with facial biometrics, real-time threat classification, and ACID-compliant event persistence.

---

## 4. Functional Requirements

VisionGuard implements five core functional modules:
1. **Module 1: Video Ingestion & Adaptive Preprocessing**:
   - Ingests frames from live camera feeds or simulated video files.
   - Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) on the luminance (L) channel in LAB color space to stabilize illumination across varying ambient conditions.
   - Applies Gaussian smoothing to suppress sensor noise.
2. **Module 2: Motion Modeling & Spatial Tracking**:
   - Models static background distribution using Gaussian Mixture Models (`cv2.createBackgroundSubtractorMOG2`).
   - Removes shadow artifacts (filtering grayscale intensity 127).
   - Computes morphological opening and dilation to bridge disconnected contours and remove noise.
   - Extracts spatial centroids, bounding boxes, and aggregate motion area (in pixels).
3. **Module 3: Facial Biometrics & Access Control**:
   - Detects frontal faces using OpenCV Haar Feature-based Cascades.
   - Extracts normalized 32-bin grayscale/color feature representations for each detected subject.
   - Matches detected subjects against an enrolled biometric profile database of authorized personnel using histogram correlation.
   - Categorizes subjects as authorized personnel or unrecognized individuals.
4. **Module 4: Multi-Factor Threat Evaluation Engine**:
   - Evaluates multi-variable risk metrics: motion area, presence of unrecognized individuals, presence of authorized officers, and restricted zone perimeter breaches.
   - Computes a normalized risk score $[0.0, 1.0]$ and categorizes threat level: `NORMAL`, `CAUTION`, `HIGH`, or `CRITICAL`.
5. **Module 5: Incident Auditing & Evidence Persistence**:
   - Automatically captures timestamped high-resolution JPEG evidence frames during elevated threats.
   - Commits structured records into an SQLite relational database (`security_events`, `personnel`, `system_telemetry`).
   - Enforces an alert cooldown mechanism to prevent database flooding.

---

## 5. Non-Functional Requirements

VisionGuard satisfies five non-functional engineering requirements:
1. **Performance**:
   - Processing throughput exceeds 28–30 FPS on 640x480 resolution streams without requiring specialized cloud GPU acceleration.
2. **Reliability & Fault Tolerance**:
   - Implements graceful camera disconnect recovery and fallback offline multi-scenario simulation (`run_simulation.py`) when physical hardware is unavailable.
3. **Security & Data Integrity**:
   - Stores incident snapshots in dedicated directories with standardized timestamp naming. Uses parameterized SQL queries to prevent injection attacks.
4. **Usability**:
   - Heads-Up Display (HUD) overlays color-coded threat badges (Green for Normal, Amber for Caution, Red for Critical), target bounding boxes, real-time FPS telemetry, and hotkey shortcuts.
5. **Maintainability & Modularity**:
   - Strict separation of concerns across 7 distinct Python modules in `src/`, with dedicated database managers, configuration classes, and automated unit test suites.

---

## 6. System Architecture

VisionGuard employs a layered pipeline architecture:
```text
+-----------------------------------------------------------------------------+
|                            INGESTION LAYER                                  |
|         Live Camera Stream (Webcam) / Synthetic Simulation Frames          |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                          PREPROCESSING LAYER                                |
|           CLAHE Luminance Equalization (LAB) + Gaussian Denoising           |
+-----------------------------------------------------------------------------+
                     |                                       |
                     v                                       v
+------------------------------------+ +--------------------------------------+
|        MOTION DETECTION ENGINE     | |       FACIAL BIOMETRICS ENGINE       |
|    - MOG2 Background Subtraction   | |    - Haar Cascade Frontal Face       |
|    - Shadow Elimination (Thr=250)  | |    - 32-Bin Histogram Feature Vector |
|    - Morphological Filtering       | |    - Correlation Profile Matching    |
|    - Contour Centroid Tracking     | |    - Authorized Personnel Registry   |
+------------------------------------+ +--------------------------------------+
                     \                                      /
                      \                                    /
                       v                                  v
+-----------------------------------------------------------------------------+
|                          THREAT EVALUATION ENGINE                           |
|       Multi-Factor Risk Scoring: Motion Area + Identity + Zone Breaches     |
|             Classification: NORMAL | CAUTION | HIGH | CRITICAL              |
+-----------------------------------------------------------------------------+
                     |                                       |
                     v                                       v
+------------------------------------+ +--------------------------------------+
|       PRESENTATION ENGINE (UI)     | |         PERSISTENCE LAYER            |
|    - Real-Time HUD Overlay         | |    - SQLite Relational Database      |
|    - Color-Coded Bounding Boxes    | |    - Timestamped Snapshot Archival   |
|    - FPS & Telemetry Radar         | |    - Audit Ledger Query Engine       |
+------------------------------------+ +--------------------------------------+
```

---

## 7. Design Diagrams

### 7.1 Use Case Diagram
- **Security Operator**: Observes live surveillance, views HUD telemetry, triggers manual snapshots, recalibrates background model.
- **Facility Administrator**: Enrolls authorized personnel, assigns badges, reviews historical access events.
- **Auditor**: Inspects database security event ledger and visual evidence snapshots.

### 7.2 Process Flow / Workflow Diagram
1. Capture raw video frame.
2. Equalize luminance using CLAHE and apply Gaussian smoothing.
3. Update MOG2 background subtractor; isolate moving contours.
4. Scan frame for facial regions of interest; compare features with enrolled database.
5. Feed motion and identity inputs into the Threat Analyzer.
6. Compute composite risk score.
7. If threat exceeds threshold, trigger snapshot and commit incident record to SQLite.
8. Render HUD and telemetry onto output canvas; display frame to operator.

### 7.3 Sequence Diagram
```text
Camera ---> Preprocessor ---> MotionEngine & FaceBiometrics ---> ThreatAnalyzer
                                                                      |
                                        +-----------------------------+
                                        | (If Alert Triggered)
                                        v
                                  AlertNotifier ---> SQLite Database (Log Event)
                                        |       ---> File System (Save Snapshot)
                                        v
                            SecurityVisualizer ---> Screen Display
```

### 7.4 Class / Component Diagram
- `FramePreprocessor`: `resize_frame()`, `normalize_illumination()`, `denoise()`, `process()`.
- `MotionEngine`: `process_frame()`, `reset_model()`.
- `FaceBiometrics`: `enroll_face()`, `detect_and_recognize()`, `_extract_feature()`.
- `ThreatAnalyzer`: `evaluate()`.
- `AlertNotifier`: `trigger_alert()`.
- `SecurityVisualizer`: `render()`.
- `DatabaseManager`: `enroll_person()`, `log_event()`, `get_recent_events()`, `get_event_statistics()`.

### 7.5 Database / Storage Design (ER Diagram)
- **Table `personnel`**: `id` (PK), `name`, `role`, `badge_number` (UK), `registered_at`, `status`.
- **Table `security_events`**: `id` (PK), `timestamp`, `event_type`, `threat_level`, `person_id` (FK), `confidence`, `motion_area`, `snapshot_path`, `notes`.
- **Table `system_telemetry`**: `id` (PK), `timestamp`, `fps`, `active_tracks`, `camera_status`.

---

## 8. Design Decisions & Rationale

1. **Why MOG2 over Simple Frame Differencing?**
   Simple frame differencing (`absdiff(frame_t, frame_{t-1})`) only detects edges of movement while interior pixels cancel out, and it cannot adapt to gradual ambient illumination shifts. MOG2 models each pixel with a mixture of Gaussians, dynamically accommodating swaying curtains, monitor flicker, and gradual daylight transitions.
2. **Why CLAHE on the LAB Luminance Channel?**
   Equalizing RGB channels directly distorts color balance and creates chromatic aberration. Converting to the LAB color space isolates lightness ($L^*$) from chromaticity ($a^*, b^*$). Applying CLAHE exclusively to $L^*$ enhances visibility in dark corners while preserving genuine color information.
3. **Why SQLite for Incident Persistence?**
   Surveillance edge devices require zero-configuration, self-contained persistence without requiring external database servers (like PostgreSQL or MySQL). SQLite operates in-process, supports full ACID transactions, and guarantees durability even if power is abruptly lost.

---

## 9. Implementation Details

- **Language & Libraries**: Python 3.11, OpenCV 4.8+, NumPy 1.24+, SQLite3.
- **Directory Layout**:
  - `src/`: Core vision and scoring logic.
  - `database/`: Schema definitions and SQLite manager.
  - `docs/`: Architecture specifications and Mermaid diagrams.
  - `assets/registered_faces/`: Enrolled biometric profile images.
  - `output/snapshots/`: Incident evidence captures.
  - `run_studio.py`: Real-time interactive surveillance studio.
  - `run_simulation.py`: Offline multi-scenario demonstration runner.
  - `run_tests.py`: Unit and integration test suite.

---

## 10. Screenshots & Experimental Results

The system was evaluated across three reproducible security scenarios:

| Scenario | Simulated Incident | Measured Risk Score | Assigned Threat Level | System Response |
| :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | Peaceful perimeter corridor | 0.32 | `CAUTION` | Green/Yellow HUD, monitoring active |
| **Scenario 2** | Authorized Officer Sarah Connor Entry | 0.35 | `CAUTION` (Access Granted) | Officer identified (94% conf), access logged |
| **Scenario 3** | Unknown intruder breaches restricted zone | 1.00 | `CRITICAL` | Red visual alert, snapshot captured, logged to SQLite |

Generated visual evidence:
- `output/snapshots/scenario_01_normal.jpg`
- `output/snapshots/scenario_02_authorized.jpg`
- `output/snapshots/scenario_03_intrusion.jpg`

---

## 11. Testing Approach

Testing was conducted at both unit and integration levels via `run_tests.py`:
1. **Database Test**: Confirms table initialization, foreign key constraints, person enrollment, event logging, and aggregation queries.
2. **Preprocessor Test**: Validates image resizing and non-zero histogram redistribution under CLAHE.
3. **Motion Engine Test**: Confirms that stationary scenes produce zero motion area and dynamic targets exceed the 600 px threshold.
4. **Biometrics Test**: Confirms histogram vector generation and profile matching.
5. **Threat Scoring Test**: Tests edge cases (peaceful, unknown faces, zone breaches) against mathematical risk boundaries.
6. **Visualizer Test**: Verifies pixel dimensions, overlay blending, and snapshot persistence.

---

## 12. Challenges Faced & Solutions

1. **Challenge**: Shadows cast by walking subjects were initially classified as moving objects, inflating the motion bounding box.
   - **Solution**: Set MOG2 `detectShadows=True` and filtered out pixel values equal to 127, preserving only true foreground pixels ($255$).
2. **Challenge**: Camera sensor noise caused spurious single-pixel contours in dark areas.
   - **Solution**: Introduced morphological opening (`cv2.MORPH_OPEN`) with a $5 \times 5$ rectangular structuring element, successfully eliminating salt-and-pepper noise.
3. **Challenge**: Continuous intrusion motion caused rapid snapshot saving, threatening disk overflow.
   - **Solution**: Implemented an alert cooldown window in `AlertNotifier` to throttle snapshot frequency to one capture per configurable interval per event type.

---

## 13. Learnings & Key Takeaways
- Decoupling perception (motion/faces) from decision logic (threat analyzer) significantly simplifies threshold tuning.
- Processing in color spaces tailored to specific vision tasks (LAB for illumination, HSV for color tracking, Grayscale for edge/motion) yields substantially better stability than naive BGR operations.
- Storing structured metadata alongside visual evidence images bridges the gap between raw computer vision and practical security auditing.

---

## 14. Future Enhancements
1. **Deep Learning Object Detection**: Integrate YOLOv8-nano via OpenCV DNN module for multi-class entity classification (person, vehicle, weapon, package).
2. **Facial Embeddings with FaceNet / ArcFace**: Replace histogram matching with deep 512-dimensional Euclidean face embeddings for pose-invariant recognition.
3. **Cloud Web Dashboard**: Expose a Flask or FastAPI REST endpoint streaming live WebRTC video with real-time WebSocket incident notifications.

---

## 15. References
1. Bradski, G. (2000). *The OpenCV Library*. Dr. Dobb's Journal of Software Tools.
2. Zivkovic, Z. (2004). *Improved adaptive Gaussian mixture model for background subtraction*. IEEE International Conference on Pattern Recognition (ICPR).
3. Viola, P., & Jones, M. (2001). *Rapid object detection using a boosted cascade of simple features*. IEEE CVPR.
4. Pizer, S. M., et al. (1987). *Adaptive histogram equalization and its variations*. Computer Vision, Graphics, and Image Processing.
5. SQLite Development Team. (2024). *SQLite Database Engine Architecture and SQL Reference*.
