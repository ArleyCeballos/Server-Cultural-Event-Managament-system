import pytest
from httpx import AsyncClient

from app.main import create_application

OCR_NOT_FOUND_MSG = "entities response not found"
OCR_PREFIX = "api/entities"
EMAILS_SERVICE_URL = "http://aplicativo-db-test/"


ocr_response = {
    "kind": "test",
    "email_id": 1,
}

ocr_response2 = {
    "kind": "test2",
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
        response = await client.get(f"{OCR_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_get_count():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(OCR_PREFIX, json=ocr_response)
        response = await client.get(f"{OCR_PREFIX}/count")
    assert response.status_code == 200
    assert response.json() == {"count": 1}


@pytest.mark.asyncio
async def test_get_all_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(OCR_PREFIX)
    assert response.status_code == 200
    assert response.json() == [], response.text


@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(OCR_PREFIX, json=ocr_response)
        response = await client.get(OCR_PREFIX)
    assert response.status_code == 200, response.text
    assert response.json() != [], response.text
    res = response.json()[0]
    for key in ocr_response:
        assert ocr_response[key] == res[key], response.text


@pytest.mark.asyncio
async def test_create_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.post(OCR_PREFIX)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        response = await client.post(OCR_PREFIX, json=ocr_response)
    assert response.status_code == 201, response.text
    for key in ocr_response:
        assert ocr_response[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(OCR_PREFIX, json=ocr_response)
        response = await client.get(f"{OCR_PREFIX}/1")
        assert response.status_code == 200, response.text
        for key in ocr_response:
            assert ocr_response[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_by_id_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.get(f"{OCR_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": OCR_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_patch_by_id():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(OCR_PREFIX, json=ocr_response)
        response = await client.patch(f"{OCR_PREFIX}/1", json=ocr_response2)
        assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test_delete_empty():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        response = await client.delete(f"{OCR_PREFIX}/1")
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": OCR_NOT_FOUND_MSG}


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url=EMAILS_SERVICE_URL) as client:
        await client.post("api/emails", json=email)
        await client.post(OCR_PREFIX, json=ocr_response)
        response = await client.delete(f"{OCR_PREFIX}/1")
        assert response.status_code == 204, response.text
