from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.sub_task_repository import SubTaskRepository

router = APIRouter()
db = Database()
sub_task_repo = SubTaskRepository(db)


class SubTaskCreate(BaseModel):
    execution_id: int
    sub_task_name: str
    sub_task_order: int = 0


class SubTaskUpdate(BaseModel):
    sub_task_name: Optional[str] = None
    sub_task_order: Optional[int] = None
    is_completed: Optional[int] = None
    completed_by: Optional[str] = None
    completed_at: Optional[str] = None


@router.post("/sub-tasks")
def create_sub_task(sub_task: SubTaskCreate):
    try:
        sub_task_id = sub_task_repo.create(
            sub_task.execution_id, sub_task.sub_task_name, sub_task.sub_task_order
        )
        return {"message": "Sub-task created", "data": {"sub_task_id": sub_task_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sub-tasks/execution/{execution_id}")
def get_sub_tasks_by_execution(execution_id: int):
    return {"data": sub_task_repo.get_by_execution(execution_id)}


@router.put("/sub-tasks/{sub_task_id}")
def update_sub_task(sub_task_id: int, sub_task: SubTaskUpdate):
    updates = {k: v for k, v in sub_task.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = sub_task_repo.update(sub_task_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Sub-task not found")
    return {"message": "Sub-task updated"}


@router.delete("/sub-tasks/{sub_task_id}")
def delete_sub_task(sub_task_id: int):
    success = sub_task_repo.delete(sub_task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sub-task not found")
    return {"message": "Sub-task deleted"}
