"""
Video frame ingestion, illumination equalization, and noise filtering.
"""

import cv2
import numpy as np


class FramePreprocessor:
    """Prepares and enhances raw frames for optimal detection sensitivity."""

    def __init__(self, target_size: tuple = (640, 480)):
        self.target_size = target_size
        # Contrast Limited Adaptive Histogram Equalizer
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resizes frame to target dimensions while maintaining aspect ratio if needed."""
        h, w = frame.shape[:2]
        if (w, h) != self.target_size:
            return cv2.resize(frame, self.target_size, interpolation=cv2.INTER_LINEAR)
        return frame

    def normalize_illumination(self, frame: np.ndarray) -> np.ndarray:
        """
        Applies CLAHE on the luminance channel (LAB color space).
        Eliminates uneven shadow artifacts and low-contrast dim areas.
        """
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        enhanced_l = self.clahe.apply(l)
        enhanced_lab = cv2.merge((enhanced_l, a, b))
        return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    def denoise(self, frame: np.ndarray, ksize: int = 5) -> np.ndarray:
        """Applies Gaussian smoothing to suppress sensor noise."""
        if ksize % 2 == 0:
            ksize += 1
        return cv2.GaussianBlur(frame, (ksize, ksize), 0)

    def process(self, frame: np.ndarray) -> np.ndarray:
        """Full preprocessing pipeline: resize -> illumination correction -> denoise."""
        resized = self.resize_frame(frame)
        enhanced = self.normalize_illumination(resized)
        return self.denoise(enhanced)
