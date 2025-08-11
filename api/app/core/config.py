from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./test.db"
    jwt_secret: str = "change-me"
    cors_origins: List[str] = ["http://localhost:5173"]
    upload_dir: str = "./uploads"

    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()
