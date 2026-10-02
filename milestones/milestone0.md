# Milestone 0 — Completion Report

## ✅ Verification Results

### 1. `pytest` — PASSED

```
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-8.3.5, pluggy-1.6.0
configfile: pyproject.toml
testpaths: api/tests
collected 1 item

api/tests/test_health.py::test_health_status_ok PASSED   [100%]

============================== 1 passed in 0.70s ==============================
```

### 2. `ruff check api` — PASSED

```
All checks passed!
```

### 3. `npm run build` — PASSED

```
vite v8.3.1 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.57 kB │ gzip:  0.35 kB
dist/assets/index-CVODXPWq.css    1.03 kB │ gzip:  0.51 kB
dist/assets/index-Cmr9SYm3.js   221.36 kB │ gzip: 69.31 kB
✓ built in 740ms
```

### 4. `npm run lint` (oxlint) — PASSED

```
Found 0 warnings and 0 errors.
Finished in 165ms on 3 files with 104 rules using 8 threads.
```

### 5. Local servers verified

- uvicorn started on port 8000
- Vite dev server on port 5173 with `/api` proxy to 8000
- `GET http://localhost:8000/api/health` → `{"status": "ok", "env": "dev"}` ✅

---

## 📁 File Layout

```
College_Kb/
├── .env.example          APP_ENV=dev
├── .gitignore            covers .env, node_modules, __pycache__, .venv
├── .github/
│   └── workflows/
│       └── ci.yml        Python lint+test + Frontend build jobs
├── DECISIONS.md          blank sections for post-deploy notes
├── README.md             local dev instructions
├── milestones/
│   └── milestone0.md     this report
├── pyproject.toml        pytest pythonpath, ruff config, Vercel entrypoint
├── requirements.txt      fastapi, uvicorn, pydantic-settings, httpx, pypdf
├── requirements-dev.txt  pytest, ruff, httpx, anyio[trio]
├── vercel.json           buildCommand, outputDirectory, function config
├── api/
│   ├── __init__.py
│   ├── index.py          GET /api/health + GET /api/stream-test
│   ├── core/
│   │   ├── __init__.py
│   │   └── settings.py   pydantic-settings + lru_cache
│   └── tests/
│       ├── __init__.py
│       └── test_health.py
└── frontend/             Vite react (Plain JS)
    ├── index.html
    ├── package.json
    ├── vite.config.js    proxy /api → 8000
    └── src/
        ├── main.jsx
        ├── index.css
        ├── App.jsx       health fetch + streaming button
        └── App.css
```

---

## 🚀 Manual Vercel Deployment Checklist

Follow exactly in order:

1. **Push to GitHub**
   - Create a new GitHub repo (e.g. `college-kb`)
   - Push the `College_Kb/` directory as the repo root:
     ```bash
     cd d:\projects\rgsaas\College_Kb
     git remote add origin https://github.com/YOUR_USER/college-kb.git
     git push -u origin main
     ```

2. **Import project on Vercel**
   - Go to https://vercel.com/new
   - Click **"Import Git Repository"** → select `college-kb`
   - Vercel auto-detects FastAPI (Python runtime)

3. **Root Directory setting**
   - Leave **Root Directory** as `.` (repo root) — do NOT set it to `frontend/` or `api/`
   - The `vercel.json` at repo root controls everything

4. **Build & Output settings** (should be auto-filled from `vercel.json`)
   - **Build Command**: `cd frontend && npm ci && npm run build`
   - **Output Directory**: `public`
   - **Framework Preset**: `Other` (or FastAPI if Vercel detects it)

5. **Environment Variables**
   - Add: `APP_ENV` = `production`

6. **Deploy**
   - Click **Deploy** — Vercel builds the frontend and bundles the FastAPI function
   - First deploy ~2–4 min for Python packages

7. **Verify on live URL**
   - Visit `https://YOUR-PROJECT.vercel.app` — health JSON should appear
   - Click **Test streaming** — 5 chunks should arrive ~1 sec apart

---

## ⚠️ Things I Was Unsure About / Notes

1. **Vercel doc followed**: [https://vercel.com/docs/frameworks/backend/fastapi](https://vercel.com/docs/frameworks/backend/fastapi) + [https://vercel.com/docs/functions/runtimes/python](https://vercel.com/docs/functions/runtimes/python) (both last updated Aug 2026).

2. **`pyproject.toml` entrypoint**: The doc says Vercel looks for `app` in `api/index.py` automatically (it's in the supported list). I also added `[tool.vercel] entrypoint = "api.index:app"` as an explicit fallback. If Vercel auto-detects the `api/` path correctly, this is redundant but harmless.

3. **Frontend + API on same domain**: The docs recommend [Vercel Services](https://vercel.com/docs/services) for full-stack Python+frontend. However, Services is a newer Teams-tier feature. Instead I used the `public/` directory approach (frontend builds to `../public`, served as CDN static) + FastAPI function — same URL, no CORS, works on all Vercel tiers.

4. **Streaming on Vercel**: The docs confirm streaming is enabled by default for Python functions. The `/api/stream-test` endpoint uses `StreamingResponse` correctly. Whether Vercel's CDN layer buffers SSE chunks before delivery depends on plan/region — record in `DECISIONS.md`.

5. **`anyio[trio]` in requirements-dev**: Added as an optional dependency for the test client's async support; not strictly needed for sync tests but avoids `anyio` warnings in future async test additions.

6. **`public/` in `.gitignore`**: The built frontend artifacts (`public/`) are gitignored since Vercel rebuilds them at deploy time. This is correct behavior.
