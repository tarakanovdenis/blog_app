from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import select, Result, func

from src.models.like import Like
from src.utils import post_crud


if TYPE_CHECKING:
    from uuid import UUID
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.models.post import Post


async def get_post_likes_number_by_id(
    post_id: UUID,
    session: AsyncSession,
):
    # Count likes number using Like model
    stmt = select(func.count().label("Likes number")).where(
        Like.post_id == post_id,
    )
    result: Result = await session.execute(stmt)
    likes_number = result.scalar()

    # Count likes number using Post model
    # post: Post = await post_crud.get_post_by_id_or_404(
    #     post_id,
    #     session,
    # )
    # likes_number = post.likes_number

    return likes_number
