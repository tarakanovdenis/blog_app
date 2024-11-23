from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from uuid import UUID

from fastapi import APIRouter, status, Path, Depends

from src.db.postgres import db_helper
from src.utils import like_crud


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get(
    "/post/{post_id}",
    status_code=status.HTTP_200_OK,
)
async def get_post_likes_number(
    post_id: Annotated[UUID, Path(desctiption="Post ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get the number of likes for a post using it's ID

    Return value:
    **likes_number** (int): the number of likes
    """
    return await like_crud.get_post_likes_number_by_id(
        post_id,
        session
    )
