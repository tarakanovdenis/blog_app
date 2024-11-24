from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import Base


if TYPE_CHECKING:
    from src.models.post import Post


class Like(Base):
    __tablename__ = "likes"

    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
    )

    post: Mapped[Post] = relationship(
        "Post",
        back_populates="likes",
    )

    repr_columns = (
        "id",
        "post_id",
        "created_at",
    )
