from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import Database

router = APIRouter()
db = Database()


class LineGroupCreate(BaseModel):
    group_name: str
    description: Optional[str] = None
    target_ready_time: Optional[str] = None


class LineGroupUpdate(BaseModel):
    group_name: Optional[str] = None
    description: Optional[str] = None
    target_ready_time: Optional[str] = None
    is_active: Optional[int] = None

@router.post("/line-groups")
def create_line_group(line_group: LineGroupCreate):
    try:
        group_id = line_group_repo.create(line_group.group_name, line_group.description, line_group.target_ready_time)
        return {"message": "Line group created", "data": {"group_id": group_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/line-groups")
def get_line_groups():
    line_groups = line_group_repo.get_all()
    return {"data": line_groups}


@router.get("/line-groups/{group_id}")
def get_line_group(group_id: int):
    line_group = line_group_repo.get_by_id(group_id)
    if not line_group:
        raise HTTPException(status_code=404, detail="Line group not found")
    return {"data": line_group}


@router.put("/line-groups/{group_id}")
def update_line_group(group_id: int, line_group: LineGroupUpdate):
    updates = {k: v for k, v in line_group.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    success = line_group_repo.update(group_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Line group not found")
    return {"message": "Line group updated"}


@router.delete("/line-groups/{group_id}")
def delete_line_group(group_id: int):
    success = line_group_repo.delete(group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Line group not found")
    return {"message": "Line group deleted"}