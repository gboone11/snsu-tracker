from typing import Any, Dict, List, Optional


class ProcessStepRepository:
    def __init__(self, db):
        self.db = db

    def create(self, group_id: int, step_order: int, team_name: str, task_name: str, avg_duration_minutes: Optional[int]) -> int:
        pass

    def get_all(self) -> List[Dict[str, Any]]:
        pass

    def get_by_group(self, group_id: int) -> List[Dict[str, Any]]:
        pass

    def get_by_id(self, step_id: int) -> Optional[Dict[str, Any]]:
        pass

    def update(self, step_id: int, updates: Dict[str, Any]) -> bool:
        pass

    def delete(self, step_id: int) -> bool:
        pass
