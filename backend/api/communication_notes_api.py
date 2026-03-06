from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.communication_note_repository import CommunicationNoteRepository

router = APIRouter()
db = Database()
note_repo = CommunicationNoteRepository(db)


class CommunicationNoteCreate(BaseModel):
    line_id: int
    note_text: str
    created_by: str
    run_id: Optional[int] = None


class CommunicationNoteUpdate(BaseModel):
    note_text: Optional[str] = None


@router.post("/communication-notes")
def create_note(note: CommunicationNoteCreate):
    try:
        note_id = note_repo.create(note.line_id, note.note_text, note.created_by, note.run_id)
        return {"message": "Note created", "data": {"note_id": note_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/communication-notes/line/{line_id}")
def get_notes_by_line(line_id: int):
    notes = note_repo.get_by_line(line_id)
    return {"data": notes}


@router.get("/communication-notes/run/{run_id}")
def get_notes_by_run(run_id: int):
    notes = note_repo.get_by_run(run_id)
    return {"data": notes}


@router.get("/communication-notes/{note_id}")
def get_note(note_id: int):
    note = note_repo.get_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"data": note}


@router.put("/communication-notes/{note_id}")
def update_note(note_id: int, note: CommunicationNoteUpdate):
    updates = {k: v for k, v in note.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = note_repo.update(note_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note updated"}


@router.delete("/communication-notes/{note_id}")
def delete_note(note_id: int):
    success = note_repo.delete(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}
