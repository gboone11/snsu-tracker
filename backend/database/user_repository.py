from typing import Any, Dict, List, Optional


class UserRepository:
    def __init__(self, db):
        self.db = db

    def create(self, username: str, full_name: str, initials: str, team_name: str) -> int:
        pass

    def get_all(self) -> List[Dict[str, Any]]:
        pass

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        pass

    def update(self, user_id: int, updates: Dict[str, Any]) -> bool:
        pass

    def delete(self, user_id: int) -> bool:
        pass

    def deactivate(self, user_id: int) -> bool:
        pass
