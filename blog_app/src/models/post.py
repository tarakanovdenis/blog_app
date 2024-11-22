from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, uniq_str_128, str_512


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[uniq_str_128]
    descriptin: Mapped[str_512]
    likes: Mapped[int] = mapped_column(Integer, server_default="0")

    repr_columns = (
        "id",
        "title",
        "description",
        "created_at",
    )
