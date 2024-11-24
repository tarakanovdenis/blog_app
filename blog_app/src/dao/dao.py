from __future__ import annotations
from typing import TYPE_CHECKING

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from src.dao.base import BaseDAO
from src.models.post import Post
from src.models.like import Like


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PostDAO(BaseDAO):
    model = Post

    @classmethod
    async def like_post_by_id(
        cls,
        post_id,
        session: AsyncSession,
    ) -> Post | None:
        logger.info(
            f"Adding like to the post with ID {post_id}"
            f" in the {cls.model.__name__} table"
        )
        try:
            post: Post = await cls.get_one_by_id_or_404(post_id, session)
            post.likes_number += 1

            like: Like = Like(post_id=post.id)
            session.add(like)
            await session.commit()
            logger.info(
                f"Like {like} was added to the post with ID {post_id} successfully."
            )
            return post
        except SQLAlchemyError as e:
            logger.error(
                f"An error occured while adding like (creating like {like}"
                f" record) to the post with ID {post_id} in the"
                f" {cls.model.__name__} table: {e}"
            )
            raise e
