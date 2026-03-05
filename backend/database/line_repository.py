from typing import Any, Dict, List, Optional


class LineRepository:
    def __init__(self, db):
        self.db = db

    def create(self, line_number: str, line_group_id: int) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO lines (line_number, line_group_id) VALUES (?, ?)",
                (line_number, line_group_id)
            )
            return cursor.lastrowid

    def get_all(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM lines WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, line_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM lines WHERE line_id = ?", (line_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, line_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [line_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE lines SET {set_clause} WHERE line_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, line_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM lines WHERE line_id = ?", (line_id,))
            return cursor.rowcount > 0
