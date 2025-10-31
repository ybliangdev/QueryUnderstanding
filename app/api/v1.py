from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.config import get_settings
from app.schemas.request import ParseRequest
from app.schemas.response import ParseResponse, Intent, Entity
from app.timing import now_ms, elapsed_ms
from app.nlp.preprocessor import QueryPreprocessor
from app.models.stub import StubModel


router = APIRouter()


_settings = get_settings()
_preprocessor = QueryPreprocessor(keep_stopwords=True, remove_punct=True)
_model = StubModel()


@router.post("/parse", response_model=ParseResponse)
def parse_query(request: ParseRequest):
	start = now_ms()
	raw = request.text
	normalized = _preprocessor.preprocess_to_text(raw)
	intent_dict, entity_dicts = _model.predict(raw, normalized)
	response = ParseResponse(
		raw_query=raw,
		normalized_query=normalized,
		intent=Intent(**intent_dict),
		entities=[Entity(**e) for e in entity_dicts],
		pipeline_latency_ms=elapsed_ms(start),
	)
	return JSONResponse(
		status_code=200,
		content=response.model_dump(),
		headers={"X-QU-Backend": _settings.model_backend},
	)


