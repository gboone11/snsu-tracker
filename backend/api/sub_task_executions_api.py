from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.sub_task_execution_repository import SubTaskExecutionRepository

router = APIRouter()
db = Database()
sub_task_exec_repo = SubTaskExecutionRepository(db)


class SubTaskExecutionCreate(BaseModel):
    execution_id: int
    sub_task_id: int


class SubTaskExecutionUpdate(BaseModel):
    is_completed: Optional[int] = None
    completed_by: Optional[str] = None
    completed_at: Optional[str] = None


@router.post("/sub-task-executions")
def create_sub_task_execution(data: SubTaskExecutionCreate):
    try:
        ste_id = sub_task_exec_repo.create(data.execution_id, data.sub_task_id)
        return {
            "message": "Sub-task execution created",
            "data": {"sub_task_execution_id": ste_id},
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sub-task-executions/execution/{execution_id}")
def get_by_execution(execution_id: int):
    return {"data": sub_task_exec_repo.get_by_execution(execution_id)}


@router.put("/sub-task-executions/{sub_task_execution_id}")
def update_sub_task_execution(
    sub_task_execution_id: int, data: SubTaskExecutionUpdate
):
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = sub_task_exec_repo.update(sub_task_execution_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Sub-task execution not found")
    return {"message": "Sub-task execution updated"}


@router.delete("/sub-task-executions/{sub_task_execution_id}")
def delete_sub_task_execution(sub_task_execution_id: int):
    success = sub_task_exec_repo.delete(sub_task_execution_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sub-task execution not found")
    return {"message": "Sub-task execution deleted"}
