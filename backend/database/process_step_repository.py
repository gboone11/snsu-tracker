from typing import Any, Dict, List, Optional


class ProcessStepRepository:
    def __init__(self, db):
        self.db = db

    def create(self, step_order: int, team_name: str, task_name: str, avg_duration_minutes: Optional[int]) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO process_steps (step_order, team_name, task_name, avg_duration_minutes) VALUES (?, ?, ?, ?)",
                (step_order, team_name, task_name, avg_duration_minutes)
            )
            return cursor.lastrowid

    def get_all(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM process_steps ORDER BY step_order")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, step_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM process_steps WHERE step_id = ?", (step_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, step_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [step_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE process_steps SET {set_clause} WHERE step_id = ?", values)
            return cursor.rowcount > 0

    def reorder(self, ordered_ids: List[int]) -> None:
        with self.db.get_connection() as conn:
            for order, step_id in enumerate(ordered_ids, start=1):
                conn.execute("UPDATE process_steps SET step_order = ? WHERE step_id = ?", (order, step_id))

    def delete(self, step_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM process_steps WHERE step_id = ?", (step_id,))
            return cursor.rowcount > 0
