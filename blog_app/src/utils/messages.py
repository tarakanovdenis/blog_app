from dataclasses import dataclass


@dataclass
class Messages:
    POSTS_WERE_NOT_FOUND = "Posts weren't found."
    POST_WITH_THAT_ID_WAS_NOT_FOUND = (
        "Post with the specified ID was not found."
    )


messages = Messages()
