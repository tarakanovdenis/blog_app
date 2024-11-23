import pytest_asyncio
from aiohttp import ClientSession


@pytest_asyncio.fixture(name="client_session", scope="session")
async def client_session():
    client_session = ClientSession()
    yield client_session
    await client_session.close()


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(client_session: ClientSession):
    async def inner(url, headers: dict = None, params: dict = None):
        async with client_session.get(
            url,
            headers=headers,
            params=params,
        ) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return body, headers, status

    return inner


@pytest_asyncio.fixture(name="make_post_request")
def make_post_request(client_session: ClientSession):
    async def inner(
        url,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
        json: dict = None,
    ):
        async with client_session.post(
            url,
            data=data,
            params=params,
            headers=headers,
            json=json,
        ) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return body, headers, status

    return inner


@pytest_asyncio.fixture(name="make_put_request")
def make_put_request(client_session: ClientSession):
    async def inner(
        url,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
        json: dict = None,
    ):
        async with client_session.put(
            url,
            data=data,
            params=params,
            headers=headers,
            json=json,
        ) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return body, headers, status

    return inner


@pytest_asyncio.fixture(name="make_patch_request")
def make_patch_request(client_session: ClientSession):
    async def inner(
        url,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
        json: dict = None,
    ):
        async with client_session.patch(
            url,
            data=data,
            params=params,
            headers=headers,
            json=json,
        ) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return body, headers, status

    return inner


@pytest_asyncio.fixture(name="make_delete_request")
def make_delete_request(client_session: ClientSession):
    async def inner(
        url,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
        json: dict = None,
    ):
        async with client_session.delete(
            url,
            data=data,
            params=params,
            headers=headers,
            json=json,
        ) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return body, headers, status

    return inner


