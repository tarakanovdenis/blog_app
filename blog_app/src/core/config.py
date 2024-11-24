from pathlib import Path
import json

from loguru import logger
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

logger.remove()
logger.add(
    BASE_DIR / "logs" / "loguru_access.log",
    level="INFO",
    rotation="100 MB",
)
logger.add(
    BASE_DIR / "logs" / "loguru_error.log",
    level="ERROR",
    rotation="300 MB",
)

log_config_file = str(BASE_DIR) + "/logs/config.json"

with open(log_config_file, "r") as config:
    log_config = json.load(config)


class ProjectSettings(BaseModel):
    title: str = "Blog Application"
    description: str = (
        "Here it can be found information about the endpoints"
        " and data types of the available schemes of the endpoints"
    )
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    version: str = "0.1.0"


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_fil=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )


class DatabaseSettings(EnvSettings):
    postgres_user: str = Field(default="app")
    postgres_password: str = Field(default="123qwe")
    postgres_db: str = Field(default="blog_api_database")
    postgres_host: str = Field(default="blog_api_db")
    postgres_port: int = Field(default=5432)

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def database_url_asyncpg(self):
        # postgresql+asyncpg://user:password@host:port/db
        return (
            f"postgresql+asyncpg://{self.postgres_user}"
            f":{self.postgres_password}@{self.postgres_host}"
            f":{self.postgres_port}/{self.postgres_db}"
        )

    db_echo: bool = Field(default=True)


class Settings(BaseSettings):
    project_settings: ProjectSettings = ProjectSettings()
    db_settings: DatabaseSettings = DatabaseSettings()


settings = Settings()
