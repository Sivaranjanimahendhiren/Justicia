# Justicia — Agentic RAG Legal Assistant

AI-powered legal assistant for Indian Real Estate Disputes under RERA Act.

## Stack
- Backend: FastAPI + Python 3.11
- RAG: ChromaDB + OpenAI text-embedding-3-large
- LLM: GPT-4o (Strategy-Gen)
- DB: PostgreSQL
- Frontend: React 18 + Tailwind CSS
- Agent: Plan–Execute–Verify loop with 6 MCP tools

---

## Quick Start

### 1. Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL running locally (or use Docker)
- OpenAI API key

### 2. Backend Setup

```bash
cd justicia/backend
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY

pip install -r requirements.txt

# Seed the knowledge base (run once)
python -m rag.seed

# Start the API
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd justicia/frontend
npm install
npm start
```

Frontend: http://localhost:3000

### 4. Docker (full stack)

```bash
cd justicia
cp backend/.env.example backend/.env
# Add OPENAI_API_KEY to backend/.env

docker-compose up --build
```

---

## Connections

### Frontend → Backend
- React proxies to `http://localhost:8000` via `package.json` proxy setting
- All API calls go to `POST /api/v1/chat`
- Set `REACT_APP_API_URL` env var to override

### Backend → Kore.ai
- Configure webhook in Kore.ai using `dialog/koreai_webhook_config.json`
- Each Service Node in the dialog flow calls the corresponding `/api/v1/tools/*` endpoint
- Use bearer token auth — set `JUSTICIA_API_KEY` in both `.env` and Kore.ai webhook config

### Backend → ChromaDB
- ChromaDB runs embedded (no separate server needed)
- Data persisted at `backend/chroma_db/`
- Run `python -m rag.seed` to populate from knowledge files

### Backend → PostgreSQL
- Set `DATABASE_URL` in `.env`
- Tables auto-created on startup via SQLAlchemy

---

## Test Sample Case

```bash
cd justicia
python -m backend.test_sample
```

Expected output includes:
- RERA Section 18, 19, 31 references
- Case law: Kolkata West v. Rudra, Sharma v. Prestige
- Conflict detection (payment date discrepancy)
- Missing document list
- Compensation calculation
- Legal strategy with action items

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | /api/v1/chat | Main agent endpoint |
| POST | /api/v1/tools/juris-sync | Fetch statutes |
| POST | /api/v1/tools/fact-conflict | Detect contradictions |
| POST | /api/v1/tools/gap-detector | Audit documents |
| POST | /api/v1/tools/precedent-ranker | Rank case law |
| POST | /api/v1/tools/ethical-guard | Validate strategy |
| POST | /api/v1/tools/strategy-gen | Generate strategy |
| GET | /health | API health |
| GET | /health/rag | RAG/ChromaDB health |

---

## Domain Guard

Queries not related to real estate / RERA return:
> "This system handles real estate disputes under RERA only."

Trigger keywords: builder, flat, possession, RERA, apartment, property, developer, allotment, delay, refund, compensation, construction, housing, real estate, plot, installment, payment, receipt, tower, project, bhk, registry, promoter
