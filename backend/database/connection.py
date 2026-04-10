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
                CREATE TABLE IF NOT EXISTS lines (
                    line_id INTEGER PRIMARY KEY,
                    line_number INTEGER UNIQUE NOT NULL,
                    display_order INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS process_steps (
                    step_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    step_order INTEGER NOT NULL,
                    team_name TEXT NOT NULL,
                    task_name TEXT NOT NULL,
                    avg_duration_minutes INTEGER
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
                
                CREATE TABLE IF NOT EXISTS sub_tasks (
                    sub_task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id INTEGER NOT NULL,
                    sub_task_name TEXT NOT NULL,
                    sub_task_order INTEGER NOT NULL DEFAULT 0,
                    is_completed INTEGER NOT NULL DEFAULT 0,
                    completed_by TEXT,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (execution_id) REFERENCES step_executions(execution_id)
                );

                CREATE INDEX IF NOT EXISTS idx_lines_order ON lines(display_order);
                CREATE INDEX IF NOT EXISTS idx_steps_order ON process_steps(step_order);
                CREATE INDEX IF NOT EXISTS idx_runs_line ON runs(line_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_executions_run ON step_executions(run_id, step_id);
                CREATE INDEX IF NOT EXISTS idx_sub_tasks_exec ON sub_tasks(execution_id, sub_task_order);
            """
            )

    def clear_data(self) -> None:
        with self.get_connection() as conn:
            conn.execute("DROP TABLE IF EXISTS sub_tasks")
            conn.execute("DROP TABLE IF EXISTS step_executions")
            conn.execute("DROP TABLE IF EXISTS runs")
            conn.execute("DROP TABLE IF EXISTS process_steps")
            conn.execute("DROP TABLE IF EXISTS lines")

        self._init_db()
