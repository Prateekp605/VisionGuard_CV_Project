"""
VisionGuard Offline Multi-Scenario Simulation Runner.
Executes automated test sequences reproducing real-world security events:
1. Normal Secure Perimeter
2. Authorized Officer Access
3. Unauthorized Intruder Detection & Perimeter Breach
"""

import os
import time
import cv2
import numpy as np

from database.db_manager import DatabaseManager
from src.config import VisionConfig
from src.preprocessor import FramePreprocessor
from src.motion_engine import MotionEngine
from src.face_biometrics import FaceBiometrics
from src.threat_analyzer import ThreatAnalyzer
from src.alert_notifier import AlertNotifier
from src.visualizer import SecurityVisualizer


def create_security_environment() -> np.ndarray:
    """Renders a simulated corridor / checkpoint environment."""
    img = np.full((480, 640, 3), (225, 230, 235), dtype=np.uint8)
    # Floor perspective lines
    cv2.line(img, (0, 480), (220, 280), (180, 185, 190), 2)
    cv2.line(img, (640, 480), (420, 280), (180, 185, 190), 2)
    # Checkpoint door frame
    cv2.rectangle(img, (240, 160), (400, 420), (100, 110, 120), 3)
    cv2.rectangle(img, (250, 170), (390, 420), (140, 150, 160), -1)
    # Zone boundary line (Restricted Area)
    cv2.line(img, (120, 390), (520, 390), (0, 0, 220), 2)
    cv2.putText(
        img,
        "RESTRICTED ZONE PERIMETER",
        (180, 382),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (0, 0, 200),
        1,
        cv2.LINE_AA
    )
    return img


def draw_actor(frame: np.ndarray, x: int, y: int, is_officer: bool = False) -> np.ndarray:
    """Draws a stylized actor into the scene."""
    canvas = frame.copy()
    body_color = (180, 80, 30) if is_officer else (40, 40, 160)
    skin_color = (190, 210, 240)

    # Torso
    cv2.rectangle(canvas, (x - 28, y - 20), (x + 28, y + 60), body_color, -1)
    # Head
    cv2.circle(canvas, (x, y - 50), 26, skin_color, -1)
    cv2.circle(canvas, (x, y - 50), 26, (100, 120, 140), 2)
    # Face details (eyes)
    cv2.circle(canvas, (x - 9, y - 54), 4, (40, 20, 10), -1)
    cv2.circle(canvas, (x + 9, y - 54), 4, (40, 20, 10), -1)
    # Mouth
    cv2.line(canvas, (x - 8, y - 38), (x + 8, y - 38), (60, 60, 150), 2)

    if is_officer:
        # Officer badge
        cv2.circle(canvas, (x + 12, y), 6, (0, 215, 255), -1)

    return canvas


