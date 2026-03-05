from typing import Any, Dict, List, Optional


class ChecklistItemRepository:
    def __init__(self, db):
        self.db = db

    def create(self, template_id: int, item_order: int, item_text: str) -> int:
        pass

    def get_by_template(self, template_id: int) -> List[Dict[str, Any]]:
        pass

    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        pass

    def update(self, item_id: int, updates: Dict[str, Any]) -> bool:
        pass

    def delete(self, item_id: int) -> bool:
        pass
