from typing import Optional
import pydantic


class Settings(pydantic.BaseSettings):
    database_name: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
