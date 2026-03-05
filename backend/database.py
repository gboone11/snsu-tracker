import json
import os
import sqlite3
from calendar import monthrange
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional


class Database:
    def __init__(self, db_path: Optional[str] = None) -> None:
        """sets up database and populates path attribute

        :param Optional[str] db_path: path where database is located, defaults to None
        """
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), "..", "database", "snsu_tracker.db"
            )
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def get_connection(self):
        """facilitates connection to db

        :yield ConnectionObject: connection to db
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        """creates tables in db if not already made."""
        with self.get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS line_groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    target_ready_time TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS lines (
                    line_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    line_number TEXT UNIQUE NOT NULL,
                    line_group_id INTEGER NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (line_group_id) REFERENCES line_groups(group_id)
                );
                
                CREATE TABLE IF NOT EXISTS process_steps (
                    step_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    step_order INTEGER NOT NULL,
                    team_name TEXT NOT NULL,
                    task_name TEXT NOT NULL,
                    avg_duration_minutes INTEGER,
                    is_active INTEGER DEFAULT 1,
                    FOREIGN KEY (group_id) REFERENCES line_groups(group_id)
                );
                
                CREATE TABLE IF NOT EXISTS runs (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    line_id INTEGER NOT NULL,
                    work_order_end_time TIMESTAMP,
                    target_ready_time TIMESTAMP,
                    actual_ready_time TIMESTAMP,
                    total_duration_minutes INTEGER,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (line_id) REFERENCES lines(line_id)
                );
                
                CREATE TABLE IF NOT EXISTS step_executions (
                    execution_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    step_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    duration_minutes INTEGER,
                    signed_by TEXT,
                    signed_at TIMESTAMP,
                    FOREIGN KEY (run_id) REFERENCES runs(run_id),
                    FOREIGN KEY (step_id) REFERENCES process_steps(step_id)
                );
                
                CREATE TABLE IF NOT EXISTS checklist_templates (
                    template_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_name TEXT NOT NULL,
                    task_name TEXT NOT NULL,
                    is_custom INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS checklist_items (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id INTEGER NOT NULL,
                    item_order INTEGER NOT NULL,
                    item_text TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    FOREIGN KEY (template_id) REFERENCES checklist_templates(template_id)
                );
                
                CREATE TABLE IF NOT EXISTS checklist_completions (
                    completion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL,
                    is_completed INTEGER DEFAULT 0,
                    completed_by TEXT,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (execution_id) REFERENCES step_executions(execution_id),
                    FOREIGN KEY (item_id) REFERENCES checklist_items(item_id)
                );
                
                CREATE TABLE IF NOT EXISTS communication_notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    line_id INTEGER NOT NULL,
                    run_id INTEGER,
                    note_text TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (line_id) REFERENCES lines(line_id),
                    FOREIGN KEY (run_id) REFERENCES runs(run_id)
                );
                
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    initials TEXT NOT NULL,
                    team_name TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_lines_group ON lines(line_group_id);
                CREATE INDEX IF NOT EXISTS idx_steps_group ON process_steps(group_id, step_order);
                CREATE INDEX IF NOT EXISTS idx_runs_line ON runs(line_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_executions_run ON step_executions(run_id, step_id);
                CREATE INDEX IF NOT EXISTS idx_notes_line ON communication_notes(line_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_checklist_template ON checklist_items(template_id, item_order);
            """
            )

    def clear_data(self) -> None:
        """Clear all data from tables"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM checklist_completions")
            conn.execute("DELETE FROM checklist_items")
            conn.execute("DELETE FROM checklist_templates")
            conn.execute("DELETE FROM step_executions")
            conn.execute("DELETE FROM communication_notes")
            conn.execute("DELETE FROM runs")
            conn.execute("DELETE FROM process_steps")
            conn.execute("DELETE FROM lines")
            conn.execute("DELETE FROM line_groups")
            conn.execute("DELETE FROM users")

    def get_all_line_groups(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM line_groups WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_all_lines(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM lines WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_process_steps(self, group_id: int) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM process_steps WHERE group_id = ? AND is_active = 1 ORDER BY step_order",
                (group_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_active_runs(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM runs WHERE status = 'active' ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_step_executions(self, run_id: int) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM step_executions WHERE run_id = ?",
                (run_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def create_user(self, username: str, full_name: str, initials: str, team_name: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, full_name, initials, team_name) VALUES (?, ?, ?, ?)",
                (username, full_name, initials, team_name)
            )
            return cursor.lastrowid

    def get_all_users(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        with self.get_connection() as conn:
            cursor = conn.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
            return cursor.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            return cursor.rowcount > 0

    def deactivate_user(self, user_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.execute("UPDATE users SET is_active = 0 WHERE user_id = ?", (user_id,))
            return cursor.rowcount > 0

