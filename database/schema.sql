-- VisionGuard Relational Schema for Security Surveillance
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS personnel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Staff',
    badge_number TEXT UNIQUE NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS security_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,          -- INTRUSION, MOTION_DETECTED, UNRECOGNIZED_PERSON, ACCESS_GRANTED
    threat_level TEXT NOT NULL,        -- NORMAL, CAUTION, HIGH, CRITICAL
    person_id INTEGER,
    confidence REAL DEFAULT 0.0,
    motion_area INTEGER DEFAULT 0,
    snapshot_path TEXT,
    notes TEXT,
    FOREIGN KEY(person_id) REFERENCES personnel(id)
);

CREATE TABLE IF NOT EXISTS system_telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fps REAL NOT NULL,
    active_tracks INTEGER DEFAULT 0,
    camera_status TEXT DEFAULT 'OK'
);
