from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, str_128, str_512


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str_128]
    body: Mapped[str_512]
    likes: Mapped[int] = mapped_column(Integer, server_default="0")

    repr_columns = (
        "id",
        "title",
        "body",
        "likes",
        "created_at",
    )
