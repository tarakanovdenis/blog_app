from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, Result

from src.schemas.post import PostCreate, PostUpdate
from src.models.post import Post
from src.utils.messages import messages


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_post(
    post_create: PostCreate,
    session: AsyncSession,
) -> Post | None:
    post: Post = Post(**post_create.model_dump())

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def get_posts_or_404(session: AsyncSession) -> list[Post] | None:
    stmt = select(Post)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.POSTS_WERE_NOT_FOUND,
        )

    return posts


async def get_post_by_id_or_404(
    post_id: UUID,
    session: AsyncSession,
) -> Post | None:
    stmt = select(Post).where(
        Post.id == post_id,
    )
    result: Result = await session.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.POST_WITH_THAT_ID_WAS_NOT_FOUND,
        )

    return post


async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    session: AsyncSession,
    partially: bool = False,
) -> Post | None:
    post: Post = await get_post_by_id_or_404(post_id, session)
    for name, value in post_update.model_dump(exclude_unset=partially).items():
        setattr(post, name, value)
    await session.commit()
    return post


async def delete_post_by_id(
    post_id: UUID,
    session: AsyncSession,
):
    post: Post = await get_post_by_id_or_404(post_id, session)
    await session.delete(post)
    await session.commit()


async def like_post_by_id(
    post_id: UUID,
    session: AsyncSession,
):
    post: Post = await get_post_by_id_or_404(post_id, session)
    post.like_number += 1
    await session.commit()
    return post
