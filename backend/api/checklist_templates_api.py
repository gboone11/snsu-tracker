from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ChecklistTemplateCreate(BaseModel):
    team_name: str
    task_name: str
    is_custom: Optional[int] = 0


class ChecklistTemplateUpdate(BaseModel):
    team_name: Optional[str] = None
    task_name: Optional[str] = None
    is_custom: Optional[int] = None
