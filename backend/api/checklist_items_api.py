from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ChecklistItemCreate(BaseModel):
    template_id: int
    item_order: int
    item_text: str


class ChecklistItemUpdate(BaseModel):
    item_order: Optional[int] = None
    item_text: Optional[str] = None
    is_active: Optional[int] = None
