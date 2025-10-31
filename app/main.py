from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.logging import get_json_logger
from app.api.v1 import router as v1_router


settings = get_settings()
logger = get_json_logger("qu")


app = FastAPI(title="Query Understanding Service", version="0.1.0")

# CORS defaults open for now; can be restricted via env later
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict:
	return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict:
	# Phase 1: simple readiness; later tie to model/spaCy load states
	return {"ready": True, "backend": settings.model_backend}


app.include_router(v1_router, prefix="/v1")


