from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class LineCreate(BaseModel):
    line_number: str
    line_group_id: int


class LineUpdate(BaseModel):
    line_number: Optional[str] = None
    line_group_id: Optional[int] = None
    is_active: Optional[int] = None
