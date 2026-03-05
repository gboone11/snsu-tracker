from typing import Any, Dict, List, Optional


class RunRepository:
    def __init__(self, db):
        self.db = db

    def create(self, line_id: int, work_order_end_time: str, target_ready_time: str, status: str) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO runs (line_id, work_order_end_time, target_ready_time, status) VALUES (?, ?, ?, ?)",
                (line_id, work_order_end_time, target_ready_time, status)
            )
            return cursor.lastrowid

    def get_all(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM runs ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_active(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM runs WHERE status = 'active' ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, run_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, run_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [run_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE runs SET {set_clause} WHERE run_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, run_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))
            return cursor.rowcount > 0
