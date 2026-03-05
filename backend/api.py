from typing import Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import Database
from api.user_api import router as user_router

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


@app.post("/clear-data", response_model=ApiResponse)
def clear_all_data():
    db.clear_data()
    return ApiResponse(message="All data cleared")