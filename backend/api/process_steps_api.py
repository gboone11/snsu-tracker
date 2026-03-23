from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.process_step_repository import ProcessStepRepository

router = APIRouter()
db = Database()
step_repo = ProcessStepRepository(db)


class ProcessStepCreate(BaseModel):
    step_order: int
    team_name: str
    task_name: str
    avg_duration_minutes: Optional[int] = None


class ProcessStepUpdate(BaseModel):
    step_order: Optional[int] = None
    team_name: Optional[str] = None
    task_name: Optional[str] = None
    avg_duration_minutes: Optional[int] = None


class ReorderRequest(BaseModel):
    ordered_ids: List[int]


@router.post("/process-steps")
def create_step(step: ProcessStepCreate):
    try:
        step_id = step_repo.create(
            step.step_order, step.team_name, step.task_name, step.avg_duration_minutes
        )
        return {"message": "Step created", "data": {"step_id": step_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/process-steps")
def get_steps():
    steps = step_repo.get_all()
    return {"data": steps}


@router.put("/process-steps/reorder")
def reorder_steps(req: ReorderRequest):
    try:
        step_repo.reorder(req.ordered_ids)
        return {"message": "Steps reordered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/process-steps/{step_id}")
def get_step(step_id: int):
    step = step_repo.get_by_id(step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return {"data": step}


@router.put("/process-steps/{step_id}")
def update_step(step_id: int, step: ProcessStepUpdate):
    updates = {k: v for k, v in step.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = step_repo.update(step_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Step not found")
    return {"message": "Step updated"}


@router.delete("/process-steps/{step_id}")
def delete_step(step_id: int):
    success = step_repo.delete(step_id)
    if not success:
        raise HTTPException(status_code=404, detail="Step not found")
    return {"message": "Step deleted"}
