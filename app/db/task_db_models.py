from datetime import date
from typing import Optional
from sqlalchemy import orm
from app.db import base_db_model


class Task(base_db_model.Base):
    __tablename__ = "task"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column()
    deadline: orm.Mapped[Optional[date]] = orm.mapped_column(default=None)
    finished: orm.Mapped[bool] = orm.mapped_column(default=False)
    progress: orm.Mapped[Optional[int]] = orm.mapped_column(default=None)
