import os

import pytest
from httpx import AsyncClient

from app.main import create_application

ASSOCIATED_NOT_FOUND_MSG = "associated emails not found"
ASSOCIATED_PREFIX = "api/associated-emails"
EMAILS_SERVICE_URL = "http://aplicativo-db-test/"


associated_email = {
    "client_email": "test",
    "user_id": 1,
}

associated_email2 = {
    "client_email": "test2",
    "user_id": 1,
}

user = {
    "username": "test",
    "password": os.getenv("USER_PASSWORD"),
    "access_token": os.getenv("USER1_ACCESS_TOKEN"),
    "role": 1,
}

app = create_application()


@pytest.mark.asyncio
async def test_get_count_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(f"{ASSOCIATED_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_get_count():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/users", json=user)
        await client.post(ASSOCIATED_PREFIX, json=associated_email)
        response = await client.get(f"{ASSOCIATED_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 1}


@pytest.mark.asyncio
async def test_get_all_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(ASSOCIATED_PREFIX)
    assert response.status_code == 200
    assert response.json() == [], response.text


@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/users", json=user)
        await client.post(ASSOCIATED_PREFIX, json=associated_email)
        response = await client.get(ASSOCIATED_PREFIX)
    assert response.status_code == 200, response.text
    assert response.json() != [], response.text
    res = response.json()[0]
    for key in associated_email:
        assert associated_email[key] == res[key], response.text


@pytest.mark.asyncio
async def test_create_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.post(ASSOCIATED_PREFIX)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/users", json=user)
        response = await client.post(ASSOCIATED_PREFIX, json=associated_email)
    assert response.status_code == 201, response.text
    for key in associated_email:
        assert associated_email[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/users", json=user)
        await client.post(ASSOCIATED_PREFIX, json=associated_email)
        response = await client.get(f"{ASSOCIATED_PREFIX}/1")
        assert response.status_code == 200, response.text
        for key in associated_email:
            assert associated_email[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(f"{ASSOCIATED_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": ASSOCIATED_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_patch_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/users", json=user)
        await client.post(ASSOCIATED_PREFIX, json=associated_email)
        response = await client.patch(f"{ASSOCIATED_PREFIX}/1", json=associated_email2)
        assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test_delete_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.delete(f"{ASSOCIATED_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": ASSOCIATED_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/users", json=user)
        await client.post(ASSOCIATED_PREFIX, json=associated_email)
        response = await client.delete(f"{ASSOCIATED_PREFIX}/1")
        assert response.status_code == 204, response.text
