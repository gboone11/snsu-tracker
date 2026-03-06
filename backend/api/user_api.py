from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.user_repository import UserRepository

router = APIRouter()
db = Database()
user_repo = UserRepository(db)


class UserCreate(BaseModel):
    username: str
    full_name: str
    initials: str
    team_name: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    initials: Optional[str] = None
    team_name: Optional[str] = None


@router.post("/users")
def create_user(user: UserCreate):
    try:
        user_id = user_repo.create(user.username, user.full_name, user.initials, user.team_name)
        return {"message": "User created", "data": {"user_id": user_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users")
def get_users():
    users = user_repo.get_all()
    return {"data": users}


@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}


@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    updates = {k: v for k, v in user.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    success = user_repo.update(user_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    success = user_repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
