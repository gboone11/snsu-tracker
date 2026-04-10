from typing import Any, Dict, List, Optional


class SubTaskRepository:
    def __init__(self, db):
        self.db = db

    def create(self, execution_id: int, sub_task_name: str, sub_task_order: int) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO sub_tasks (execution_id, sub_task_name, sub_task_order) VALUES (?, ?, ?)",
                (execution_id, sub_task_name, sub_task_order),
            )
            return cursor.lastrowid

    def get_by_execution(self, execution_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM sub_tasks WHERE execution_id = ? ORDER BY sub_task_order",
                (execution_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

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
            cursor = conn.execute(
                "DELETE FROM sub_tasks WHERE sub_task_id = ?", (sub_task_id,)
            )
            return cursor.rowcount > 0
