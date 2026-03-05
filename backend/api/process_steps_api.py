from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ProcessStepCreate(BaseModel):
    group_id: int
    step_order: int
    team_name: str
    task_name: str
    avg_duration_minutes: Optional[int] = None


class ProcessStepUpdate(BaseModel):
    step_order: Optional[int] = None
    team_name: Optional[str] = None
    task_name: Optional[str] = None
    avg_duration_minutes: Optional[int] = None
    is_active: Optional[int] = None
