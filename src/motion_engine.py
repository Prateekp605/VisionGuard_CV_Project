"""
Motion detection, spatial contour extraction, and loitering analysis engine.
"""

from typing import List, Dict, Any, Tuple
import cv2
import numpy as np
from .config import VisionConfig


class MotionEngine:
    """Detects movement, analyzes spatial contours, and monitors loitering."""

    def __init__(self, config: VisionConfig = VisionConfig()):
        self.config = config
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=config.MOG2_HISTORY,
            varThreshold=config.MOG2_VAR_THRESHOLD,
            detectShadows=True
        )
        self.loitering_tracker: Dict[int, int] = {}
        self.frame_index = 0

    def reset_model(self):
        """Re-initializes the background model."""
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=self.config.MOG2_HISTORY,
            varThreshold=self.config.MOG2_VAR_THRESHOLD,
            detectShadows=True
        )
        self.loitering_tracker.clear()

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List[Dict[str, Any]], int]:
        """
        Extracts foreground motion mask and bounding regions.

        Returns:
            fg_mask: Cleaned binary mask of moving objects.
            detections: List of bounding boxes and centroids.
            total_motion_area: Aggregate area in pixels.
        """
        self.frame_index += 1
        # Extract raw foreground mask
        raw_mask = self.bg_subtractor.apply(frame)

        # Discard shadows (marked as 127 in MOG2)
        _, thresh = cv2.threshold(raw_mask, 250, 255, cv2.THRESH_BINARY)

        # Morphological opening and dilation to remove speckles and bridge fractured contours
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        dilated = cv2.dilate(cleaned, kernel, iterations=2)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        total_area = 0

        for c in contours:
            area = cv2.contourArea(c)
            if area >= self.config.MIN_CONTOUR_AREA:
                total_area += int(area)
                x, y, w, h = cv2.boundingRect(c)
                centroid = (x + w // 2, y + h // 2)

                detections.append({
                    "bbox": (x, y, w, h),
                    "centroid": centroid,
                    "area": int(area)
                })

        return dilated, detections, total_area
