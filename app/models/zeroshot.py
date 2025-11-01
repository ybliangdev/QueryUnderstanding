from typing import Dict, List, Tuple

from app.models.base import QUModel, IntentDict, EntityDict
from app.config import get_settings
from app.nlp.preprocessor import QueryPreprocessor


_DEFAULT_MODEL = "facebook/bart-large-mnli"


class ZeroShotIntentModel(QUModel):
	"""Zero-shot intent classifier using Hugging Face transformers.

	Also performs simple entity extraction using spaCy NER via the provided QueryPreprocessor.
	"""

	def __init__(self, preprocessor: QueryPreprocessor, candidate_labels: List[str] | None = None, model_name: str | None = None) -> None:
		self.settings = get_settings()
		self.preprocessor = preprocessor
		self._pipeline = None  # lazy
		labels_csv = self.settings.intents_csv
		self.labels: List[str] = candidate_labels or [l.strip() for l in labels_csv.split(",") if l.strip()]
		self.model_name = model_name or _DEFAULT_MODEL

	def _load_pipeline(self):
		if self._pipeline is not None:
			return self._pipeline
		# Lazy imports to avoid heavy deps when running stub
		from transformers import pipeline  # type: ignore
		self._pipeline = pipeline("zero-shot-classification", model=self.model_name)
		return self._pipeline

	def _predict_intent(self, text: str) -> IntentDict:
		pipe = self._load_pipeline()
		result = pipe(text, candidate_labels=self.labels, multi_label=False)
		label = result["labels"][0]
		score = float(result["scores"][0])
		return {"name": label, "confidence": max(0.0, min(1.0, score))}

	def _extract_entities(self, raw_text: str) -> List[EntityDict]:
		entities: List[EntityDict] = []
		doc = self.preprocessor.nlp(raw_text)
		for ent in doc.ents:
			etype = ent.label_
			mapped: str | None = None
			if etype in ("GPE", "LOC"):
				mapped = "location"
			elif etype in ("ORG",):
				# Heuristic: organizations might be restaurants; we do not assign for now
				mapped = None
			elif etype in ("PRODUCT",):
				mapped = "food_type"
			if mapped:
				entities.append({
					"text": ent.text,
					"value": ent.text,
					"type": mapped,
					"start_char": int(ent.start_char),
					"end_char": int(ent.end_char),
				})
		return entities

	def predict(self, raw_text: str, normalized_text: str) -> Tuple[IntentDict, List[EntityDict]]:
		intent = self._predict_intent(raw_text)
		entities = self._extract_entities(raw_text)
		return intent, entities


