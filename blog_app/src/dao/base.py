from __future__ import annotations
from typing import TYPE_CHECKING

from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from uuid import UUID


class BaseDAO:
    model = None

    @classmethod
    async def create(cls, values: BaseModel, session: AsyncSession):
        logger.info(f"Creating record in the {cls.model.__name__} table")
        try:
            record = cls.model(**values.model_dump())
            session.add(record)
            await session.commit()
            await session.refresh(record)
            logger.info(
                f"Record was created successfully in the {cls.model.__name__} table"
            )
            return record
        except SQLAlchemyError as e:
            logger.error(
                f"An error occured while creating record"
                f" in the {cls.model.__name__} table: {e}"
            )

    @classmethod
    async def get_all_or_404(cls, session: AsyncSession):
        logger.info(f"Fetching all records in the {cls.model.__name__} table")
        try:
            stmt = select(cls.model)
            result: Result = await session.execute(stmt)

            if not (records := result.scalars().all()):
                logger.info(f"Records in the table {cls.model.__name__} weren't found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Records in the table {cls.model.__name__}" " weren't found."
                    ),
                )

            logger.info(f"{len(records)} records were fetched")
            return records

        except SQLAlchemyError as e:
            logger.error(
                f"An error occured while fetching all records"
                f" in the {cls.model.__name__}: {e}"
            )
            raise e

    @classmethod
    async def get_one_by_id_or_404(cls, id: UUID | int, session: AsyncSession):
        logger.info(f"Fetch one record with ID {id} in the {cls.model.__name__} table")
        try:
            stmt = select(cls.model).where(cls.model.id == id)
            result: Result = await session.execute(stmt)

            if not (record := result.scalar_one_or_none()):
                logger.info(
                    f"Record with the specified ID {id} wasn't"
                    f" found in the {cls.model.__name__}"
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Record with the specified ID {id} wasn't"
                        f" found in the {cls.model.__name__} table."
                    ),
                )
            logger.info(f"{record} record was fetched.")
            return record

        except SQLAlchemyError as e:
            logger.error(
                "An error occured while fetching record with ID"
                f" {id} in the {cls.model.__name__} table: {e}"
            )
            raise e

    @classmethod
    async def update_by_id(
        cls,
        id: UUID | int,
        values: BaseModel,
        session: AsyncSession,
        partially: bool = False,
    ):
        logger.info(
            f"Update record with ID {id} in the {cls.model.__name__} table"
            f" using {'PATCH' if partially else 'PUT'} HTTP method."
        )
        try:
            record = await cls.get_one_by_id_or_404(id, session)
            for name, value in values.model_dump(exclude_unset=partially).items():
                setattr(record, name, value)
            await session.commit()
            logger.info(
                f"Record with ID {id} in the {cls.model.__name__} table"
                f" was updated successfully using"
                f" {'PATCH' if partially else 'PUT'} HTTP method"
            )
            return record
        except SQLAlchemyError as e:
            logger.error(
                "An error occured while fetching record with ID"
                f" {id} in the table {cls.model.__name__}: {e}"
            )
            raise e

    @classmethod
    async def delete_by_id(cls, id: UUID | int, session: AsyncSession):
        logger.info(f"Delete record with ID {id} in the {cls.model.__name__} table")
        try:
            record = await cls.get_one_by_id_or_404(id, session)
            await session.delete(record)
            await session.commit()
            logger.info(
                f"Record with ID {id} in the {cls.model.__name__} table"
                " was deleted successfully"
            )
        except SQLAlchemyError as e:
            logger.error(
                "An error occured while fetching record with ID"
                f" {id} in the {cls.model.__name__} table: {e}"
            )
            raise e
