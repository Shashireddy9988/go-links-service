# 🔗 Go Links — Internal URL Shortcut Service

A modular, well-tested hybrid web application built with a **Python FastAPI Backend** and a **TypeScript React Frontend**.

Go Links enables team members to create intuitive shortcuts (e.g. `go/design-system`, `go/oncall`, `go/payroll`) that redirect instantly to internal or external web resources while tracking engagement analytics.

---

## 🏗️ Architecture & Stack

- **Backend**: **Python 3.12** + **FastAPI** + **Pydantic v2** + **Pytest**.
  - RESTful API (`/api/v1/links`).
  - HTTP 302 Redirection router (`/go/{alias}`).
  - Structured logging and correlation Request IDs (`X-Request-ID`).
  - Repository pattern (`BaseLinkRepository` interface and `InMemoryLinkRepository`).
- **Frontend**: **TypeScript** + **React 18** + **Vite**.
  - Modern glassmorphism UI dashboard.
  - Live search, filtering by tags, click statistics, modal form validation, and quick copy-to-clipboard.

---

## 📁 Repository Structure

```
go-links/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── schemas/            # Pydantic v2 validation models
│   │   ├── repositories/       # BaseLinkRepository & InMemoryLinkRepository
│   │   ├── services/           # LinkService domain business logic
│   │   ├── middleware/         # Request ID & logging middleware
│   │   ├── routers/            # Link REST API & Redirect routers
│   │   └── main.py             # FastAPI App entrypoint
│   ├── tests/                  # Pytest test suite (12 tests)
│   │   ├── test_schemas.py
│   │   ├── test_service.py
│   │   └── test_api.py
│   └── requirements.txt        # Python dependencies
├── client/                     # TypeScript React + Vite Frontend UI
│   ├── src/
│   │   ├── components/         # UI Header, LinkCard, StatsOverview, CreateModal
│   │   ├── services/           # API client wrapper
│   │   ├── App.tsx             # Main dashboard
│   ├── screenshots/                # Captured UI test screenshots
├── README.md
└── question.txt                # Prompt instructions
```

---

## 🛠️ How to Run

### 1. Python FastAPI Backend

```bash
cd backend

# Install Python requirements
pip install -r requirements.txt

# Run Pytest suite
python -m pytest

# Start FastAPI backend server (http://127.0.0.1:8000)
python -m uvicorn app.main:app --reload --port 8000
```

> **Interactive API Docs**: Once started, open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access Swagger / OpenAPI documentation.

### 2. TypeScript React Frontend UI

In a second terminal:

```bash
cd client

# Install frontend dependencies
npm install

# Start Vite dev server (http://localhost:5173)
npm run dev
```

---

## 🧪 Automated Testing Results

- **Python Backend**: All **12 Pytest tests passed** (`test_schemas.py`, `test_service.py`, `test_api.py`).
- **TypeScript Frontend**: `npm run type-check` passed with **0 errors**.

---

## 📡 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/go/{alias}` | Redirects to target URL (HTTP 302) & increments click counter |
| **GET** | `/api/v1/links` | Fetch all shortcuts (supports `search`, `tag`, `sortBy`) |
| **POST** | `/api/v1/links` | Create a new shortcut |
| **GET** | `/api/v1/links/{id}` | Fetch single shortcut by ID |
| **GET** | `/api/v1/links/alias/{alias}` | Fetch shortcut details by alias |
| **PUT** | `/api/v1/links/{id}` | Update shortcut details |
| **DELETE** | `/api/v1/links/{id}` | Delete a shortcut |
| **GET** | `/health` | Server health check endpoint |

---

## 📸 Test Screenshots

The project includes test screenshots in the [`screenshots/`](screenshots/) folder:

- [`1_initial_dashboard.png`](screenshots/1_initial_dashboard.png) — Initial Dashboard layout & statistics.
- [`2_empty_modal.png`](screenshots/2_empty_modal.png) — Shortcut Creation Modal dialog.
- [`3_filled_modal.png`](screenshots/3_filled_modal.png) — Filled shortcut form before submission.
- [`4_shortcut_created_dashboard.png`](screenshots/4_shortcut_created_dashboard.png) — Updated dashboard with the new shortcut.
- [`5_filtered_search_dashboard.png`](screenshots/5_filtered_search_dashboard.png) — Live search query filtering.

