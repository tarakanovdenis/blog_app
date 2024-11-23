from http import HTTPStatus

import pytest

from src.tests.functional.config import test_settings


@pytest.mark.parametrize(
    "expected_answer",
    [
        (
            {
                "status": HTTPStatus.OK,
                "likes_number": 5,
            }
        )
    ]
)
@pytest.mark.asyncio
async def test_get_post_likes_number(
    make_post_request,
    make_get_request,
    expected_answer,
):
    """Test the checking the likes number of the post."""

    post_data = {
        "title": "My opinion about the film Schindler's List",
        "body": "Here it can be found a detailed description.",
    }

    body, *_ = await make_post_request(
        test_settings.blog_api_backend_url + "/posts/",
        json=post_data,
    )

    post_id = body["id"]

    for _ in range(5):
        body, _, status = await make_post_request(
            test_settings.blog_api_backend_url + f"/posts/{post_id}/like/",
        )

    body, _, status = await make_get_request(
        test_settings.blog_api_backend_url + f"/likes/post/{post_id}/"
    )

    assert status == expected_answer["status"]
    assert body == expected_answer["likes_number"]
