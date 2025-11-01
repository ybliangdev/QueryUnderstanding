from app.config import get_settings
from app.nlp.preprocessor import QueryPreprocessor
from app.models.base import QUModel
from app.models.stub import StubModel


def create_model(preprocessor: QueryPreprocessor) -> QUModel:
	settings = get_settings()
	backend = (settings.model_backend or "stub").lower()
	if backend == "zeroshot":
		# Lazy import to avoid transformers dependency when not needed
		from app.models.zeroshot import ZeroShotIntentModel  # type: ignore
		return ZeroShotIntentModel(preprocessor=preprocessor)
	# default
	return StubModel()


