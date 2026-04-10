from typing import Any, Dict, List, Optional


class SubTaskExecutionRepository:
    def __init__(self, db):
        self.db = db

    def create(self, execution_id: int, sub_task_id: int) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO sub_task_executions (execution_id, sub_task_id) VALUES (?, ?)",
                (execution_id, sub_task_id),
            )
            return cursor.lastrowid

    def get_by_execution(self, execution_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM sub_task_executions WHERE execution_id = ? ORDER BY sub_task_id",
                (execution_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def update(self, sub_task_execution_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [sub_task_execution_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                f"UPDATE sub_task_executions SET {set_clause} WHERE sub_task_execution_id = ?",
                values,
            )
            return cursor.rowcount > 0

    def delete(self, sub_task_execution_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM sub_task_executions WHERE sub_task_execution_id = ?",
                (sub_task_execution_id,),
            )
            return cursor.rowcount > 0

    def delete_by_execution(self, execution_id: int) -> None:
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM sub_task_executions WHERE execution_id = ?",
                (execution_id,),
            )
