from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_parse_contract_and_stub_logic():
	resp = client.post("/v1/parse", json={"text": "Can you find me a good pizza place in NYC?"})
	assert resp.status_code == 200, resp.text
	body = resp.json()
	assert body["raw_query"].startswith("Can you")
	assert "normalized_query" in body
	assert body["intent"]["name"] == "find_restaurant"
	assert 0.0 <= body["intent"]["confidence"] <= 1.0
	entities = body["entities"]
	assert isinstance(entities, list)

	# Check for expected entities
	types = {e["type"] for e in entities}
	assert "food_type" in types
	assert "location" in types
	assert "sort_by" in types

	locs = [e for e in entities if e["type"] == "location"]
	assert any(e["value"] in ("New York City", "NYC") for e in locs)


