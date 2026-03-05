from typing import Any, Dict, List, Optional


class RunRepository:
    def __init__(self, db):
        self.db = db

    def create(self, line_id: int, work_order_end_time: str, target_ready_time: str, status: str) -> int:
        pass

    def get_all(self) -> List[Dict[str, Any]]:
        pass

    def get_active(self) -> List[Dict[str, Any]]:
        pass

    def get_by_id(self, run_id: int) -> Optional[Dict[str, Any]]:
        pass

    def update(self, run_id: int, updates: Dict[str, Any]) -> bool:
        pass

    def delete(self, run_id: int) -> bool:
        pass
