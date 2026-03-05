import os
from calendar import monthrange
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from classes.api_facade import Api_Facade
from classes.asset import Asset
from classes.database import Database
from classes.model import Model

app = FastAPI(title="Falsey Finder API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class SyncRequest(BaseModel):
    pass


class AnalysisRequest(BaseModel):
    asset: str
    limit: int = 10
    month: Optional[int] = None
    year: Optional[int] = None


class ApiResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None

    def __init__(
        self, message: Optional[str] = None, data: Optional[Any] = None, **kwargs: Any
    ) -> None:
        super().__init__(message=message, data=data, **kwargs)


