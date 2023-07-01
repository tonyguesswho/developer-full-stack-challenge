from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, validator

PROJECT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # DEBUG
    DEBUG: bool

    # TOKENS
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # SECURITY
    SECRET_KEY: str

    # PROJECT NAME, API PREFIX, CORS ORIGINS
    PROJECT_NAME: str
    API_STR: str = "/api"
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]]

    # POSTGRESQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    # VALIDATORS
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def _assemble_db_connection(cls, v: Optional[str], values: Dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        if values.get("DEBUG"):
            postgres_server = "localhost"
        else:
            postgres_server = values.get("POSTGRES_SERVER")

        return AnyUrl.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=postgres_server or "localhost",
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True


settings: Settings = Settings()
