from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_parse_requires_non_empty_text():
	resp = client.post("/v1/parse", json={"text": ""})
	assert resp.status_code == 422


def test_parse_missing_text_field():
	resp = client.post("/v1/parse", json={})
	assert resp.status_code == 422
