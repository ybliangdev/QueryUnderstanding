import os
from dataclasses import dataclass


@dataclass
class Settings:
	service_name: str = os.getenv("QU_SERVICE_NAME", "QU Service")
	model_backend: str = os.getenv("QU_MODEL_BACKEND", "stub")
	spacy_model: str = os.getenv("QU_SPACY_MODEL", "en_core_web_sm")
	intents_csv: str = os.getenv(
		"QU_INTENTS",
		"find_restaurant,get_weather,schedule_reminder",
	)
	port: int = int(os.getenv("PORT", "8000"))
	enable_debug: bool = os.getenv("QU_DEBUG", "false").lower() == "true"


def get_settings() -> Settings:
	return Settings(
		service_name=os.getenv("QU_SERVICE_NAME", "QU Service"),
		model_backend=os.getenv("QU_MODEL_BACKEND", "stub"),
		spacy_model=os.getenv("QU_SPACY_MODEL", "en_core_web_sm"),
		intents_csv=os.getenv(
			"QU_INTENTS",
			"find_restaurant,get_weather,schedule_reminder",
		),
		port=int(os.getenv("PORT", "8000")),
		enable_debug=os.getenv("QU_DEBUG", "false").lower() == "true",
	)


