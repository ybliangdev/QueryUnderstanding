import re
from typing import Dict, List, Tuple

from app.models.base import QUModel, IntentDict, EntityDict


_FOOD_WORDS = [
	"pizza",
	"sushi",
	"burger",
	"tacos",
	"taco",
	"pasta",
	"ramen",
	"steak",
	"salad",
	"noodles",
]

_WEATHER_WORDS = [
	"weather",
	"temperature",
	"rain",
	"snow",
	"forecast",
	"wind",
]

_REMINDER_WORDS = [
	"remind",
	"reminder",
	"schedule",
	"remember",
	"note",
]

_SORT_WORDS = [
	"best",
	"good",
	"top",
	"cheap",
	"cheapest",
	"nearby",
]

_LOCATION_NORMALIZE = {
	"nyc": "New York City",
	"sf": "San Francisco",
	"la": "Los Angeles",
	"bay area": "San Francisco Bay Area",
}


class StubModel(QUModel):
	"""Deterministic rules-based model for Phase 1."""

	def _detect_intent(self, text: str, lowered: str) -> IntentDict:
		if any(w in lowered for w in _FOOD_WORDS + ["restaurant", "eat", "diner", "food"]):
			return {"name": "find_restaurant", "confidence": 0.95}
		if any(w in lowered for w in _WEATHER_WORDS):
			return {"name": "get_weather", "confidence": 0.92}
		if any(w in lowered for w in _REMINDER_WORDS) or re.search(r"\b(\d{1,2})(am|pm)\b", lowered):
			return {"name": "schedule_reminder", "confidence": 0.90}
		return {"name": "find_restaurant", "confidence": 0.50}

	def _match_spans(self, raw_text: str, pattern: str) -> List[Tuple[int, int, str]]:
		spans: List[Tuple[int, int, str]] = []
		for m in re.finditer(pattern, raw_text, flags=re.IGNORECASE):
			spans.append((m.start(), m.end(), m.group(0)))
		return spans

	def _extract_food(self, raw_text: str) -> List[EntityDict]:
		entities: List[EntityDict] = []
		pattern = r"\b(" + "|".join(map(re.escape, _FOOD_WORDS)) + r")(?:\s+place)?\b"
		for start, end, txt in self._match_spans(raw_text, pattern):
			value = txt.lower().replace(" place", "")
			entities.append({
				"text": txt,
				"value": value,
				"type": "food_type",
				"start_char": start,
				"end_char": end,
			})
		return entities

	def _extract_sort(self, raw_text: str) -> List[EntityDict]:
		entities: List[EntityDict] = []
		pattern = r"\b(" + "|".join(map(re.escape, _SORT_WORDS)) + r")\b"
		for start, end, txt in self._match_spans(raw_text, pattern):
			entities.append({
				"text": txt,
				"value": txt.lower(),
				"type": "sort_by",
				"start_char": start,
				"end_char": end,
			})
		return entities

	def _extract_location(self, raw_text: str) -> List[EntityDict]:
		entities: List[EntityDict] = []
		# Handle "in <location>" pattern
		for start, end, txt in self._match_spans(raw_text, r"\bin\s+([A-Za-z][A-Za-z\s\.]+)\b"):
			loc_text = txt.split(" ", 1)[1]
			value = _LOCATION_NORMALIZE.get(loc_text.strip().lower(), loc_text.strip())
			entities.append({
				"text": loc_text,
				"value": value,
				"type": "location",
				"start_char": start + 3,  # after 'in '
				"end_char": end,
			})
		# Handle common abbreviations like NYC, SF, LA
		for start, end, txt in self._match_spans(raw_text, r"\b(NYC|SF|LA)\b"):
			value = _LOCATION_NORMALIZE.get(txt.lower(), txt)
			entities.append({
				"text": txt,
				"value": value,
				"type": "location",
				"start_char": start,
				"end_char": end,
			})
		return entities

	def predict(self, raw_text: str, normalized_text: str) -> Tuple[IntentDict, List[EntityDict]]:
		lowered = normalized_text
		intent = self._detect_intent(raw_text, lowered)
		entities: List[EntityDict] = []
		entities.extend(self._extract_food(raw_text))
		entities.extend(self._extract_sort(raw_text))
		entities.extend(self._extract_location(raw_text))
		return intent, entities


