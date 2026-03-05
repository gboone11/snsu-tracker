from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ChecklistCompletionCreate(BaseModel):
    execution_id: int
    item_id: int


class ChecklistCompletionUpdate(BaseModel):
    is_completed: Optional[int] = None
    completed_by: Optional[str] = None
    completed_at: Optional[str] = None
