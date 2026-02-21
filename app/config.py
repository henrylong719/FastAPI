from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    app_name: str = "Issue Tracker API"
    app_version: str = "0.1.0"
    debug: bool = False

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    data_dir: Path = Path("data")

    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
