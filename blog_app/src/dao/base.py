from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession):
        logger.info(f"Fetching all rows in the {cls.model.__name__} table")
        try:
            stmt = select(cls.model)
            result: Result = await session.execute(stmt)

            if not (records := result.scalars().all()):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Records in the table {cls.model.__name__} were found."
                )

            logger.info(f"{len(records)} records were fetched")
            return records

        except SQLAlchemyError as e:
            logger.error(
                f"An error occured while fetching all rows"
                f" in the {cls.model.__name__}: {e}"
            )
            raise
