from typing import Any, Dict, List, Optional


class CommunicationNoteRepository:
    def __init__(self, db):
        self.db = db

    def create(self, line_id: int, note_text: str, created_by: str, run_id: Optional[int] = None) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO communication_notes (line_id, note_text, created_by, run_id) VALUES (?, ?, ?, ?)",
                (line_id, note_text, created_by, run_id)
            )
            return cursor.lastrowid

    def get_by_line(self, line_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM communication_notes WHERE line_id = ? ORDER BY created_at DESC",
                (line_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_by_run(self, run_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM communication_notes WHERE run_id = ? ORDER BY created_at DESC",
                (run_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, note_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM communication_notes WHERE note_id = ?", (note_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, note_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [note_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE communication_notes SET {set_clause} WHERE note_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, note_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM communication_notes WHERE note_id = ?", (note_id,))
            return cursor.rowcount > 0
