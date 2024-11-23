from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, str_128, str_512


if TYPE_CHECKING:
    from src.models.like import Like


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str_128]
    body: Mapped[str_512]
    likes_number: Mapped[int] = mapped_column(Integer, server_default="0")

    likes: Mapped[list[Like]] = relationship(
        "Like",
        back_populates="post",
    )

    repr_columns = (
        "id",
        "title",
        "body",
        "likes",
        "created_at",
    )
