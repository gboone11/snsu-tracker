from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.checklist_item_repository import ChecklistItemRepository

router = APIRouter()
db = Database()
item_repo = ChecklistItemRepository(db)


class ChecklistItemCreate(BaseModel):
    template_id: int
    item_order: int
    item_text: str


class ChecklistItemUpdate(BaseModel):
    item_order: Optional[int] = None
    item_text: Optional[str] = None
    is_active: Optional[int] = None


@router.post("/checklist-items")
def create_item(item: ChecklistItemCreate):
    try:
        item_id = item_repo.create(item.template_id, item.item_order, item.item_text)
        return {"message": "Item created", "data": {"item_id": item_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/checklist-items/template/{template_id}")
def get_items_by_template(template_id: int):
    items = item_repo.get_by_template(template_id)
    return {"data": items}


@router.get("/checklist-items/{item_id}")
def get_item(item_id: int):
    item = item_repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"data": item}


@router.put("/checklist-items/{item_id}")
def update_item(item_id: int, item: ChecklistItemUpdate):
    updates = {k: v for k, v in item.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = item_repo.update(item_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated"}


@router.delete("/checklist-items/{item_id}")
def delete_item(item_id: int):
    success = item_repo.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
