from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthz_ok():
	resp = client.get("/healthz")
	assert resp.status_code == 200
	assert resp.json() == {"status": "ok"}


def test_readyz_shape():
	resp = client.get("/readyz")
	assert resp.status_code == 200
	body = resp.json()
	assert body.get("ready") is True
	backend = body.get("backend")
	assert isinstance(backend, str)
	assert len(backend) > 0


def test_parse_includes_backend_header():
	resp = client.post("/v1/parse", json={"text": "Find pizza in NYC"})
	assert resp.status_code == 200
	assert resp.headers.get("X-QU-Backend")
