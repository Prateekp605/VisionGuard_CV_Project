"""
Multi-factor security threat evaluation and risk scoring engine.
"""

from typing import List, Dict, Any, Tuple
from .config import VisionConfig


class ThreatAnalyzer:
    """Assesses live telemetry and classifies operational threat levels."""

    def __init__(self, config: VisionConfig = VisionConfig()):
        self.config = config

    def evaluate(
        self,
        motion_area: int,
        motion_detections: List[Dict[str, Any]],
        face_detections: List[Dict[str, Any]],
        restricted_zone_breach: bool = False
    ) -> Tuple[str, float, List[str]]:
        """
        Evaluates risk factors and determines composite threat level.

        Returns:
            threat_level: NORMAL, CAUTION, HIGH, or CRITICAL.
            risk_score: Numerical score [0.0 - 1.0].
            reasons: List of human-readable trigger causes.
        """
        reasons = []
        score = 0.0

        # Factor 1: Unrecognized individuals detected
        unrecognized_count = sum(1 for f in face_detections if not f["is_authorized"])
        authorized_count = sum(1 for f in face_detections if f["is_authorized"])

        if unrecognized_count > 0:
            score += 0.45 * unrecognized_count
            reasons.append(f"{unrecognized_count} unrecognized person(s) in frame")

        if authorized_count > 0:
            score = max(0.0, score - 0.20 * authorized_count)
            reasons.append(f"{authorized_count} authorized personnel present")

        # Factor 2: Significant perimeter motion
        if motion_area >= self.config.MIN_CONTOUR_AREA:
            motion_severity = min(0.35, (motion_area / 15000.0) * 0.35)
            score += motion_severity
            reasons.append(f"Perimeter motion detected ({motion_area} px)")

        # Factor 3: Restricted perimeter intrusion
        if restricted_zone_breach:
            score += 0.50
            reasons.append("Restricted security zone breach!")

        score = min(1.0, max(0.0, score))

        # Categorize threat
        if score >= 0.75 or restricted_zone_breach:
            threat_level = self.config.THREAT_CRITICAL
        elif score >= 0.45 or unrecognized_count > 0:
            threat_level = self.config.THREAT_HIGH
        elif score >= 0.15 or motion_area >= self.config.MIN_CONTOUR_AREA:
            threat_level = self.config.THREAT_CAUTION
        else:
            threat_level = self.config.THREAT_NORMAL
            if not reasons:
                reasons.append("Perimeter secure")

        return threat_level, score, reasons
