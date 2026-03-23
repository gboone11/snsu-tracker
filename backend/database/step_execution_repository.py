from typing import Any, Dict, List, Optional


class StepExecutionRepository:
    def __init__(self, db):
        self.db = db

    def create(self, run_id: int, step_id: int, status: str) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO step_executions (run_id, step_id, status) VALUES (?, ?, ?)",
                (run_id, step_id, status),
            )
            return cursor.lastrowid

    def get_by_run(self, run_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM step_executions WHERE run_id = ?", (run_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, execution_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM step_executions WHERE execution_id = ?", (execution_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, execution_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [execution_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                f"UPDATE step_executions SET {set_clause} WHERE execution_id = ?",
                values,
            )
            return cursor.rowcount > 0

    def delete(self, execution_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM step_executions WHERE execution_id = ?", (execution_id,)
            )
            return cursor.rowcount > 0
