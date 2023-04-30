from typing import Optional

import fastapi

from app.db import db_engine
from app.schemas import task_schemas
from app.services import task_service


router = fastapi.APIRouter()


@router.get("/tasks")
async def api_read_all_tasks(
    db: db_engine.Session = fastapi.Depends(db_engine.get_db),
) -> Optional[list[task_schemas.TaskResult]]:
    return task_service.read_all_tasks(db)


@router.get("/tasks/id/{id}")
async def api_read_task(
    id: int, db: db_engine.Session = fastapi.Depends(db_engine.get_db)
) -> task_schemas.TaskResult:
    return task_service.read_task(db, id)


@router.post("/tasks")
async def api_create_task(
    task_create_model: task_schemas.TaskCreate,
    db: db_engine.Session = fastapi.Depends(db_engine.get_db),
) -> task_schemas.TaskResult:
    return task_service.create_task(db, task_create_model)


@router.put("/tasks/id/{id}/finish")
async def api_finish_task(
    id: int, db: db_engine.Session = fastapi.Depends(db_engine.get_db)
) -> task_schemas.TaskResult:
    return task_service.finish_task(db, id)


@router.get("/tasks/summary")
async def api_summarize_tasks(
    db: db_engine.Session = fastapi.Depends(db_engine.get_db),
) -> task_schemas.TasksSummary:
    return task_service.summarize_tasks(db)
