from typing import List
from pydantic import BaseModel, Field


class Intent(BaseModel):
	name: str = Field(..., description="Predicted intent label")
	confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in prediction")


class Entity(BaseModel):
	text: str
	value: str
	type: str
	start_char: int
	end_char: int


class ParseResponse(BaseModel):
	raw_query: str
	normalized_query: str
	intent: Intent
	entities: List[Entity]
	pipeline_latency_ms: int


