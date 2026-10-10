# AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

---

## Description

The **AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform** is a full-stack platform designed for modern food supply chain operations, retail grocery management, warehouse cold chains, and consumers. The platform integrates computer vision inspection, environmental IoT storage telemetry, and deterministic predictive decay modeling to evaluate food quality, forecast remaining shelf life, detect spoilage defects, and provide actionable storage guidance.

---

## Milestone 4 Implementation Scope (COMPLETED)

Milestone 4 completes the platform with **Full-Stack Analytics, Automated Reporting, IoT Telemetry, and Production Deployment Hardening**:

### 1. Real Database-Driven Analytics Dashboard
- **No Mock Statistics**: All dashboard analytics are computed directly from live database records.
- **Facility Telemetry**: Real-time average facility temperature (°C) and relative humidity (%) computed across all active storage logs.
- **Shelf-Life Risk Breakdown**: Aggregated batch counts categorized by risk levels (`CRITICAL`, `HIGH RISK`, `MEDIUM RISK`, `LOW RISK`), alongside average remaining days.
- **Computer Vision Freshness Metrics**: Overall average freshness score (0–100) and grade distribution across all inspections.
- **Active Spoilage & Telemetry Alerts Feed**: Live feed highlighting batches with high spoilage risk or out-of-range storage conditions.

### 2. Comprehensive Reporting & Certificate Export Engine
- **Inventory CSV Export (`GET /api/reports/inventory/csv`)**: RFC-4180 streaming export of the entire inventory catalogue.
- **Freshness Inspection Certificate (`GET /api/reports/freshness/{id}/json`)**: Downloadable JSON certificate including CV color indices, GLCM texture metrics, detected defects, and model version.
- **Shelf-Life Forecast Certificate (`GET /api/reports/shelf-life/{id}/json`)**: Downloadable JSON audit certificate capturing the predictive feature snapshot, degradation velocity, and storage recommendations.

### 3. High-Throughput IoT Batch Telemetry Ingestion
- **Batch Endpoint (`POST /api/storage-conditions/batch-telemetry` & alias `/simulate-stream`)**: Ingests bulk readings from IoT sensor arrays.
- **Safe Payload Caps & Validation**: Limits ingestion to $\le 50$ readings per batch, validating realistic environmental boundaries (-30°C to 60°C, 0–100% RH) and returning threshold alerts.

### 4. Containerization & Production Deployment
- **Multi-Stage Frontend Dockerfile**: Builds static assets with Node.js and serves via an optimized Nginx Alpine image.
- **Reverse Proxy**: Nginx routes `/api/` and `/uploads/` directly to the backend service.
- **Persistent Media Volume**: Dedicated `uploads_data` volume prevents loss of uploaded inspection images during container lifecycles.
- **Automated Health Probes**: Backend `/health` probe integrated into Docker health checks.
- **Flexible Configuration**: Pydantic v2 `SettingsConfigDict` resolving environment variables across `.env` and `../.env`.

---

## Milestone 3 Implementation Scope (COMPLETED)

Milestone 3 delivers **Predictive Shelf-Life Monitoring & Risk Assessment** powered by a deterministic, multi-factor baseline model (`shelf-life-baseline-v1`):

### 1. Deterministic Predictive Baseline Model (`shelf-life-baseline-v1`)
The remaining shelf-life calculation follows a transparent, multi-factor formula:

$$\text{Remaining Shelf Life} = \max\left(0, \left(\text{Base Days} \times \text{Freshness Factor} \times \text{Spoilage Factor} \times \text{Temp Factor} \times \text{Humidity Factor} \times \text{Packaging Factor} \times \text{Condition Factor} \times \text{Trend Factor}\right) - \text{Food Age}\right)$$

> **Transparency Note**: `shelf-life-baseline-v1` is a heuristic baseline model designed for operational forecasting. It is **not** a trained statistical ML model, nor a certified food safety guarantee.

### 2. Multi-Factor Impact Breakdown
- **Category Baseline Days**: Food item category baselines (Fruits: 14d, Vegetables: 10d, Dairy: 7d, Meat & Poultry: 5d, Seafood: 3d, Bakery: 4d, Beverages: 30d, Pantry: 90d).
- **Assisted vs. Baseline Mode**: Accurately tracks whether an assessment is assisted by visual computer vision (`has_image_analysis: true`) or derived strictly from inventory and storage telemetry (`has_image_analysis: false`).
- **Timestamp-Based Degradation Velocity**: Calculates exact score change over elapsed days ($\Delta \text{Score} / \Delta t$) across historical visual assessments (`Declining`, `Stable`, `Improving`, `Insufficient Data`).
- **Transparent Heuristic Confidence Score**: Calculated based on data completeness (image analysis +0.30, storage log +0.20, historical trend +0.15, specialized packaging +0.05).
- **Interactive Storage What-If Simulator**: Tweak storage temperature, humidity, storage environment, or packaging to dynamically recalculate shelf-life.

---

## Milestone 2 Implementation Scope (COMPLETED)

