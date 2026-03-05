import os
from calendar import monthrange
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from database import Database

app = FastAPI(title="SNSU Tracker API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
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


class ApiResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None


# Initialize database
db = Database()


# User endpoints
@app.post("/users", response_model=ApiResponse)
def create_user(user: UserCreate):
    try:
        user_id = db.create_user(user.username, user.full_name, user.initials, user.team_name)
        return ApiResponse(message="User created", data={"user_id": user_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users", response_model=ApiResponse)
def get_users():
    users = db.get_all_users()
    return ApiResponse(data=users)


@app.get("/users/{user_id}", response_model=ApiResponse)
def get_user(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(data=user)


@app.put("/users/{user_id}", response_model=ApiResponse)
def update_user(user_id: int, user: UserUpdate):
    updates = {k: v for k, v in user.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    success = db.update_user(user_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(message="User updated")


@app.delete("/users/{user_id}", response_model=ApiResponse)
def delete_user(user_id: int):
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(message="User deleted")


@app.post("/users/{user_id}/deactivate", response_model=ApiResponse)
def deactivate_user(user_id: int):
    success = db.deactivate_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(message="User deactivated")


@app.post("/clear-data", response_model=ApiResponse)
def clear_all_data():
    db.clear_data()
    return ApiResponse(message="All data cleared")
