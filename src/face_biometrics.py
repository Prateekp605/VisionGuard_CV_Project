"""
Facial biometrics, identity enrollment, and verification module.
"""

import os
from typing import List, Dict, Any, Tuple
import cv2
import numpy as np
from .config import VisionConfig


class FaceBiometrics:
    """Handles face detection, feature representation, and enrolled database verification."""

    def __init__(self, config: VisionConfig = VisionConfig(), faces_dir: str = ""):
        self.config = config
        self.faces_dir = faces_dir

        cascade_dir = cv2.data.haarcascades
        self.face_cascade = cv2.CascadeClassifier(
            os.path.join(cascade_dir, "haarcascade_frontalface_default.xml")
        )
        self.eye_cascade = cv2.CascadeClassifier(
            os.path.join(cascade_dir, "haarcascade_eye.xml")
        )

        # In-memory enrolled face profiles: {name: normalized_histogram_feature}
        self.enrolled_profiles: Dict[str, np.ndarray] = {}
        self._load_enrolled_faces()

    def _extract_feature(self, face_crop: np.ndarray) -> np.ndarray:
        """
        Computes normalized HSV and Grayscale color histograms
        as a fast, robust biometric representation vector.
        """
        resized = cv2.resize(face_crop, (96, 96))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
        return cv2.normalize(hist, hist).flatten()

    def _load_enrolled_faces(self):
        """Loads and indexes enrolled reference photos."""
        if not self.faces_dir or not os.path.exists(self.faces_dir):
            return

        for fname in os.listdir(self.faces_dir):
            if fname.lower().endswith((".jpg", ".png", ".jpeg")):
                name = os.path.splitext(fname)[0].replace("_", " ").title()
                img_path = os.path.join(self.faces_dir, fname)
                img = cv2.imread(img_path)
                if img is not None:
                    # Detect face in reference image
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    if len(faces) > 0:
                        x, y, w, h = faces[0]
                        crop = img[y : y + h, x : x + w]
                    else:
                        crop = img
                    self.enrolled_profiles[name] = self._extract_feature(crop)

    def enroll_face(self, name: str, face_img: np.ndarray) -> bool:
        """Enrolls a new authorized identity into the memory index and disk."""
        feature = self._extract_feature(face_img)
        self.enrolled_profiles[name] = feature
        if self.faces_dir:
            os.makedirs(self.faces_dir, exist_ok=True)
            save_name = f"{name.lower().replace(' ', '_')}.jpg"
            cv2.imwrite(os.path.join(self.faces_dir, save_name), face_img)
        return True

    def detect_and_recognize(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detects faces in frame and compares against enrolled biometric profiles.

        Returns:
            List of detected face dicts with bounding boxes, identity, and match confidence.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_eq = cv2.equalizeHist(gray)

        faces = self.face_cascade.detectMultiScale(
            gray_eq,
            scaleFactor=self.config.FACE_SCALE_FACTOR,
            minNeighbors=self.config.FACE_MIN_NEIGHBORS,
            minSize=self.config.FACE_MIN_SIZE
        )

        results = []
        for (x, y, w, h) in faces:
            face_roi = frame[y : y + h, x : x + w]
            feature = self._extract_feature(face_roi)

            best_match = "Unknown"
            best_score = 0.0

            for name, enrolled_feat in self.enrolled_profiles.items():
                # Compare histograms using Bhattacharyya distance / correlation
                score = cv2.compareHist(feature, enrolled_feat, cv2.HISTCMP_CORREL)
                if score > best_score:
                    best_score = score
                    best_match = name

            is_authorized = (best_score >= self.config.MATCH_CONFIDENCE_THRESHOLD)
            identity = best_match if is_authorized else "Unrecognized Subject"

            results.append({
                "bbox": (x, y, w, h),
                "identity": identity,
                "is_authorized": is_authorized,
                "confidence": float(best_score),
                "crop": face_roi
            })

        return results
