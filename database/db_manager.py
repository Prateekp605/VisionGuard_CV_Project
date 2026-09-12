"""
Database manager for VisionGuard security surveillance platform.
Handles SQLite storage, personnel enrollment, and incident audit logging.
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """Manages persistent SQLite operations for VisionGuard."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base, "database", "vision_guard.db")
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
        if os.path.exists(schema_file):
            with open(schema_file, "r", encoding="utf-8") as f:
                schema_content = f.read()
            with self._get_connection() as conn:
                conn.executescript(schema_content)
                conn.commit()

    def enroll_person(self, name: str, role: str, badge_number: str) -> int:
        """Enrolls an authorized individual in the personnel registry."""
        query = """
            INSERT INTO personnel (name, role, badge_number)
            VALUES (?, ?, ?)
            ON CONFLICT(badge_number) DO UPDATE SET name=excluded.name, role=excluded.role
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, role, badge_number))
            conn.commit()
            return cursor.lastrowid

    def log_event(
        self,
        event_type: str,
        threat_level: str,
        person_id: Optional[int] = None,
        confidence: float = 0.0,
        motion_area: int = 0,
        snapshot_path: Optional[str] = None,
        notes: str = ""
    ) -> int:
        """Logs a security event to the audit ledger."""
        query = """
            INSERT INTO security_events 
            (event_type, threat_level, person_id, confidence, motion_area, snapshot_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (event_type, threat_level, person_id, confidence, motion_area, snapshot_path, notes)
            )
            conn.commit()
            return cursor.lastrowid

    def log_telemetry(self, fps: float, active_tracks: int = 0, camera_status: str = "OK"):
        """Records runtime frame rate and track telemetry."""
        query = "INSERT INTO system_telemetry (fps, active_tracks, camera_status) VALUES (?, ?, ?)"
        with self._get_connection() as conn:
            conn.execute(query, (fps, active_tracks, camera_status))
            conn.commit()

    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves most recent security incidents."""
        query = """
            SELECT e.id, e.timestamp, e.event_type, e.threat_level, e.confidence, 
                   e.motion_area, e.snapshot_path, e.notes, p.name as person_name, p.role as person_role
            FROM security_events e
            LEFT JOIN personnel p ON e.person_id = p.id
            ORDER BY e.id DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query, (limit,)).fetchall()
            return [dict(row) for row in rows]

    def get_event_statistics(self) -> Dict[str, Any]:
        """Calculates aggregated statistics across logged security events."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            total_events = cursor.execute("SELECT COUNT(*) FROM security_events").fetchone()[0]
            intrusions = cursor.execute(
                "SELECT COUNT(*) FROM security_events WHERE threat_level IN ('HIGH', 'CRITICAL')"
            ).fetchone()[0]
            personnel_count = cursor.execute("SELECT COUNT(*) FROM personnel").fetchone()[0]
            return {
                "total_events": total_events,
                "high_threats": intrusions,
                "registered_personnel": personnel_count
            }
