from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import Database

router = APIRouter()
db = Database()


class UserCreate(BaseModel):
    username: str
    full_name: str
    initials: str
    team_name: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    initials: Optional[str] = None
    team_name: Optional[str] = None
    is_active: Optional[int] = None


@router.post("/users")
def create_user(user: UserCreate):
    try:
        user_id = db.create_user(user.username, user.full_name, user.initials, user.team_name)
        return {"message": "User created", "data": {"user_id": user_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users")
def get_users():
    users = db.get_all_users()
    return {"data": users}


@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}


@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    updates = {k: v for k, v in user.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    success = db.update_user(user_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


@router.post("/users/{user_id}/deactivate")
def deactivate_user(user_id: int):
    success = db.deactivate_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated"}
