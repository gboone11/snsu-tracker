from typing import Any, Dict, List, Optional


class ChecklistItemRepository:
    def __init__(self, db):
        self.db = db

    def create(self, template_id: int, item_order: int, item_text: str) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO checklist_items (template_id, item_order, item_text) VALUES (?, ?, ?)",
                (template_id, item_order, item_text)
            )
            return cursor.lastrowid

    def get_by_template(self, template_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM checklist_items WHERE template_id = ? ORDER BY item_order",
                (template_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM checklist_items WHERE item_id = ?", (item_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, item_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [item_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE checklist_items SET {set_clause} WHERE item_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, item_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM checklist_items WHERE item_id = ?", (item_id,))
            return cursor.rowcount > 0
