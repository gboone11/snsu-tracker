from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import Database
from database.checklist_template_repository import ChecklistTemplateRepository

router = APIRouter()
db = Database()
template_repo = ChecklistTemplateRepository(db)


class ChecklistTemplateCreate(BaseModel):
    team_name: str
    task_name: str
    is_custom: Optional[int] = 0


class ChecklistTemplateUpdate(BaseModel):
    team_name: Optional[str] = None
    task_name: Optional[str] = None
    is_custom: Optional[int] = None


@router.post("/checklist-templates")
def create_template(template: ChecklistTemplateCreate):
    try:
        template_id = template_repo.create(template.team_name, template.task_name, template.is_custom)
        return {"message": "Template created", "data": {"template_id": template_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/checklist-templates")
def get_templates():
    templates = template_repo.get_all()
    return {"data": templates}


@router.get("/checklist-templates/{template_id}")
def get_template(template_id: int):
    template = template_repo.get_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"data": template}


@router.put("/checklist-templates/{template_id}")
def update_template(template_id: int, template: ChecklistTemplateUpdate):
    updates = {k: v for k, v in template.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = template_repo.update(template_id, updates)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template updated"}


@router.delete("/checklist-templates/{template_id}")
def delete_template(template_id: int):
    success = template_repo.delete(template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted"}
