from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class PostBase(BaseModel):
    id: UUID
    title: str = Field(
        min_length=3,
        max_length=128,
        description="Post title (length from 3 to 128 characters)",
    )
    description: str = Field(
        min_length=3,
        max_length=512,
        description="Post description (length from 3 to 512 characters)",
    )
    updated_at: datetime
    created_at: datetime


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    likes: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class PostUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
