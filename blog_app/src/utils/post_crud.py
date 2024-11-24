from __future__ import annotations
from typing import TYPE_CHECKING

from src.schemas.post import PostCreate, PostUpdate
from src.models.post import Post
from src.dao.dao import PostDAO


if TYPE_CHECKING:
    from uuid import UUID
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_post(
    post_create: PostCreate,
    session: AsyncSession,
) -> Post | None:
    return await PostDAO.create(post_create, session)


async def get_posts_or_404(session: AsyncSession) -> list[Post] | None:
    return await PostDAO.get_all_or_404(session)


async def get_post_by_id_or_404(
    post_id: UUID,
    session: AsyncSession,
) -> Post | None:
    return await PostDAO.get_one_by_id_or_404(post_id, session)


async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    session: AsyncSession,
    partially: bool = False,
) -> Post | None:
    return await PostDAO.update_by_id(post_id, post_update, session, partially)


async def delete_post_by_id(
    post_id: UUID,
    session: AsyncSession,
):
    return await PostDAO.delete_by_id(post_id, session)


async def like_post_by_id(
    post_id: UUID,
    session: AsyncSession,
) -> Post | None:
    return await PostDAO.like_post_by_id(post_id, session)
