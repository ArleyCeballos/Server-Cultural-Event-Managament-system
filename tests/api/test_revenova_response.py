import pytest
from httpx import AsyncClient

from app.main import create_application

REVENOVA_NOT_FOUND_MSG = "revenova response not found"
REVENOVA_PREFIX = "api/revenova"
EMAILS_SERVICE_URL = "http://aplicativo-db-test/"


revenova_response = {
    "description": "test",
    "response": {},
    "aplicativo_id": 1,
}

revenova_response2 = {
    "description": "test2",
    "response": {},
    "aplicativo_id": 1,
}

aplicativo = {
    "date_available": "2022-02-12T21:56:22.619000+00:00",
    "equipment_options": "test",
    "contact_name": "test",
    "contact_email": "test",
    "contact_phone": "test",
    "destination_country": "test",
    "destination_state": "test",
    "destination_city": "test",
    "origin_country": "test",
    "origin_state": "test",
    "origin_city": "test",
    "number_available": "1",
    "equipment_description": "test",
    "carrier_name": "test",
    "mc_number": "test",
    "dot_number": "test",
    "email_id": 1,
}

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

app = create_application()


@pytest.mark.asyncio
async def test_get_count_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(f"{REVENOVA_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_get_count():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post("api/aplicativos", json=aplicativo)
        await client.post(REVENOVA_PREFIX, json=revenova_response)
        response = await client.get(f"{REVENOVA_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 1}


@pytest.mark.asyncio
async def test_get_all_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(REVENOVA_PREFIX)
    assert response.status_code == 200
    assert response.json() == [], response.text


@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post("api/aplicativos", json=aplicativo)
        await client.post(REVENOVA_PREFIX, json=revenova_response)
        response = await client.get(REVENOVA_PREFIX)
    assert response.status_code == 200, response.text
    assert response.json() != [], response.text
    res = response.json()[0]
    for key in revenova_response:
        assert revenova_response[key] == res[key], response.text


@pytest.mark.asyncio
async def test_create_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.post(REVENOVA_PREFIX)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post("api/aplicativos", json=aplicativo)
        response = await client.post(REVENOVA_PREFIX, json=revenova_response)
    assert response.status_code == 201, response.text
    for key in revenova_response:
        assert revenova_response[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post("api/aplicativos", json=aplicativo)
        await client.post(REVENOVA_PREFIX, json=revenova_response)
        response = await client.get(f"{REVENOVA_PREFIX}/1")
        assert response.status_code == 200, response.text
        for key in revenova_response:
            assert revenova_response[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(f"{REVENOVA_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": REVENOVA_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_patch_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post("api/aplicativos", json=aplicativo)
        await client.post(REVENOVA_PREFIX, json=revenova_response)
        response = await client.patch(f"{REVENOVA_PREFIX}/1", json=revenova_response2)
        assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test_delete_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.delete(f"{REVENOVA_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": REVENOVA_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post("api/aplicativos", json=aplicativo)
        await client.post(REVENOVA_PREFIX, json=revenova_response)
        response = await client.delete(f"{REVENOVA_PREFIX}/1")
        assert response.status_code == 204, response.text
