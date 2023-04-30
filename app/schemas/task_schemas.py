from typing import Optional
import pydantic
from datetime import date


class TaskResult(pydantic.BaseModel):
    id: int
    name: str
    deadline: Optional[date]
    finished: bool

    class Config:
        orm_mode = True


class TaskCreate(pydantic.BaseModel):
    name: str
    deadline: Optional[date] = None


class TasksSummary(pydantic.BaseModel):
    active: int = 0
    finished: int = 0
    total: int = 0
