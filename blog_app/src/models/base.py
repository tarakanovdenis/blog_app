from typing import Annotated, Any
from uuid import uuid4

from sqlalchemy import MetaData, DateTime, text, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import UUID

from src.core.config import settings


uniq_str_128 = Annotated[
    str, mapped_column(String(128), unique=True, nullable=False)
]
str_512 = Annotated[
    str, mapped_column(String(512), nullable=False)
]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db_settings.naming_convention,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())")
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now()"),
        onupdate=text("TIMEZONE('utc', now()"),
    )

    repr_column_number = 1
    repr_columns = tuple()

    def to_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        columns = []

        for idx, column in enumerate(self.__table__.columns.keys()):
            if column in self.repr_columns or idx < self.repr_column_number:
                columns.append(f"{column}={getattr(self, column)}")

        return f"<{self.__class__.__name__} {', '.join(columns)}>"
