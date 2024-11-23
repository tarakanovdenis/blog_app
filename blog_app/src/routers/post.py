from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, Path

from src.schemas.post import (
    PostCreate,
    PostRead,
    PostUpdate,
)
from src.db.postgres import db_helper
from src.utils import post_crud


from sqlalchemy.ext.asyncio import AsyncSession
# if TYPE_CHECKING:


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostRead,
)
async def create_post(
    post_create: PostCreate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create post

    Parameters:
    **title** (str): post title
    **body** (str): post body

    Return value:
    **post** (PostRead): post
    """
    return await post_crud.create_post(
        post_create,
        session,
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PostRead],
)
async def get_posts(session: AsyncSession = Depends(db_helper.get_session)):
    """
    Get posts

    Return value:
    **posts** (list[PostRead]): lists of posts
    """
    return await post_crud.get_posts_or_404(session)


@router.get(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostRead,
)
async def get_post(
    post_id: Annotated[UUID, Path(description="Post ID (UUID)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get post using it's ID

    Parameters:
    **post_id** (UUID): post ID (UUID4)

    Return value:
    **post** (PostRead): post
    """
    return await post_crud.get_post_by_id_or_404(
        post_id,
        session,
    )


@router.put(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostRead,
)
async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Update post using ID

    Parameters:
    **post_id** (UUID): post ID (UUID4)
    **title** (str): post title
    **body** (str): post body

    Return value:
    **post** (PostRead): updated post
    """
    return await post_crud.update_post(
        post_id,
        post_update,
        session,
    )


@router.patch(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostRead,
)
async def update_post_partially(
    post_id: UUID,
    post_update: PostUpdate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Update post using ID partially

    Parameters:
    **post_id** (UUID): post ID (UUID4)
    **title** (str): post title (optional)
    **body** (str): post body (optional)
    """
    return await post_crud.update_post(
        post_id,
        post_update,
        session,
        partially=True,
    )


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: Annotated[UUID, Path(description="Post ID (UUID)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete post using ID

    Parameters:
    **post_id** (UUID): post ID (UUID4)
    """
    return await post_crud.delete_post_by_id(
        post_id,
        session,
    )
