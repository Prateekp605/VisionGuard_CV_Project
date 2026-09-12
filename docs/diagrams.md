# VisionGuard System Architecture & Design Diagrams

## 1. System Architecture Diagram
```mermaid
graph TD
    subgraph Ingestion Layer
        CAM[Webcam / Video Feed] --> PRE[Frame Preprocessor: CLAHE & Gaussian Blur]
    end

    subgraph Perception Engine
        PRE --> ME[Motion Engine: MOG2 Background Subtractor]
        PRE --> FB[Face Biometrics: Haar Cascade & Histogram Extractor]
    end

    subgraph Intelligence & Scoring
        ME --> TA[Threat Analyzer: Rules Engine]
        FB --> TA
    end

    subgraph Presentation & Persistence
        TA --> VIS[Security Visualizer: HUD & Badges]
        TA --> AN[Alert Notifier: Snapshot Dispatcher]
        AN --> DB[(SQLite Database: Events & Personnel)]
        AN --> DISK[Disk Storage: Evidence Snapshots]
    end
```

## 2. Process Workflow Diagram
```mermaid
flowchart TD
    Start([Start Surveillance]) --> Capture[Capture Video Frame]
    Capture --> Preprocess[CLAHE Illumination Normalization & Denoising]
    Preprocess --> DetectMotion[MOG2 Background Differencing]
    DetectMotion --> DetectFaces[Haar Cascade Face Detection]
    DetectFaces --> BiometricMatch{Authorized in Database?}
    
    BiometricMatch -- Yes --> ThreatEval1[Threat Score: Low / Access Granted]
    BiometricMatch -- No --> ThreatEval2[Threat Score: High / Unrecognized Subject]
    
    ThreatEval1 --> CompositeRisk[Calculate Composite Risk Score]
    ThreatEval2 --> CompositeRisk
    
    CompositeRisk --> ThresholdCheck{Risk Score >= Threshold?}
    ThresholdCheck -- Yes --> DispatchAlert[Dispatch Visual Alert & Save Snapshot]
    ThresholdCheck -- No --> RenderHUD[Render Normal Security HUD]
    
    DispatchAlert --> LogDB[Log Security Event to SQLite]
    LogDB --> RenderHUD
    RenderHUD --> Display[Display Frame on Screen]
    Display --> CheckExit{User Pressed Q?}
    CheckExit -- No --> Capture
    CheckExit -- Yes --> End([Terminate Surveillance])
```

## 3. Use Case Diagram
```mermaid
graph LR
    actor1((Security Operator))
    actor2((Facility Administrator))
    actor3((System Auditor))

    subgraph VisionGuard System
        UC1[View Real-Time Video Stream]
        UC2[Monitor Threat Radar & HUD]
        UC3[Enroll Authorized Personnel]
        UC4[Receive Intrusion Alert Snapshots]
        UC5[Query Incident Event History]
        UC6[Recalibrate Background Model]
    end

    actor1 --> UC1
    actor1 --> UC2
    actor1 --> UC4
    actor1 --> UC6

    actor2 --> UC3
    actor2 --> UC5

    actor3 --> UC5
```

## 4. Sequence Diagram: Security Event Detection & Alerting
```mermaid
sequenceDiagram
    autonumber
    actor Target as Intruder
    participant Cam as Video Camera
    participant Pipe as Preprocessor
    participant Motion as MotionEngine
    participant Bio as FaceBiometrics
    participant Threat as ThreatAnalyzer
    participant Alert as AlertNotifier
    participant DB as SQLite DB
    participant UI as SecurityVisualizer

    Target->>Cam: Moves across perimeter
    Cam->>Pipe: Raw Frame (BGR)
    Pipe->>Motion: Preprocessed Frame
    Motion->>Threat: Motion Contours & Area (px)
    Pipe->>Bio: Face ROI
    Bio->>Threat: Unrecognized Subject Flag
    Threat->>Threat: Compute Risk Score (HIGH/CRITICAL)
    Threat->>Alert: Trigger Alert (Threat Level)
    Alert->>DB: INSERT INTO security_events
    Alert->>Alert: Save Snapshot to disk
    Threat->>UI: Render Danger Badges & Bounding Boxes
    UI-->>Cam: Display Annotated Feed
```

## 5. Entity-Relationship (ER) Diagram
```mermaid
erDiagram
    PERSONNEL ||--o{ SECURITY_EVENTS : "associated_with"
    
    PERSONNEL {
        int id PK
        string name
        string role
        string badge_number UK
        timestamp registered_at
        string status
    }

    SECURITY_EVENTS {
        int id PK
        timestamp timestamp
        string event_type
        string threat_level
        int person_id FK
        float confidence
        int motion_area
        string snapshot_path
        string notes
    }

    SYSTEM_TELEMETRY {
        int id PK
        timestamp timestamp
        float fps
        int active_tracks
        string camera_status
    }
```
