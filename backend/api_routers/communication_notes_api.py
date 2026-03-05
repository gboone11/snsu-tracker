from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class CommunicationNoteCreate(BaseModel):
    line_id: int
    note_text: str
    created_by: str
    run_id: Optional[int] = None


class CommunicationNoteUpdate(BaseModel):
    note_text: Optional[str] = None
