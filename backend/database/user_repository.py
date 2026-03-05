from typing import Any, Dict, List, Optional


class UserRepository:
    def __init__(self, db):
        self.db = db

    def create(self, username: str, full_name: str, initials: str, team_name: str) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, full_name, initials, team_name) VALUES (?, ?, ?, ?)",
                (username, full_name, initials, team_name)
            )
            return cursor.lastrowid

    def get_all(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, user_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            return cursor.rowcount > 0

    def deactivate(self, user_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("UPDATE users SET is_active = 0 WHERE user_id = ?", (user_id,))
            return cursor.rowcount > 0
