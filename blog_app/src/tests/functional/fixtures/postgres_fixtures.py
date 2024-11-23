import pytest_asyncio

from src.db.postgres import db_helper


@pytest_asyncio.fixture(name="clear_database", scope="function", autouse=True)
async def clear_database():
    await db_helper.create_database_tables()
    yield
    await db_helper.purge_database_tables()
