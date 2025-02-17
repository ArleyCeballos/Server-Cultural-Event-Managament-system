import os

import pytest
from httpx import AsyncClient

from app.main import create_application

aplicativo_NOT_FOUND_MSG = "aplicativo not found"
aplicativoS_PREFIX = "api/aplicativos"
aplicativoS_SERVICE_URL = "http://aplicativo-db-test/"

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

aplicativo_update = {
    "date_available": "2022-02-12T21:56:22.619000+00:00",
    "equipment_options": "test2",
    "contact_name": "test2",
    "contact_email": "test2",
    "contact_phone": "test22",
    "destination_country": "test2",
    "destination_state": "test2",
    "destination_city": "test2",
    "origin_country": "test2",
    "origin_state": "test2",
    "origin_city": "test2",
    "number_available": "1",
    "equipment_descrption": "test2",
    "carrier_name": "test2",
    "mc_number": "test2",
    "dot_number": "test2",
    "email_id": 1,
}


email = {
    "client_email": "test",
    "subject": "test",
    "intake_id": "test",
    "conversation_id": "test",
    "datetime_recived": "2022-02-12T21:56:22.619000+00:00",
    "graph_type": "test",
    "entry_type": "test",
    "has_attachments": False,
    "status": 1,
}

user2 = {"username": "test2", "password": os.getenv("USER_2_PASSWORD"), "role": 1}

app = create_application()


@pytest.mark.asyncio
async def test_get_count_empty():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        response = await client.get(f"{aplicativoS_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_get_count():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(aplicativoS_PREFIX, json=aplicativo)
        response = await client.get(f"{aplicativoS_PREFIX}/count")
        assert response.status_code == 200
        assert response.json() == {"count": 1}, response.text


@pytest.mark.asyncio
async def test_get_all_empty():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        response = await client.get(aplicativoS_PREFIX)
    assert response.status_code == 200
    assert response.json() == [], response.text


@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(aplicativoS_PREFIX, json=aplicativo)
        response = await client.get(aplicativoS_PREFIX)
    assert response.status_code == 200, response.text
    assert response.json() != [], response.text
    res = response.json()[0]
    for key in aplicativo:
        assert aplicativo[key] == res[key]


@pytest.mark.asyncio
async def test_create_empty():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        response = await client.post(aplicativoS_PREFIX)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_repeat():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(aplicativoS_PREFIX, json=aplicativo)
        response = await client.post(aplicativoS_PREFIX, json=aplicativo)
    assert response.status_code == 201, response.text


@pytest.mark.asyncio
async def test_create():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        response = await client.post(aplicativoS_PREFIX, json=aplicativo)
    assert response.status_code == 201, response.text
    for key in aplicativo:
        assert aplicativo[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(aplicativoS_PREFIX, json=aplicativo)
        response = await client.get(f"{aplicativoS_PREFIX}/1")
    assert response.status_code == 200, response.text
    for key in aplicativo:
        assert aplicativo[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id_empty():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        response = await client.get(f"{aplicativoS_PREFIX}/1")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": aplicativo_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_patch_by_id():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(aplicativoS_PREFIX, json=aplicativo)
        response = await client.patch(f"{aplicativoS_PREFIX}/1", json=aplicativo_update)
    assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test_delete_empty():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        response = await client.delete(f"{aplicativoS_PREFIX}/1")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": aplicativo_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url=aplicativoS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(aplicativoS_PREFIX, json=aplicativo)
        response = await client.delete(f"{aplicativoS_PREFIX}/1")
    assert response.status_code == 204, response.text
