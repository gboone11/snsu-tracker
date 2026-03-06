from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.checklist_completion_repository import ChecklistCompletionRepository

router = APIRouter()
db = Database()
completion_repo = ChecklistCompletionRepository(db)


class ChecklistCompletionCreate(BaseModel):
    execution_id: int
    item_id: int


class ChecklistCompletionUpdate(BaseModel):
    is_completed: Optional[int] = None
    completed_by: Optional[str] = None
    completed_at: Optional[str] = None


@router.post("/checklist-completions")
def create_completion(completion: ChecklistCompletionCreate):
    try:
        completion_id = completion_repo.create(completion.execution_id, completion.item_id)
        return {"message": "Completion created", "data": {"completion_id": completion_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/checklist-completions/execution/{execution_id}")
def get_completions_by_execution(execution_id: int):
    completions = completion_repo.get_by_execution(execution_id)
    return {"data": completions}


@router.get("/checklist-completions/{completion_id}")
def get_completion(completion_id: int):
    completion = completion_repo.get_by_id(completion_id)
    if not completion:
        raise HTTPException(status_code=404, detail="Completion not found")
    return {"data": completion}


@router.put("/checklist-completions/{completion_id}")
def update_completion(completion_id: int, completion: ChecklistCompletionUpdate):
    updates = {k: v for k, v in completion.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = completion_repo.update(completion_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Completion not found")
    return {"message": "Completion updated"}


@router.delete("/checklist-completions/{completion_id}")
def delete_completion(completion_id: int):
    success = completion_repo.delete(completion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Completion not found")
    return {"message": "Completion deleted"}
