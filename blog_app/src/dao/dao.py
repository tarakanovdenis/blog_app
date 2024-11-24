from src.dao.base import BaseDAO
from src.models.post import Post


class PostDAO(BaseDAO):
    model = Post
