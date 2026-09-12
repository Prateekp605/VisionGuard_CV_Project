"""
Alert notification and incident snapshot dispatcher.
Persists critical events to disk and commits audit records to SQLite.
"""

import os
import time
from datetime import datetime
from typing import Optional, Dict, Any
import cv2
import numpy as np


class AlertNotifier:
    """Dispatches alerts, captures event snapshots, and writes database records."""

    def __init__(self, db_manager, snapshot_dir: str, cooldown_seconds: float = 3.0):
        self.db = db_manager
        self.snapshot_dir = snapshot_dir
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time: Dict[str, float] = {}
        os.makedirs(snapshot_dir, exist_ok=True)

    def trigger_alert(
        self,
        event_type: str,
        threat_level: str,
        frame: np.ndarray,
        confidence: float = 0.0,
        motion_area: int = 0,
        notes: str = ""
    ) -> Optional[str]:
        """
        Captures snapshot and logs event if outside cooldown window.

        Returns:
            snapshot_path if alert was dispatched, None if cooled down.
        """
        now = time.time()
        last_time = self.last_alert_time.get(event_type, 0.0)

        # Check cooldown to prevent filling storage with identical frames
        if (now - last_time) < self.cooldown_seconds:
            return None

        self.last_alert_time[event_type] = now

        # Save snapshot
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
        filename = f"incident_{event_type.lower()}_{timestamp_str}.jpg"
        filepath = os.path.join(self.snapshot_dir, filename)
        cv2.imwrite(filepath, frame)

        # Log into database
        self.db.log_event(
            event_type=event_type,
            threat_level=threat_level,
            confidence=confidence,
            motion_area=motion_area,
            snapshot_path=filepath,
            notes=notes
        )

        return filepath
