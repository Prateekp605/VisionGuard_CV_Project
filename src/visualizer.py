"""
Visual presentation engine: renders security HUD, threat badges,
colored detection bounding boxes, and system performance metrics.
"""

from typing import List, Dict, Any
import cv2
import numpy as np
from .config import VisionConfig


class SecurityVisualizer:
    """Renders real-time telemetry and overlays on top of video frames."""

    def __init__(self, config: VisionConfig = VisionConfig()):
        self.config = config

    def render(
        self,
        frame: np.ndarray,
        threat_level: str,
        risk_score: float,
        reasons: List[str],
        motion_detections: List[Dict[str, Any]],
        face_detections: List[Dict[str, Any]],
        fps: float,
        system_status: str = "LIVE SURVEILLANCE"
    ) -> np.ndarray:
        """Draws all security annotations and HUD onto frame."""
        canvas = frame.copy()
        h, w = canvas.shape[:2]

        # 1. Select theme color based on threat level
        if threat_level in (self.config.THREAT_CRITICAL, self.config.THREAT_HIGH):
            badge_color = self.config.COLOR_DANGER
        elif threat_level == self.config.THREAT_CAUTION:
            badge_color = self.config.COLOR_WARNING
        else:
            badge_color = self.config.COLOR_SAFE

        # 2. Draw Motion Bounding Boxes
        for m in motion_detections:
            x, y, mw, mh = m["bbox"]
            cv2.rectangle(canvas, (x, y), (x + mw, y + mh), (255, 140, 0), 1)
            cv2.putText(
                canvas,
                "MOTION",
                (x, max(15, y - 4)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.38,
                (255, 140, 0),
                1,
                cv2.LINE_AA
            )

        # 3. Draw Face Bounding Boxes & Badges
        for f in face_detections:
            x, y, fw, fh = f["bbox"]
            is_auth = f["is_authorized"]
            box_color = self.config.COLOR_SAFE if is_auth else self.config.COLOR_DANGER
            cv2.rectangle(canvas, (x, y), (x + fw, y + fh), box_color, 2)

            label = f"{f['identity']} ({int(f['confidence'] * 100)}%)"
            # Badge background
            cv2.rectangle(canvas, (x, y - 22), (x + len(label) * 9 + 10, y), box_color, -1)
            cv2.putText(
                canvas,
                label,
                (x + 5, y - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        # 4. Draw Header Overlay Bar
        overlay = canvas.copy()
        cv2.rectangle(overlay, (0, 0), (w, 48), self.config.COLOR_HUD_BG, -1)
        # Footer Bar
        cv2.rectangle(overlay, (0, h - 32), (w, h), self.config.COLOR_HUD_BG, -1)
        alpha = 0.78
        cv2.addWeighted(overlay, alpha, canvas, 1 - alpha, 0, canvas)

        # 5. Header Content
        # System title
        cv2.putText(
            canvas,
            "VISIONGUARD AI",
            (14, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            self.config.COLOR_ACCENT,
            2,
            cv2.LINE_AA
        )

        # Threat Badge
        threat_text = f"[{threat_level}] RISK: {int(risk_score * 100)}%"
        cv2.rectangle(canvas, (w // 2 - 120, 10), (w // 2 + 120, 38), badge_color, -1)
        cv2.putText(
            canvas,
            threat_text,
            (w // 2 - 105, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # FPS & Track counts
        telemetry_str = f"FPS: {fps:.1f} | OBJ: {len(motion_detections)}"
        cv2.putText(
            canvas,
            telemetry_str,
            (w - 180, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
            (200, 255, 200),
            1,
            cv2.LINE_AA
        )

        # 6. Secondary reason sub-banner if alert active
        if threat_level != self.config.THREAT_NORMAL and reasons:
            reason_str = " | ".join(reasons[:2])
            cv2.rectangle(canvas, (0, 48), (w, 70), (20, 20, 20), -1)
            cv2.putText(
                canvas,
                f"ALERT: {reason_str}",
                (14, 64),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                badge_color,
                1,
                cv2.LINE_AA
            )

        # 7. Footer Instructions
        footer_text = "[1] Toggle Feed  [S] Snapshot  [R] Reset Bg  [E] Enroll Face  [Q] Exit"
        cv2.putText(
            canvas,
            footer_text,
            (14, h - 11),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (210, 210, 210),
            1,
            cv2.LINE_AA
        )

        return canvas
