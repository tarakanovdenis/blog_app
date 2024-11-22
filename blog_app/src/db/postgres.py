from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from src.models.base import Base
from src.core.config import settings


class DatabaseHelper:

    def __init__(self, url: str, echo: bool = False):
        self.url = url
        self.echo = echo

        self.engine = create_async_engine(
            self.url,
            self.echo,
        )

        self.async_session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_database_tables(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def purge_database_tables(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)


db_helper = DatabaseHelper(
    url=settings.db_settings.database_url_asyncpg,
    echo=settings.db_settings.db_echo,
)
