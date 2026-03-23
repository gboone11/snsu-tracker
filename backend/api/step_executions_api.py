from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.step_execution_repository import StepExecutionRepository

router = APIRouter()
db = Database()
execution_repo = StepExecutionRepository(db)


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


@router.post("/step-executions")
def create_execution(execution: StepExecutionCreate):
    try:
        execution_id = execution_repo.create(
            execution.run_id, execution.step_id, execution.status
        )
        return {"message": "Execution created", "data": {"execution_id": execution_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/step-executions/run/{run_id}")
def get_executions_by_run(run_id: int):
    executions = execution_repo.get_by_run(run_id)
    return {"data": executions}


@router.get("/step-executions/{execution_id}")
def get_execution(execution_id: int):
    execution = execution_repo.get_by_id(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"data": execution}


@router.put("/step-executions/{execution_id}")
def update_execution(execution_id: int, execution: StepExecutionUpdate):
    updates = {k: v for k, v in execution.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = execution_repo.update(execution_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"message": "Execution updated"}


@router.delete("/step-executions/{execution_id}")
def delete_execution(execution_id: int):
    success = execution_repo.delete(execution_id)
    if not success:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"message": "Execution deleted"}
