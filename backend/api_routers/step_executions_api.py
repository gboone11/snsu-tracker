from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class StepExecutionCreate(BaseModel):
    run_id: int
    step_id: int
    status: str


class StepExecutionUpdate(BaseModel):
    status: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    signed_by: Optional[str] = None
    signed_at: Optional[str] = None
