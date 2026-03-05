from typing import Any, Dict, List, Optional


class ChecklistTemplateRepository:
    def __init__(self, db):
        self.db = db

    def create(self, team_name: str, task_name: str, is_custom: int = 0) -> int:
        pass

    def get_all(self) -> List[Dict[str, Any]]:
        pass

    def get_by_id(self, template_id: int) -> Optional[Dict[str, Any]]:
        pass

    def update(self, template_id: int, updates: Dict[str, Any]) -> bool:
        pass

    def delete(self, template_id: int) -> bool:
        pass
