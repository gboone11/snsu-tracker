from typing import Any, Dict, List, Optional


class StepExecutionRepository:
    def __init__(self, db):
        self.db = db

    def create(self, run_id: int, step_id: int, status: str) -> int:
        pass

    def get_by_run(self, run_id: int) -> List[Dict[str, Any]]:
        pass

    def get_by_id(self, execution_id: int) -> Optional[Dict[str, Any]]:
        pass

    def update(self, execution_id: int, updates: Dict[str, Any]) -> bool:
        pass

    def delete(self, execution_id: int) -> bool:
        pass
