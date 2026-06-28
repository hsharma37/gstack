from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./ictos.db"
    api_prefix: str = "/api/v1"
    app_name: str = "ICTOS Backend"
    app_version: str = "0.2.0"
    project_root: Path = Path(__file__).resolve().parent.parent
    cors_origins: list[str] = ["http://localhost:4173", "http://localhost:3000"]
    jwt_secret: str = "ictos-dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    debug: bool = False

    model_config = ConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
