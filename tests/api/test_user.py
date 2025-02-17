import os

import pytest
from httpx import AsyncClient

from app.main import create_application

USER_NOT_FOUND_MSG = "user not found"
USERS_PREFIX = "api/users"
USERS_SERVICE_URL = "http://aplicativo-db-test/"

user = {
    "username": "test",
    "password": os.getenv("USER_PASSWORD"),
    "access_token": os.getenv("USER1_ACCESS_TOKEN"),
    "role": 1,
}

user_update = {
    "username": "test1",
    "password": os.getenv("USER_PASSWORD_UPDATE"),
}

user_update2 = {
    "username": "test1",
    "password": os.getenv("USER_PASSWORD_UPDATE"),
}

user2 = {
    "username": "test2",
    "password": os.getenv("USER_2_PASSWORD"),
    "access_token": os.getenv("USER2_ACCESS_TOKEN"),
    "role": 1,
}

app = create_application()


@pytest.mark.asyncio
async def test_get_count_empty():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        response = await client.get(f"{USERS_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_get_count():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        await client.post(USERS_PREFIX, json=user)
        response = await client.get(f"{USERS_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 1}


@pytest.mark.asyncio
async def test_get_all_empty():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        response = await client.get(USERS_PREFIX)
    assert response.status_code == 200
    assert response.json() == [], response.text


@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        await client.post(USERS_PREFIX, json=user)
        response = await client.get(USERS_PREFIX)
    assert response.status_code == 200, response.text
    assert response.json() != [], response.text
    res = response.json()[0]
    del user["password"]
    del user["role"]
    for key in user:
        assert user[key] == res[key]
    user["password"] = os.getenv("USER_PASSWORD")
    user["role"] = 1


@pytest.mark.asyncio
async def test_create_empty():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        response = await client.post(USERS_PREFIX)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        response = await client.post(USERS_PREFIX, json=user)
    assert response.status_code == 201, response.text
    del user["password"]
    del user["role"]
    for key in user:
        assert user[key] == response.json()[key]
    user["password"] = os.getenv("USER_PASSWORD")
    user["role"] = 1


@pytest.mark.asyncio
async def test_get_by_id():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        await client.post(USERS_PREFIX, json=user)
        response = await client.get(f"{USERS_PREFIX}/1")
    assert response.status_code == 200, response.text
    del user["password"]
    del user["role"]
    for key in user:
        assert user[key] == response.json()[key]
    user["password"] = os.getenv("USER_PASSWORD")
    user["role"] = 1


@pytest.mark.asyncio
async def test_get_by_id_empty():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        response = await client.get(f"{USERS_PREFIX}/1")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": USER_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_patch_by_id():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        await client.post(USERS_PREFIX, json=user)
        response = await client.patch(f"{USERS_PREFIX}/1", json=user_update)
    assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test_delete_empty():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        response = await client.delete(f"{USERS_PREFIX}/1")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": USER_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url=USERS_SERVICE_URL) as client:
        await client.post(USERS_PREFIX, json=user)
        response = await client.delete(f"{USERS_PREFIX}/1")
    assert response.status_code == 204, response.text
