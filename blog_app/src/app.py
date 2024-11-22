from fastapi import FastAPI

from src.core.config import settings


app = FastAPI(
    title=settings.project_settings.title,
    description=settings.project_settings.description,
    version=settings.project_settings.version,
    docs_url=settings.project_settings.docs_url,
    openapi_url=settings.project_settings.openapi_url,
)
