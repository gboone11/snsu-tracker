from typing import Any, Dict, List, Optional


class ChecklistCompletionRepository:
    def __init__(self, db):
        self.db = db

    def create(self, execution_id: int, item_id: int) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO checklist_completions (execution_id, item_id) VALUES (?, ?)",
                (execution_id, item_id)
            )
            return cursor.lastrowid

    def get_by_execution(self, execution_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM checklist_completions WHERE execution_id = ?",
                (execution_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, completion_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM checklist_completions WHERE completion_id = ?", (completion_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, completion_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [completion_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE checklist_completions SET {set_clause} WHERE completion_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, completion_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM checklist_completions WHERE completion_id = ?", (completion_id,))
            return cursor.rowcount > 0
