from fastapi import FastAPI

from src.core.config import settings
from src.routers.post import router as post_router
from src.routers.like import router as like_router


app = FastAPI(
    title=settings.project_settings.title,
    description=settings.project_settings.description,
    version=settings.project_settings.version,
    docs_url=settings.project_settings.docs_url,
    openapi_url=settings.project_settings.openapi_url,
)
app.include_router(
    post_router,
    prefix="/posts",
    tags=["Post Management Endpoints"],
)
app.include_router(
    like_router,
    prefix="/likes",
    tags=["Like Management Endpoints"],
)
