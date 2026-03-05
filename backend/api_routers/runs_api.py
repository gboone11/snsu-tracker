from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class RunCreate(BaseModel):
    line_id: int
    work_order_end_time: str
    target_ready_time: str
    status: str


class RunUpdate(BaseModel):
    actual_ready_time: Optional[str] = None
    total_duration_minutes: Optional[int] = None
    status: Optional[str] = None
