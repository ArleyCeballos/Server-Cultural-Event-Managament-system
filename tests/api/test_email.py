import pytest
from httpx import AsyncClient

from app.main import create_application

EMAIL_NOT_FOUND_MSG = "email not found"
EMAILS_PREFIX = "api/emails"
EMAILS_SERVICE_URL = "http://aplicativo-db-test/"


email = {
    "client_email": "test",
    "subject": "test",
    "intake_id": "test",
    "conversation_id": "test",
    "datetime_recived": "2022-02-12T21:56:22.619000+00:00",
    "entry_type": "test",
    "has_attachments": False,
    "status": 1,
}

email2 = {
    "client_email": "test2",
    "subject": "test2",
    "intake_id": "test",
    "conversation_id": "test2",
    "datetime_recived": "2022-02-12T22:56:22.619000+00:00",
    "entry_type": "test2",
    "has_attachments": False,
    "status": 1,
}

data = {
    "id": 1,
    "client_email": "test",
    "status": 1,
    "subject": "test",
    "assign_to": None,
}

email_by_id = {
    "id": 1,
    "client_email": "test",
    "status": 1,
    "subject": "test",
}


app = create_application()


@pytest.mark.asyncio
async def test_get_count_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(f"{EMAILS_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_get_count():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post(EMAILS_PREFIX, json=email)
        response = await client.get(f"{EMAILS_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 1}


@pytest.mark.asyncio
async def test_get_all_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(EMAILS_PREFIX)
    assert response.status_code == 200
    assert response.json() == [], response.text


@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post(EMAILS_PREFIX, json=email)
        response = await client.get(EMAILS_PREFIX)
    assert response.status_code == 200, response.text
    assert response.json() != [], response.text
    res = response.json()[0]
    for key in email:
        assert email[key] == res[key], response.text


@pytest.mark.asyncio
async def test_create_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.post(EMAILS_PREFIX)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.post(EMAILS_PREFIX, json=email)
    assert response.status_code == 201, response.text
    for key in email:
        assert email[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post(EMAILS_PREFIX, json=email)
        response = await client.get(f"{EMAILS_PREFIX}/1")
        assert response.status_code == 200, response.text
        for key in email_by_id:
            assert email_by_id[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(f"{EMAILS_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": EMAIL_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_patch_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post(EMAILS_PREFIX, json=email)
        response = await client.patch(f"{EMAILS_PREFIX}/1", json=email2)
        assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test_delete_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.delete(f"{EMAILS_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": EMAIL_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post(EMAILS_PREFIX, json=email)
        response = await client.delete(f"{EMAILS_PREFIX}/1")
        assert response.status_code == 204, response.text
