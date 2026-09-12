"""
VisionGuard Interactive Real-Time Surveillance Studio.
Connects to physical camera/webcam and runs live intrusion detection,
facial recognition, threat analysis, and database audit logging.
"""

import argparse
from datetime import datetime
import os
import sys
import time
import cv2

from database.db_manager import DatabaseManager
from src.config import VisionConfig
from src.preprocessor import FramePreprocessor
from src.motion_engine import MotionEngine
from src.face_biometrics import FaceBiometrics
from src.threat_analyzer import ThreatAnalyzer
from src.alert_notifier import AlertNotifier
from src.visualizer import SecurityVisualizer


def main():
    parser = argparse.ArgumentParser(description="VisionGuard AI Live Surveillance Studio")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--width", type=int, default=640, help="Capture width")
    parser.add_argument("--height", type=int, default=480, help="Capture height")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    snapshots_dir = os.path.join(base_dir, "output", "snapshots")
    faces_dir = os.path.join(base_dir, "assets", "registered_faces")
    db_path = os.path.join(base_dir, "database", "vision_guard.db")

    print("=======================================================")
    print("       VISIONGUARD REAL-TIME SURVEILLANCE STUDIO       ")
    print("=======================================================")
    print(f"Opening camera index [{args.camera}]...")

    cap = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(args.camera)

    if not cap.isOpened():
        print(f"[Error] Could not open camera {args.camera}.")
        print("Tip: If you do not have a physical webcam connected, run:")
        print("     -> python run_simulation.py")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    # Initialize components
    cfg = VisionConfig()
    db = DatabaseManager(db_path)
    preprocessor = FramePreprocessor((args.width, args.height))
    motion_engine = MotionEngine(cfg)
    face_biometrics = FaceBiometrics(cfg, faces_dir=faces_dir)
    threat_analyzer = ThreatAnalyzer(cfg)
    alert_notifier = AlertNotifier(db, snapshot_dir=snapshots_dir, cooldown_seconds=4.0)
    visualizer = SecurityVisualizer(cfg)

    # Warm-up background model with first few frames
    print("Calibrating background illumination...")
    for _ in range(10):
        ret, f = cap.read()
        if ret:
            processed = preprocessor.process(f)
            motion_engine.process_frame(processed)

    window_name = "VisionGuard AI Surveillance Studio (Press Q to exit)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    prev_time = time.time()
    overlay_mode = True

    print("\nStudio Controls:")
    print("  [1] Toggle Security HUD & Overlays")
    print("  [S] Save Manual Snapshot to output/snapshots/")
    print("  [R] Reset / Re-calibrate Background Model")
    print("  [E] Quick-Enroll Face in Frame as Authorized")
    print("  [Q] or [ESC] to Exit\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[Warning] Frame capture error. Exiting...")
                break

            # Calculate FPS
            curr_time = time.time()
            dt = curr_time - prev_time
            prev_time = curr_time
            fps = 1.0 / dt if dt > 0 else 30.0

            # 1. Preprocess
            clean_frame = preprocessor.process(frame)

            # 2. Motion Detection
            fg_mask, motion_detections, motion_area = motion_engine.process_frame(clean_frame)

            # 3. Face Biometrics
            face_detections = face_biometrics.detect_and_recognize(clean_frame)

            # 4. Threat Analysis
            threat_level, risk_score, reasons = threat_analyzer.evaluate(
                motion_area=motion_area,
                motion_detections=motion_detections,
                face_detections=face_detections
            )

            # 5. Dispatch Alert on High/Critical Threat
            if threat_level in (cfg.THREAT_HIGH, cfg.THREAT_CRITICAL):
                alert_notifier.trigger_alert(
                    event_type="UNAUTHORIZED_ACTIVITY",
                    threat_level=threat_level,
                    frame=clean_frame,
                    confidence=risk_score,
                    motion_area=motion_area,
                    notes="; ".join(reasons)
                )

            # 6. Render
            if overlay_mode:
                display_frame = visualizer.render(
                    frame=clean_frame,
                    threat_level=threat_level,
                    risk_score=risk_score,
                    reasons=reasons,
                    motion_detections=motion_detections,
                    face_detections=face_detections,
                    fps=fps
                )
            else:
                display_frame = clean_frame

            cv2.imshow(window_name, display_frame)

            # Hotkeys
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q"), 27):
                break
            elif key == ord("1"):
                overlay_mode = not overlay_mode
            elif key in (ord("r"), ord("R")):
                motion_engine.reset_model()
                print("[Action] Background model recalibrated.")
            elif key in (ord("s"), ord("S")):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                snap_path = os.path.join(snapshots_dir, f"manual_{ts}.jpg")
                cv2.imwrite(snap_path, display_frame)
                print(f"[Snapshot] Saved manual capture: {snap_path}")
            elif key in (ord("e"), ord("E")):
                if face_detections:
                    crop = face_detections[0].get("crop")
                    if crop is not None:
                        enroll_name = f"Personnel_{len(face_biometrics.enrolled_profiles) + 1}"
                        face_biometrics.enroll_face(enroll_name, crop)
                        db.enroll_person(enroll_name, "Registered Visitor", f"VIS-{int(time.time()) % 10000}")
                        print(f"[Enrollment] Registered current face as '{enroll_name}'")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("\nCamera released. VisionGuard terminated gracefully.")


if __name__ == "__main__":
    main()
