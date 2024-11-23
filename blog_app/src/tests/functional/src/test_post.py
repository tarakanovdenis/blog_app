from http import HTTPStatus

import pytest

from src.tests.functional.config import test_settings


@pytest.mark.parametrize(
    "expected_answer",
    [
        (
            {
                "status": HTTPStatus.CREATED,
                "title": "My opinion about the film Schindler's List",
                "body": "Here it can be found a detailed description.",
            }
        )
    ]
)
@pytest.mark.asyncio
async def test_create_post(
    make_post_request,
    expected_answer,
):
    """Test the creating the post."""
    post_data = {
        "title": "My opinion about the film Schindler's List",
        "body": "Here it can be found a detailed description.",
    }

    body, _, status = await make_post_request(
        test_settings.blog_api_backend_url + "/posts/",
        json=post_data,
    )

    assert status == expected_answer["status"]
    assert body["title"] == expected_answer["title"]
    assert body["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        (
            {
                "status": HTTPStatus.OK,
                "post_number": 5,
            }
        )
    ]
)
@pytest.mark.asyncio
async def test_get_posts(
    make_post_request,
    make_get_request,
    expected_answer,
):
    """Test the retrieving the post list."""
    post_data = {
        "title": "My opinion about the film Schindler's List",
        "body": "Here it can be found a detailed description.",
    }

    for _ in range(5):
        body, _, status = await make_post_request(
            test_settings.blog_api_backend_url + "/posts/",
            json=post_data,
        )

    body, _, status = await make_get_request(
        test_settings.blog_api_backend_url + "/posts/",
    )

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["post_number"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        (
            {
                "status": HTTPStatus.OK,
                "title": "My opinion about the film Schindler's List",
                "body": "Here it can be found a detailed description.",
            }
        )
    ]
)
@pytest.mark.asyncio
async def test_get_post(
    make_post_request,
    make_get_request,
    expected_answer,
):
    """Test the retrieving the post details."""

    post_data = {
        "title": "My opinion about the film Schindler's List",
        "body": "Here it can be found a detailed description.",
    }

    body, _, status = await make_post_request(
            test_settings.blog_api_backend_url + "/posts/",
            json=post_data,
        )

    post_id = body["id"]

    body, _, status = await make_get_request(
        test_settings.blog_api_backend_url + f"/posts/{post_id}",
    )

    assert status == expected_answer["status"]
    assert body["title"] == expected_answer["title"]
    assert body["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        (
            {
                "status": HTTPStatus.OK,
                "title": "My opinion about the film Schindler's List (UPDATED)",
                "body": "Here it can be found a detailed description.",
            }
        )
    ]
)
@pytest.mark.asyncio
async def test_update_post_using_put_method(
    make_post_request,
    make_put_request,
    expected_answer,
):
    """Test the updating the post using PUT HTTP method."""
    post_data = {
        "title": "My opinion about the film Schindler's List",
        "body": "Here it can be found a detailed description.",
    }

    body, *_ = await make_post_request(
            test_settings.blog_api_backend_url + "/posts/",
            json=post_data,
        )

    post_id = body["id"]

    updated_post_data = {
        "title": "My opinion about the film Schindler's List (UPDATED)",
        "body": "Here it can be found a detailed description.",
    }

    body, _, status = await make_put_request(
        test_settings.blog_api_backend_url + f"/posts/{post_id}",
        json=updated_post_data,
    )

    assert status == expected_answer["status"]
    assert body["title"] == expected_answer["title"]
    assert body["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        (
            {
                "status": HTTPStatus.OK,
                "title": "My opinion about the film Schindler's List (UPDATED)",
                "body": "Here it can be found a detailed description.",
            }
        )
    ]
)
@pytest.mark.asyncio
async def test_update_post_using_patch_method(
    make_post_request,
    make_patch_request,
    expected_answer,
):
    """Test the updating the post using PATCH HTTP method."""
    post_data = {
        "title": "My opinion about the film Schindler's List",
        "body": "Here it can be found a detailed description.",
    }

    body, *_ = await make_post_request(
            test_settings.blog_api_backend_url + "/posts/",
            json=post_data,
        )

    post_id = body["id"]

    updated_post_data = {
        "title": "My opinion about the film Schindler's List (UPDATED)",
    }

    body, _, status = await make_patch_request(
        test_settings.blog_api_backend_url + f"/posts/{post_id}",
        json=updated_post_data,
    )

    assert status == expected_answer["status"]
    assert body["title"] == expected_answer["title"]
    assert body["body"] == expected_answer["body"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        (
            {
                "status": HTTPStatus.NO_CONTENT,
            }
        )
    ]
)
@pytest.mark.asyncio
async def test_delete_post(
    make_post_request,
    make_delete_request,
    expected_answer,
):
    """Test the deleting the post."""
    post_data = {
        "title": "My opinion about the film Schindler's List",
        "body": "Here it can be found a detailed description.",
    }

    body, *_ = await make_post_request(
            test_settings.blog_api_backend_url + "/posts/",
            json=post_data,
        )

    post_id = body["id"]

    *_, status = await make_delete_request(
        test_settings.blog_api_backend_url + f"/posts/{post_id}",
    )

    assert status == expected_answer["status"]
