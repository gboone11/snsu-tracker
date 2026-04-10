from typing import Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database.connection import Database
from api.lines_api import router as lines_router
from api.runs_api import router as runs_router
from api.process_steps_api import router as process_steps_router
from api.step_executions_api import router as step_executions_router
from api.sub_tasks_api import router as sub_tasks_router

app = FastAPI(title="SNSU Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApiResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None


db = Database()

app.include_router(lines_router)
app.include_router(runs_router)
app.include_router(process_steps_router)
app.include_router(step_executions_router)
app.include_router(sub_tasks_router)


@app.post("/clear-data", response_model=ApiResponse)
def clear_all_data():
    db.clear_data()
    return ApiResponse(message="All data cleared")
