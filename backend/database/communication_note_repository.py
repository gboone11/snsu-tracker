from typing import Any, Dict, List, Optional


class CommunicationNoteRepository:
    def __init__(self, db):
        self.db = db

    def create(self, line_id: int, note_text: str, created_by: str, run_id: Optional[int] = None) -> int:
        pass

    def get_by_line(self, line_id: int) -> List[Dict[str, Any]]:
        pass

    def get_by_run(self, run_id: int) -> List[Dict[str, Any]]:
        pass

    def get_by_id(self, note_id: int) -> Optional[Dict[str, Any]]:
        pass

    def update(self, note_id: int, updates: Dict[str, Any]) -> bool:
        pass

    def delete(self, note_id: int) -> bool:
        pass
