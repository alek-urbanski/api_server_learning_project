from typing import Any, Dict, Optional, Sequence

from sqlalchemy import orm
from sqlalchemy.sql import func

import fastapi

from app.db import task_db_models
from app.schemas import task_schemas


def read_all_tasks(db: orm.Session) -> list[task_schemas.TaskResult]:
    """reads all tasks from database"""
    db_rows: Sequence[task_db_models.Task] = db.query(task_db_models.Task).all()
    if not db_rows:
        raise fastapi.HTTPException(status_code=404, detail="No tasks found.")

    return [task_schemas.TaskResult.from_orm(db_row) for db_row in db_rows]


def read_task(db: orm.Session, id: int) -> task_schemas.TaskResult:
    """reads one task from database"""
    db_row: Optional[task_db_models.Task] = db.get(task_db_models.Task, id)
    if not db_row:
        raise fastapi.HTTPException(
            status_code=404, detail=f"There is no task with an id of {id}."
        )

    return task_schemas.TaskResult.from_orm(db_row)


def create_task(
    db: orm.Session, task_create_data: task_schemas.TaskCreate
) -> task_schemas.TaskResult:
    """creates a task"""
    new_db_row = task_db_models.Task(**task_create_data.dict())
    db.add(new_db_row)
    db.commit()

    return task_schemas.TaskResult.from_orm(new_db_row)


def finish_task(db: orm.Session, id: int) -> task_schemas.TaskResult:
    """marks task as finished"""
    db_row: Optional[task_db_models.Task] = db.get(task_db_models.Task, id)
    if not db_row:
        raise fastapi.HTTPException(
            status_code=404, detail=f"There is no task with an id of {id}."
        )
    db_row.finished = True
    db.commit()

    return task_schemas.TaskResult.from_orm(db_row)


def summarize_tasks(db: orm.Session) -> task_schemas.TasksSummary:
    """Counts tasks by status"""
    summary_result = (
        db.query(task_db_models.Task.finished, func.count())
        .group_by(task_db_models.Task.finished)
        .all()
    )

    # prepare dictionary to build response
    response_data: Dict[str, Any] = {"finished": 0, "active": 0, "total": 0}

    for row in summary_result:
        if row[0]:
            response_data["finished"] = row[1]
        else:
            response_data["active"] = row[1]

    # fmt: off
    response_data["total"] = ( 
        response_data.get("finished", 0) 
        + response_data.get("active", 0)
    )
    # fmt: on

    return task_schemas.TasksSummary.parse_obj(response_data)
