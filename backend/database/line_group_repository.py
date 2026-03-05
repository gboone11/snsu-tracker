from typing import Any, Dict, List, Optional


class LineGroupRepository:
    def __init__(self, db):
        self.db = db

    def create(self, group_name: str, description: Optional[str], target_ready_time: Optional[str]) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO line_groups (group_name, description, target_ready_time) VALUES (?, ?, ?)",
                (group_name, description, target_ready_time)
            )
            return cursor.lastrowid

    def get_all(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM line_groups WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, group_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM line_groups WHERE group_id = ?", (group_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, group_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [group_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE line_groups SET {set_clause} WHERE group_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, group_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM line_groups WHERE group_id = ?", (group_id,))
            return cursor.rowcount > 0
