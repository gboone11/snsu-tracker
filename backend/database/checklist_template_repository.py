from typing import Any, Dict, List, Optional


class ChecklistTemplateRepository:
    def __init__(self, db):
        self.db = db

    def create(self, team_name: str, task_name: str, is_custom: int = 0) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO checklist_templates (team_name, task_name, is_custom) VALUES (?, ?, ?)",
                (team_name, task_name, is_custom)
            )
            return cursor.lastrowid

    def get_all(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM checklist_templates")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, template_id: int) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM checklist_templates WHERE template_id = ?", (template_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, template_id: int, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [template_id]
        with self.db.get_connection() as conn:
            cursor = conn.execute(f"UPDATE checklist_templates SET {set_clause} WHERE template_id = ?", values)
            return cursor.rowcount > 0

    def delete(self, template_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM checklist_templates WHERE template_id = ?", (template_id,))
            return cursor.rowcount > 0
