from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import Database

router = APIRouter()
db = Database()


class LineGroupCreate(BaseModel):
    group_name: str
    description: Optional[str] = None
    target_ready_time: Optional[str] = None


class LineGroupUpdate(BaseModel):
    group_name: Optional[str] = None
    description: Optional[str] = None
    target_ready_time: Optional[str] = None
    is_active: Optional[int] = None
