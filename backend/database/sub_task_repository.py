from typing import Any, Dict, List, Optional


class SubTaskRepository:
    def __init__(self, db):
        self.db = db

    def create(self, step_id: int, sub_task_name: str, sub_task_order: int) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO sub_tasks (step_id, sub_task_name, sub_task_order) VALUES (?, ?, ?)",
                (step_id, sub_task_name, sub_task_order),
            )
            return cursor.lastrowid

    def get_by_step(self, step_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM sub_tasks WHERE step_id = ? ORDER BY sub_task_order",
                (step_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, sub_task_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM sub_tasks WHERE sub_task_id = ?", (sub_task_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, sub_task_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [sub_task_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                f"UPDATE sub_tasks SET {set_clause} WHERE sub_task_id = ?", values
            )
            return cursor.rowcount > 0

    def delete(self, sub_task_id: int) -> bool:
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM sub_task_executions WHERE sub_task_id = ?", (sub_task_id,)
            )
            cursor = conn.execute(
                "DELETE FROM sub_tasks WHERE sub_task_id = ?", (sub_task_id,)
            )
            return cursor.rowcount > 0
