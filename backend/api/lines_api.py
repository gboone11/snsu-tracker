from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.line_repository import LineRepository

router = APIRouter()
db = Database()
line_repo = LineRepository(db)


class LineCreate(BaseModel):
    line_number: int


class LineUpdate(BaseModel):
    line_number: Optional[int] = None


class ReorderRequest(BaseModel):
    ordered_ids: List[int]


@router.post("/lines")
def create_line(line: LineCreate):
    try:
        line_id = line_repo.create(line.line_number)
        return {"message": "Line created", "data": {"line_id": line_id}}
    except Exception as e:
        if "UNIQUE constraint" in str(e):
            raise HTTPException(
                status_code=409, detail=f"Line {line.line_number} already exists"
            )
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/lines")
def get_lines():
    lines = line_repo.get_all()
    return {"data": lines}


@router.put("/lines/reorder")
def reorder_lines(req: ReorderRequest):
    try:
        line_repo.reorder(req.ordered_ids)
        return {"message": "Lines reordered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/lines/{line_id}")
def get_line(line_id: int):
    line = line_repo.get_by_id(line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found")
    return {"data": line}


@router.put("/lines/{line_id}")
def update_line(line_id: int, line: LineUpdate):
    updates = {k: v for k, v in line.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    success = line_repo.update(line_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Line not found")
    return {"message": "Line updated"}


@router.delete("/lines/{line_id}")
def delete_line(line_id: int):
    success = line_repo.delete(line_id)
    if not success:
        raise HTTPException(status_code=404, detail="Line not found")
    return {"message": "Line deleted"}
