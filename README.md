# AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## Description

The **AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform** is designed to use food image analysis, environmental cold-chain conditions, and storage telemetry to estimate food freshness, predict remaining shelf life, detect spoilage indicators, and generate intelligent storage recommendations across food supply chains.

---

## Milestone 1 Implementation Scope

The current **Milestone 1** delivery establishes the foundational full-stack architecture, focusing on:

- **Project Initialization**: Structured full-stack workspace with properly decoupled frontend and backend.
- **System Architecture**: Production-ready architecture, REST APIs, and service layer stubs.
- **Database Setup**: PostgreSQL relational models (`users`, `food_items`, `inventory`, categories) with SQLite fallback for local development.
- **Authentication & Security**: User registration, login, bcrypt password hashing, and JWT access tokens.
- **Role-Based Access Control (RBAC)**: Backend permission enforcement for `CONSUMER`, `RETAIL_MANAGER`, `WAREHOUSE_OPERATOR`, `FOOD_QUALITY_INSPECTOR`, and `ADMINISTRATOR`.
- **Food Inventory Management**: Full inventory CRUD workflow, batch number tracking, expiry date management, and environmental telemetry (temperature, humidity, packaging type, storage duration).
- **Dataset Organization**: Structured raw and processed dataset directory foundation (`fruits`, `vegetables`, `food_freshness`, `food101`) and dataset specifications.
- **Frontend/Backend Foundation**: Responsive dark-mode dashboard UI built with React, Vite, and Tailwind CSS.

---

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy ORM, Pydantic v2, PyJWT, bcrypt
- **Frontend**: React.js, JavaScript, Tailwind CSS, Lucide Icons, Vite
- **Database**: PostgreSQL (Primary) / SQLite (Development fallback)
- **Authentication**: JWT (JSON Web Tokens), OAuth2 Password Bearer, bcrypt
- **Tools & Infrastructure**: Git, GitHub, Docker, Docker Compose, Pytest, Uvicorn

---

## Features Implemented (Milestone 1)

- **Authentication System**: User registration, JWT login, profile endpoint (`/api/auth/me`), and frontend logout.
- **Role-Based Authorization**: Granular route guards for 5 distinct roles.
- **Inventory & Batch Tracking**: Manage food products, batch codes, quantities, purchase dates, and expiration dates.
- **Cold-Chain Environmental Telemetry**: Track storage temperature (°C), relative humidity (%), packaging formats, and storage duration.
- **Calculated Freshness Badges**: Real-time calculated status badges (`Fresh`, `Good`, `Acceptable`, `Near Spoilage`, `Spoiled`).
- **Interactive Dashboard**: Stat cards, telemetry meters, recent activity logs, and 1-click quick demo login buttons.
- **Admin User Management**: User table, role modification, account status toggle, and deletion.
- **OpenAPI Documentation**: Auto-generated interactive Swagger UI and ReDoc.

---

## Project Structure

```text
ai-food-freshness-monitoring-platform/
│
├── frontend/                  # React + Vite + Tailwind CSS web dashboard
│   ├── src/
│   │   ├── components/        # Navbar, Sidebar, StatCard, StatusBadge, Modal, Toast
│   │   ├── pages/             # Landing, Login, Register, Dashboard, Inventory, AddItem, Batches, Users, Datasets, Profile, Settings
│   │   ├── context/           # AuthContext, NotificationContext
│   │   ├── services/          # API HTTP client
│   │   ├── utils/             # Constants, Roles, Status colors
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── backend/                   # FastAPI REST API backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry point & CORS
│   │   ├── core/              # Config, Security (JWT/bcrypt), Permissions (RBAC)
│   │   ├── database/          # SQLAlchemy session setup
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── routers/           # Auth, Users, FoodItems, Inventory, Stats
│   │   └── services/          # Seed demo data service
│   ├── tests/                 # Pytest test suite
│   ├── requirements.txt
│   └── Dockerfile
│
├── datasets/                  # Dataset organization structure
│   ├── raw/                   # Raw images (fruits, vegetables, food_freshness, food101)
│   ├── processed/             # Preprocessed data manifests
│   └── README.md
│
├── docs/                      # Technical documentation
│   ├── architecture.md
│   ├── database-schema.md
│   └── api-documentation.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Environment Variables

Copy `.env.example` to create your local `.env` configuration:

```bash
cp .env.example .env
```

Template contents in `.env.example`:

```env
DATABASE_URL=
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=
CORS_ORIGINS=
```

---

## Running the Project Locally

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The application will be accessible at:
- **Frontend App**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000`

### 3. Docker Compose Setup

```bash
docker compose up --build
```

---

## API Documentation

FastAPI provides automatic interactive API documentation accessible when the backend is running:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Future Milestones & Roadmap

- **Milestone 2**: Computer Vision Food Image Analysis (Fresh vs. Spoiled image classification models).
- **Milestone 3**: Predictive Shelf-Life Engine & Spoilage Forecast Models.
- **Milestone 4**: Automated Storage Telemetry Sensors (IoT integration).
- **Milestone 5**: Recommendation Engine & Supply Chain Analytics.

---
