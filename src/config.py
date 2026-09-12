"""
Configuration constants, color palettes, and operational thresholds for VisionGuard.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class VisionConfig:
    # Camera settings
    CAMERA_INDEX: int = 0
    FRAME_WIDTH: int = 640
    FRAME_HEIGHT: int = 480
    TARGET_FPS: int = 30

    # Motion detection thresholds
    MIN_CONTOUR_AREA: int = 600          # Minimum pixel area for motion detection
    MOG2_HISTORY: int = 400              # Number of frames for background model
    MOG2_VAR_THRESHOLD: int = 24         # Mahalanobis distance threshold
    LOITERING_DURATION_FRAMES: int = 45  # Frames required to trigger loitering alert

    # Facial Biometrics
    FACE_MIN_SIZE: tuple = (50, 50)
    FACE_SCALE_FACTOR: float = 1.15
    FACE_MIN_NEIGHBORS: int = 5
    MATCH_CONFIDENCE_THRESHOLD: float = 0.65

    # Threat Levels
    THREAT_NORMAL: str = "NORMAL"
    THREAT_CAUTION: str = "CAUTION"
    THREAT_HIGH: str = "HIGH"
    THREAT_CRITICAL: str = "CRITICAL"

    # UI Color Palettes (BGR)
    COLOR_SAFE: tuple = (40, 200, 60)       # Vibrant Green
    COLOR_WARNING: tuple = (0, 200, 255)    # Amber Yellow
    COLOR_DANGER: tuple = (40, 40, 240)     # High Alert Red
    COLOR_ACCENT: tuple = (255, 180, 0)     # Electric Cyan/Blue
    COLOR_HUD_BG: tuple = (18, 20, 24)      # Dark Matte Surface
    COLOR_WHITE: tuple = (245, 245, 245)
