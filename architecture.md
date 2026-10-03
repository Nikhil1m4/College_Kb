# Project Architecture and File Explanations

This document explains every piece of the `College_Kb` project. When building a modern web application, having a solid folder structure is just as important as the code itself. 

This project is a **Monorepo**, meaning both the Backend (Python) and the Frontend (Javascript) live happily in the same Git repository. This makes deployment and keeping the codebase in sync much easier.

---

## 1. Root Configuration Files
These files sit at the very base of your project and orchestrate how the whole repository functions, tests, and deploys.

*   **`vercel.json`** 
    *   **What it does:** The master blueprint for Vercel. 
    *   **Why it's here:** It tells Vercel that this project has two distinct services: a Python FastAPI backend and a Node.js Vite frontend. It handles the internet routing so that if a user visits `/api/...`, Vercel sends them to the backend, and if they visit anything else, it sends them to the frontend.

*   **`.python-version`**
    *   **What it does:** A tiny file containing exactly `3.12`.
    *   **Why it's here:** When Vercel (or other platforms) attempt to build your backend, this file strictly forces it to use Python 3.12, ensuring the environment matches your local machine.

*   **`pytest.ini`**
    *   **What it does:** Configuration for the Python testing framework (`pytest`).
    *   **Why it's here:** It tells `pytest` exactly where to look for tests (the `api/tests/` folder) and ensures your code can be imported correctly during testing.

*   **`ruff.toml`**
    *   **What it does:** Configuration for the Python linter (`ruff`).
    *   **Why it's here:** A linter acts like an automated spell-checker for code. This file tells `ruff` that lines of code shouldn't exceed 100 characters and enforces basic formatting rules (Errors, Fatal errors, and Import sorting).

*   **`requirements.txt`**
    *   **What it does:** The list of dependencies required to run your backend in *production*.
    *   **Why it's here:** When Vercel builds your backend, it reads this file to install `fastapi`, `uvicorn`, and other essential libraries. 

*   **`requirements-dev.txt`**
    *   **What it does:** The list of dependencies required *only* for local development.
    *   **Why it's here:** It contains tools like `pytest` and `ruff`. We separate these from `requirements.txt` because Vercel doesn't need testing tools installed on the production server.

*   **`.gitignore`**
    *   **What it does:** A list of files and folders that Git should ignore.
    *   **Why it's here:** It prevents you from accidentally uploading massive folders (like `node_modules` or `.venv`) or sensitive secrets (like `.env`) to GitHub.

*   **`.env.example`**
    *   **What it does:** A blank template for environment variables.
    *   **Why it's here:** It safely shows other developers (or you on a new computer) what API keys and secrets the project needs to run locally, without actually exposing your real passwords.

*   **`README.md` & `DECISIONS.md`**
    *   **What they do:** Human-readable documentation files.
    *   **Why they are here:** `README.md` is the front page of your GitHub repository containing setup instructions. `DECISIONS.md` is a logbook used to record architecture decisions and metrics for future reference.

---

## 2. Backend (`api/`)
This directory is exclusively for the Python FastAPI server. It acts as the brain of the application.

*   **`api/index.py`**
    *   **What it does:** The main entry point for the FastAPI application.
    *   **Why it's here:** When Vercel spins up your backend, this is the exact file it executes to start the server. It handles the API endpoints like `/api/health`.

*   **`api/core/`**
    *   **What it does:** This folder holds the core business logic.
    *   **Why it's here:** As the app grows, you shouldn't cram all your code into `index.py`. You will place database connections, AI logic, and data processing models inside this folder.

*   **`api/tests/`**
    *   **What it does:** Holds your automated Python tests.
    *   **Why it's here:** Contains files like `test_health.py` to ensure your API functions work flawlessly before you deploy them.

*   **`api/__init__.py`**
    *   **What it does:** An empty file.
    *   **Why it's here:** It is a special Python marker that tells Python to treat the `api` folder as an official "package," allowing you to import code smoothly across different files.

---

## 3. Frontend (`frontend/`)
This directory is entirely dedicated to the Vite + React user interface.

*   **`frontend/package.json` & `package-lock.json`**
    *   **What they do:** The exact equivalent of `requirements.txt`, but for Javascript. 
    *   **Why they are here:** They list all the Javascript libraries (like React and Vite) your frontend needs to build and run. The `-lock` file ensures the exact same versions are installed everywhere.

*   **`frontend/vite.config.js`**
    *   **What it does:** Configuration for the Vite bundler.
    *   **Why it's here:** It tells Vite how to compile your React code. Crucially, it sets up a local "proxy" so that when your frontend fetches `/api/...` on your computer, it forwards the request to your local Python server on port 8000.

*   **`frontend/index.html`**
    *   **What it does:** The single HTML file for your entire application.
    *   **Why it's here:** Because this is a Single Page Application (SPA), the browser only loads this one HTML file. This file contains a `<div id="root"></div>` where React takes over and draws the entire interface.

*   **`frontend/src/`**
    *   **What it does:** The source code for your React application.
    *   **Why it's here:** 
        *   `main.jsx`: The starting point that mounts React into the `index.html`.
        *   `App.jsx`: The main layout component of your website where buttons, text, and structure are defined.
        *   `App.css` & `index.css`: The stylesheets that make the application look beautiful.

*   **`frontend/public/`**
    *   **What it does:** Holds static assets that don't need to be compiled.
    *   **Why it's here:** Files like `favicon.svg` (the icon in the browser tab) sit here and are served directly to the user untouched.