Milestone 2 provides **Image Analysis & Visual Freshness Assessment** capabilities:
- **Food Image Upload & Validation**: Dropzone for JPG, PNG, and WEBP formats up to 10MB.
- **Computer Vision Pipeline (`backend/app/ml/`)**: Preprocessing, color analysis (Browning Index), texture analysis (GLCM), spoilage indicator detection, and 5-category freshness classification.
- **Frontend Inspection Workflows**: `/freshness-analysis` page, printable inspection reports, and batch freshness history.

---

## Milestone 1 Implementation Scope (COMPLETED)

- **Authentication System**: User registration, JWT login, profile endpoint, and frontend logout.
- **Role-Based Authorization**: Granular route guards for 5 distinct roles (`CONSUMER`, `RETAIL_MANAGER`, `WAREHOUSE_OPERATOR`, `FOOD_QUALITY_INSPECTOR`, `ADMINISTRATOR`).
- **Inventory & Batch Tracking**: Manage food products, batch codes, quantities, purchase dates, and expiration dates.

---

## Technology Stack

- **Backend**: Python 3.11+, FastAPI 0.115+, SQLAlchemy 2.0 ORM, Pydantic v2, PyJWT, passlib/bcrypt, Pillow, OpenCV, NumPy
- **Frontend**: React 18, JavaScript, Tailwind CSS, Lucide Icons, Vite 5
- **Database**: PostgreSQL 15 (Primary) / SQLite (Development & Pytest)
- **ML & Predictive Engine**: Custom Baseline Engine (`shelf-life-baseline-v1`), OpenCV, NumPy, Scikit-learn
- **Reverse Proxy & Web Server**: Nginx Alpine
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest, HTTPX

---

## Project Structure

```text
ai-food-freshness-monitoring-platform/
│
├── frontend/                  # React + Vite + Tailwind CSS web dashboard
│   ├── src/
│   │   ├── components/        # Navbar, Sidebar, StatCard, StatusBadge, Modal, Toast
│   │   ├── pages/             # Landing, Login, Register, Dashboard, FreshnessAnalysis, ShelfLifePage, FreshnessReport, Inventory, AddItem, Batches, Users, Datasets, Profile, Settings
│   │   ├── context/           # AuthContext, NotificationContext
│   │   ├── services/          # API HTTP client
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf             # Production Nginx reverse-proxy configuration
│   └── Dockerfile             # Multi-stage production container build
│
├── backend/                   # FastAPI REST API backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry point & CORS & static uploads & health probe
│   │   ├── core/              # Config, Security (JWT/bcrypt), Permissions (RBAC)
│   │   ├── database/          # SQLAlchemy session setup
│   │   ├── ml/                # Computer Vision & ML Pipeline & Shelf Life Predictive Engine
│   │   │   ├── shelf_life_features.py   # Feature extraction & timestamp degradation rate
│   │   │   ├── shelf_life_model.py      # Deterministic shelf-life model (shelf-life-baseline-v1)
│   │   │   └── shelf_life_predictor.py  # Master predictor orchestrator
│   │   ├── models/            # SQLAlchemy database models (User, FoodItem, Inventory, AnalysisResult, StorageCondition, ShelfLifePrediction)
│   │   ├── schemas/           # Pydantic schemas (User, FoodItem, Inventory, Freshness, StorageCondition, ShelfLifePrediction, Reports, Stats)
│   │   ├── routers/           # Auth, Users, FoodItems, Inventory, Stats, Freshness, Storage, ShelfLife, Reports
│   │   └── services/          # Seed demo data service
│   ├── tests/                 # Complete Pytest test suite (38 automated test cases)
│   ├── uploads/               # Uploaded food freshness images directory
│   ├── requirements.txt
│   └── Dockerfile
│
├── ml/                        # ML Training & Evaluation Infrastructure
├── datasets/                  # Dataset organization structure
├── docs/                      # Technical documentation
│   ├── architecture.md        # Full architecture & component specifications
│   ├── api-documentation.md   # Complete REST API reference
│   └── database-schema.md     # Relational entity-relationship specifications
├── docker-compose.yml         # Multi-container orchestration (DB, Backend, Frontend)
├── .env.example
├── .gitignore
└── README.md
```

---

## Running the Platform

### Option A: Running via Docker Compose (Recommended for Production)

```bash
docker-compose up --build
```

Services will be accessible at:
- **Web Dashboard**: `http://localhost:5173`
- **Backend API Docs**: `http://localhost:8000/docs`
- **Backend Health Check**: `http://localhost:8000/health`

---

### Option B: Running Locally for Development

#### 1. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The application will be accessible at:
- **Frontend App**: `http://localhost:5173`
- **Backend API Docs**: `http://localhost:8000/docs`

---

## Automated Verification & Testing

Run all backend tests:

```bash
cd backend
python -m pytest tests/ -v
```

**Test Suite Results:**
```text
38 passed in ~19s
```

Run frontend production build verification:

```bash
cd frontend
npm run build
```

---

## Model & Safety Disclaimers

- **Baseline Model**: `shelf-life-baseline-v1` is a transparent heuristic baseline formula.
- **Safety Exclusion**: Predictions are operational guidelines and do **not** replace certified food safety regulations or laboratory microbiological shelf-life testing.
