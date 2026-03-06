from typing import Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database.connection import Database
from api.user_api import router as user_router
from api.line_groups_api import router as line_groups_router
from api.lines_api import router as lines_router

app = FastAPI(title="SNSU Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApiResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None


db = Database()

app.include_router(user_router)
app.include_router(line_groups_router)
app.include_router(lines_router)


@app.post("/clear-data", response_model=ApiResponse)
def clear_all_data():
    db.clear_data()
    return ApiResponse(message="All data cleared")