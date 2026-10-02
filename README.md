# College Club Knowledge Base

RAG web app — **Milestone 0**: empty skeleton that builds, tests, and deploys.

---

## Local development

### Backend

```bash
# From repo root
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt -r requirements-dev.txt

# Run the API server
uvicorn api.index:app --reload --port 8000
```

API is now at <http://localhost:8000/api/health>

### Frontend

```bash
# In a separate terminal
cd frontend
npm install
npm run dev
```

Frontend is at <http://localhost:5173>.  
`/api/*` requests are proxied to the backend at port 8000.

---

## Running tests & linting

```bash
# From repo root (with venv active)
pytest
ruff check api
```

---

## Vercel deployment

See the Vercel checklist in `DECISIONS.md` and follow the steps in:
<https://vercel.com/docs/frameworks/backend/fastapi>

---

## Previews

<img width="903" height="637" alt="image" src="https://github.com/user-attachments/assets/575eaf33-cd75-49c1-a85d-8ce7f97e97ed" />
<img width="875" height="306" alt="image" src="https://github.com/user-attachments/assets/46782171-70d0-415e-9de3-e90cb86536e1" />
