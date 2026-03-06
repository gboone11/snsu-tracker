from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.run_repository import RunRepository

router = APIRouter()
db = Database()
run_repo = RunRepository(db)


class RunCreate(BaseModel):
    line_id: int
    work_order_end_time: str
    target_ready_time: str
    status: str


class RunUpdate(BaseModel):
    actual_ready_time: Optional[str] = None
    total_duration_minutes: Optional[int] = None
    status: Optional[str] = None


@router.post("/runs")
def create_run(run: RunCreate):
    try:
        run_id = run_repo.create(run.line_id, run.work_order_end_time, run.target_ready_time, run.status)
        created_run = run_repo.get_by_id(run_id)
        return {"message": "Run created", "data": created_run}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/runs")
def get_runs():
    runs = run_repo.get_all()
    return {"data": runs}


@router.get("/runs/active")
def get_active_runs():
    runs = run_repo.get_active()
    return {"data": runs}


@router.get("/runs/{run_id}")
def get_run(run_id: int):
    run = run_repo.get_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"data": run}


@router.put("/runs/{run_id}")
def update_run(run_id: int, run: RunUpdate):
    updates = {k: v for k, v in run.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = run_repo.update(run_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"message": "Run updated"}


@router.delete("/runs/{run_id}")
def delete_run(run_id: int):
    success = run_repo.delete(run_id)
    if not success:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"message": "Run deleted"}
