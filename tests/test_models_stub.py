from app.models.stub import StubModel


def test_stub_model_predicts_entities_and_intent():
	model = StubModel()
	raw = "Find the best sushi place in SF"
	intent, entities = model.predict(raw, "find the best sushi place in sf")
	assert intent["name"] == "find_restaurant"
	types = {e["type"] for e in entities}
	assert "food_type" in types
	assert "sort_by" in types
	assert "location" in types
	locs = [e for e in entities if e["type"] == "location"]
	assert any(e["value"] == "San Francisco" for e in locs)
	foods = [e for e in entities if e["type"] == "food_type"]
	assert any(e["value"] == "sushi" for e in foods)