def run_simulation():
    print("=========================================================")
    print("       VISIONGUARD AUTONOMOUS SIMULATION RUNNER          ")
    print("=========================================================")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    snapshots_dir = os.path.join(output_dir, "snapshots")
    reports_dir = os.path.join(output_dir, "reports")
    faces_dir = os.path.join(base_dir, "assets", "registered_faces")

    os.makedirs(snapshots_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(faces_dir, exist_ok=True)

    # Initialize modules
    cfg = VisionConfig()
    db = DatabaseManager(os.path.join(base_dir, "database", "vision_guard.db"))
    preprocessor = FramePreprocessor((cfg.FRAME_WIDTH, cfg.FRAME_HEIGHT))
    motion_engine = MotionEngine(cfg)
    face_biometrics = FaceBiometrics(cfg, faces_dir=faces_dir)
    threat_analyzer = ThreatAnalyzer(cfg)
    alert_notifier = AlertNotifier(db, snapshot_dir=snapshots_dir, cooldown_seconds=0.0)
    visualizer = SecurityVisualizer(cfg)

    # 1. Enroll Authorized Officer
    print("[Enrollment] Registering Authorized Officer 'Sarah Connor' (Badge SEC-007)...")
    officer_id = db.enroll_person("Sarah Connor", "Security Lead", "SEC-007")

    # Generate reference face profile
    ref_face = np.full((120, 120, 3), (190, 210, 240), dtype=np.uint8)
    cv2.circle(ref_face, (60, 60), 40, (170, 195, 230), -1)
    cv2.circle(ref_face, (45, 52), 5, (40, 20, 10), -1)
    cv2.circle(ref_face, (75, 52), 5, (40, 20, 10), -1)
    cv2.line(ref_face, (50, 75), (70, 75), (50, 50, 160), 2)
    face_biometrics.enroll_face("Sarah Connor", ref_face)
    print("             -> Authorized personnel profile registered in database & biometrics.")

    base_env = create_security_environment()

    # Warm up background subtractor
    for _ in range(15):
        motion_engine.process_frame(base_env)

    # -------------------------------------------------------------
    # Scenario 1: Perimeter Normal
    # -------------------------------------------------------------
    print("\n[Scenario 1/3] Evaluating Peaceful Secure Perimeter...")
    f1 = base_env.copy()
    processed_f1 = preprocessor.process(f1)
    _, m_det1, m_area1 = motion_engine.process_frame(processed_f1)
    f_det1 = face_biometrics.detect_and_recognize(processed_f1)
    threat1, score1, reasons1 = threat_analyzer.evaluate(m_area1, m_det1, f_det1)

    out1 = visualizer.render(
        frame=processed_f1,
        threat_level=threat1,
        risk_score=score1,
        reasons=reasons1,
        motion_detections=m_det1,
        face_detections=f_det1,
        fps=30.0
    )
    s1_path = os.path.join(snapshots_dir, "scenario_01_normal.jpg")
    cv2.imwrite(s1_path, out1)
    print(f"               -> Threat: {threat1} (Risk: {score1:.2f}) | Saved: {s1_path}")

    # -------------------------------------------------------------
    # Scenario 2: Authorized Officer Entry
    # -------------------------------------------------------------
    print("\n[Scenario 2/3] Simulating Authorized Officer Entry...")
    f2 = draw_actor(base_env, x=320, y=280, is_officer=True)
    processed_f2 = preprocessor.process(f2)
    _, m_det2, m_area2 = motion_engine.process_frame(processed_f2)

    # Simulated authorized detection
    f_det2 = [{
        "bbox": (294, 204, 52, 52),
        "identity": "Sarah Connor",
        "is_authorized": True,
        "confidence": 0.94
    }]
    threat2, score2, reasons2 = threat_analyzer.evaluate(m_area2, m_det2, f_det2)
    db.log_event(
        event_type="ACCESS_GRANTED",
        threat_level=threat2,
        person_id=officer_id,
        confidence=0.94,
        motion_area=m_area2,
        snapshot_path=None,
        notes="Authorized Officer Sarah Connor entered checkpoint."
    )

    out2 = visualizer.render(
        frame=processed_f2,
        threat_level=threat2,
        risk_score=score2,
        reasons=reasons2,
        motion_detections=m_det2,
        face_detections=f_det2,
        fps=29.2
    )
    s2_path = os.path.join(snapshots_dir, "scenario_02_authorized.jpg")
    cv2.imwrite(s2_path, out2)
    print(f"               -> Threat: {threat2} (Risk: {score2:.2f}) | Access Granted | Saved: {s2_path}")

    # -------------------------------------------------------------
    # Scenario 3: Unauthorized Intruder Perimeter Breach
    # -------------------------------------------------------------
    print("\n[Scenario 3/3] Simulating Unauthorized Intruder in Restricted Zone...")
    f3 = draw_actor(base_env, x=220, y=410, is_officer=False)
    processed_f3 = preprocessor.process(f3)
    _, m_det3, m_area3 = motion_engine.process_frame(processed_f3)

    f_det3 = [{
        "bbox": (194, 334, 52, 52),
        "identity": "Unrecognized Subject",
        "is_authorized": False,
        "confidence": 0.18
    }]
    threat3, score3, reasons3 = threat_analyzer.evaluate(
        motion_area=m_area3,
        motion_detections=m_det3,
        face_detections=f_det3,
        restricted_zone_breach=True
    )

    out3 = visualizer.render(
        frame=processed_f3,
        threat_level=threat3,
        risk_score=score3,
        reasons=reasons3,
        motion_detections=m_det3,
        face_detections=f_det3,
        fps=28.7
    )
    s3_path = os.path.join(snapshots_dir, "scenario_03_intrusion.jpg")
    cv2.imwrite(s3_path, out3)

    alert_path = alert_notifier.trigger_alert(
        event_type="RESTRICTED_ZONE_INTRUSION",
        threat_level=threat3,
        frame=out3,
        confidence=0.89,
        motion_area=m_area3,
        notes="Unrecognized individual breached perimeter boundary in sector 4."
    )
    print(f"               -> Threat: {threat3} (Risk: {score3:.2f}) | Incident Logged to SQLite!")
    print(f"               -> Saved Snapshot: {s3_path}")

    # Aggregation check
    stats = db.get_event_statistics()
    recent = db.get_recent_events(limit=3)

    print("\n=========================================================")
    print("               DATABASE AUDIT VERIFICATION               ")
    print("=========================================================")
    print(f"Total Logged Events: {stats['total_events']}")
    print(f"High / Critical Threats: {stats['high_threats']}")
    print(f"Registered Personnel: {stats['registered_personnel']}")
    print("\nRecent Event Ledger:")
    for ev in recent:
        print(f"  [{ev['timestamp']}] ID={ev['id']} | Type={ev['event_type']} | Threat={ev['threat_level']} | Notes={ev['notes']}")
    print("=========================================================\n")


if __name__ == "__main__":
    run_simulation()
