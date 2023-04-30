import fastapi
from app import config

# database
from app.db import db_engine

# routers
from app.api import task_api

settings = config.Settings()  # type: ignore

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup_event():
    await db_engine.init(settings.database_name)


@app.get("/")
async def get_root():
    return "Service is running."


app.include_router(task_api.router)
