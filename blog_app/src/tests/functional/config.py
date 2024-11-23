from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


BASE_DIR = Path(__file__).parent
ENV_FILE_PATH = BASE_DIR / ".env"


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class TestSettings(EnvSettings):
    blog_api_backend_host: str = Field(default="blog_api_backend_for_test")
    blog_api_backend_port: int = Field(default=8000)

    @property
    def blog_api_backend_url(self):
        return (
            f"http://{self.blog_api_backend_host}:"
            f"{self.blog_api_backend_port}"
        )


test_settings = TestSettings()
