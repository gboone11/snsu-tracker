import os
import sqlite3
from contextlib import contextmanager
from typing import Optional


class Database:
    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "database", "snsu_tracker.db"
            )
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self.get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS line_groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    target_ready_time TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS lines (
                    line_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    line_number TEXT UNIQUE NOT NULL,
                    line_group_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (line_group_id) REFERENCES line_groups(group_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS process_steps (
                    step_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    step_order INTEGER NOT NULL,
                    team_name TEXT NOT NULL,
                    task_name TEXT NOT NULL,
                    avg_duration_minutes INTEGER,
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
        with self.get_connection() as conn:
            conn.execute("DROP TABLE IF EXISTS checklist_completions")
            conn.execute("DROP TABLE IF EXISTS checklist_items")
            conn.execute("DROP TABLE IF EXISTS checklist_templates")
            conn.execute("DROP TABLE IF EXISTS step_executions")
            conn.execute("DROP TABLE IF EXISTS communication_notes")
            conn.execute("DROP TABLE IF EXISTS runs")
            conn.execute("DROP TABLE IF EXISTS process_steps")
            conn.execute("DROP TABLE IF EXISTS lines")
            conn.execute("DROP TABLE IF EXISTS line_groups")
            conn.execute("DROP TABLE IF EXISTS users")
        self._init_db()
