# Query Understanding (QU) Microservice

A FastAPI service that converts raw user text into structured JSON (intent + entities).

## Run locally

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Optional for Phase 2+: python -m spacy download en_core_web_sm
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Health checks:
- GET http://localhost:8000/healthz
- GET http://localhost:8000/readyz

API (stable):
- POST http://localhost:8000/v1/parse

## Docker

```bash
docker build -t qu:local .
docker run -p 8000:8000 --rm qu:local
```

## Configuration (env)
- `QU_MODEL_BACKEND`: stub | zeroshot | finetuned (default: stub)
- `QU_SPACY_MODEL`: en_core_web_sm
- `QU_INTENTS`: comma-separated labels for Phases 1–2

## Phases
- Phase 1: Stub backend (this image)
- Phase 2: Zero-shot + spaCy NER
- Phase 3: Fine-tuned PyTorch multitask


---

## How to run locally next time:
Activate venv:
PowerShell: .\\.venv\\Scripts\\Activate.ps1
Start server:
.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Test:
Health: http://localhost:8000/healthz
Ready: http://localhost:8000/readyz
POST API: http://localhost:8000/v1/parse
Notes:
The app requires the spaCy model en_core_web_sm. If missing, install via:
.\\.venv\\Scripts\\python.exe -m spacy download en_core_web_sm
All tasks completed:
Created venv
Installed deps
Started Uvicorn dev server

Test the v1/Parse endpoint:

```
powershell -NoProfile -Command "(Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/v1/parse -ContentType 'application/json' -Body (@{ text = 'Can you find me a good pizza place in NYC?' } | ConvertTo-Json)).Content"

outputs:
{"raw_query":"Can you find me a good pizza place in NYC?","normalized_query":"can you find I a good pizza place in nyc","intent":{"name":"find_restaurant","confidence":0.95},"entities":[{"text":"pizza place","value":"pizza","type":"food_type","start_char":23,"end_char":34},{"text":"good","value":"good","type":"sort_by","start_char":18,"end_char":22},{"text":"NYC","value":"New York City","type":"location","start_char":38,"end_char":41},{"text":"NYC","value":"New York City","type":"location","start_char":38,"end_char":41}],"pipeline_latency_ms":9}
```