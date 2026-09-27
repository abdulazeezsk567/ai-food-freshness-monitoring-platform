# AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## Description

The **AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform** is designed to use food image analysis, environmental cold-chain conditions, and storage telemetry to estimate food freshness, predict remaining shelf life, detect spoilage indicators, and generate intelligent storage recommendations across food supply chains.

---

## Milestone 3 Implementation Scope (COMPLETED)

Milestone 3 expands the platform with full **Predictive Shelf-Life Monitoring & Risk Assessment** capabilities:

- **Feature Engineering Layer (`backend/app/ml/shelf_life_features.py`)**:
  - **Category Baseline Shelf Life**: Preserves baseline shelf life per food category (e.g., Leafy Greens = 7 days, Meat/Poultry = 4 days, Bakery = 5 days, Dairy = 10 days, Fruits = 14 days, Root Vegetables = 30 days).
  - **Storage Duration & Age**: Calculates total elapsed time in storage from inventory batch purchase date.
  - **Environmental Stress Factors**: Quantifies temperature degradation factor ($Q_{10}$ kinetic model) and humidity loss factor relative to optimal storage profiles.
  - **Historical Visual Degradation Rate**: Computes degradation velocity ($\Delta \text{Score} / \Delta t$) across sequential visual image assessments.
- **Predictive Model Engine (`backend/app/ml/shelf_life_model.py` - Model `shelf-life-baseline-v1`)**:
  - **Remaining Shelf-Life Estimation**: Calculates expected remaining days until spoilage based on composite degradation rate.
  - **Estimated Expiry Date**: Computes projected expiry date ($T_{current} + \text{Remaining Days}$), explicitly labeled as an AI estimate.
  - **Risk Classification**: Classifies batches into 4 operational risk levels (`LOW RISK`, `MEDIUM RISK`, `HIGH RISK`, `CRITICAL`).
  - **Freshness Degradation Trend**: Tracks quality trajectory (`Improving`, `Stable`, `Declining`, `Insufficient Data` for $<2$ assessments).
  - **Storage Impact Analysis & Actionable Guidance**: Generates human-readable explanations of environmental impact (e.g. thermal acceleration, moisture loss) and customized storage recommendations (e.g. lower storage temp to 4°C, adjust RH to 85-90%).
- **Database Schema Extensions (`backend/app/models/`)**:
  - `StorageCondition`: Tracks temperature (°C), relative humidity (%), storage facility type (`REFRIGERATED`, `COLD_ROOM`, `FREEZER`, `AMBIENT`, `DISPLAY`), and direct sunlight exposure.
  - `ShelfLifePrediction`: Persists prediction records, remaining days, estimated expiry date, risk level, degradation trend, storage impact, guidance, input features, and model version.
- **REST API Routers (`backend/app/routers/`)**:
  - `POST /api/shelf-life/predict`: Predict remaining shelf life for an inventory batch.
  - `GET /api/shelf-life/inventory/{inventory_id}`: Retrieve latest shelf life forecast.
  - `GET /api/shelf-life/history/{inventory_id}`: Retrieve full prediction audit history.
  - `POST /api/storage-conditions`: Log environmental storage conditions.
  - `GET /api/storage-conditions/inventory/{inventory_id}`: List logged storage history.
- **Frontend Predictive Shelf-Life Inspector (`frontend/src/pages/ShelfLifePage.jsx`)**:
  - Remaining days gauge with color-coded risk indicators.
  - Estimated expiry date badge and degradation trend tracker.
  - Interactive Storage Condition Inspector for live "what-if" environmental scenarios (modifying temperature, humidity, storage type, and sunlight exposure).
  - Degradation trend graph and storage condition impact breakdown.
  - Integration with `InventoryPage` via "Shelf-Life Forecast" button and navigation `Sidebar`.

---

## Milestone 2 Implementation Scope (COMPLETED)

Milestone 2 expands the platform with full **Image Analysis & Visual Freshness Assessment** capabilities:

- **Food Image Upload & Validation**: Secure file dropzone supporting JPG, PNG, and WEBP formats up to 10MB.
- **Computer Vision Pipeline (`backend/app/ml/`)**: Preprocessing, color analysis (Browning Index), texture analysis (GLCM), spoilage indicator detection, and 5-category freshness classification.
- **Database Schema Extension**: `AnalysisResult` model storing visual analysis metrics.
- **Frontend Analysis & Inspection Workflows**: `/freshness-analysis` page, printable inspection reports, and batch freshness history.

---

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy ORM, Pydantic v2, PyJWT, bcrypt, Pillow, OpenCV, NumPy
- **Frontend**: React.js, JavaScript, Tailwind CSS, Lucide Icons, Vite
- **Database**: PostgreSQL (Primary) / SQLite (Development fallback)
- **ML & Computer Vision**: Pillow, OpenCV, NumPy, Scikit-learn, Custom Shelf-Life Predictive Engine (`shelf-life-baseline-v1`)
- **Authentication**: JWT (JSON Web Tokens), OAuth2 Password Bearer, bcrypt
- **Tools & Infrastructure**: Git, GitHub, Docker, Pytest, Uvicorn

---

## Features Implemented (Milestones 1, 2 & 3)

- **Authentication System**: User registration, JWT login, profile endpoint, and frontend logout.
- **Role-Based Authorization**: Granular route guards for 5 distinct roles (`CONSUMER`, `RETAIL_MANAGER`, `WAREHOUSE_OPERATOR`, `FOOD_QUALITY_INSPECTOR`, `ADMINISTRATOR`).
- **Inventory & Batch Tracking**: Manage food products, batch codes, quantities, purchase dates, and expiration dates.
- **Cold-Chain Environmental Telemetry**: Log and track storage temperature (°C), relative humidity (%), storage facility types, and sunlight exposure.
- **Visual Image Freshness Analysis**: Upload food images to compute 0-100 freshness score, 5-category classification, and spoilage probabilities.
- **Predictive Shelf-Life Forecasting**: Compute expected remaining days, estimated expiry date, degradation velocity, risk tier, and trend.
- **Interactive Storage Inspector**: Simulate environmental changes (temperature, humidity, sunlight) to visualize shelf-life impact in real-time.
- **Actionable Storage Guidance**: Data-driven recommendations to extend food shelf life and minimize waste.
- **Printable Inspection Reports**: Generate formal certificates with scores, metrics, timestamps, and model version.
- **OpenAPI Documentation**: Auto-generated interactive Swagger UI and ReDoc.

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
│   └── Dockerfile
│
├── backend/                   # FastAPI REST API backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry point & CORS & static uploads
│   │   ├── core/              # Config, Security (JWT/bcrypt), Permissions (RBAC)
│   │   ├── database/          # SQLAlchemy session setup
│   │   ├── ml/                # Computer Vision & ML Pipeline & Shelf Life Predictive Engine
│   │   │   ├── shelf_life_features.py   # Feature extraction & environmental factors
│   │   │   ├── shelf_life_model.py      # Baseline shelf-life formula & guidance
│   │   │   └── shelf_life_predictor.py  # Master predictor service
│   │   ├── models/            # SQLAlchemy database models (User, FoodItem, Inventory, AnalysisResult, StorageCondition, ShelfLifePrediction)
│   │   ├── schemas/           # Pydantic schemas (User, FoodItem, Inventory, Freshness, StorageCondition, ShelfLifePrediction)
│   │   ├── routers/           # Auth, Users, FoodItems, Inventory, Stats, Freshness, Storage, ShelfLife
│   │   └── services/          # Seed demo data service
│   ├── tests/                 # Pytest test suite (Auth, Users, FoodItems, Inventory, Freshness, Shelf Life)
│   ├── uploads/               # Uploaded food freshness images directory
│   ├── requirements.txt
│   └── Dockerfile
│
├── ml/                        # ML Training & Evaluation Infrastructure
│   ├── models/                # Saved model weights (`freshness_model.json`)
│   ├── training/              # Training & dataset generation scripts (`train_classifier.py`)
│   └── evaluation/            # Model performance report (`eval_report.md`)
│
├── datasets/                  # Dataset organization structure
├── docs/                      # Technical documentation
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
DATABASE_URL=postgresql://postgres:azeez%40123@localhost:5432/food_freshness_db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
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

## Testing

Run backend tests using pytest:

```bash
cd backend
pytest tests/ -v
```

Output:
```text
tests/test_auth.py PASSED
tests/test_freshness.py PASSED
tests/test_shelf_life.py PASSED (21 passed)
```

---

## API Documentation

FastAPI provides automatic interactive API documentation accessible when the backend is running:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Shelf Life & Storage Endpoints

```text
POST   /api/shelf-life/predict                           Predict remaining shelf life for inventory batch
GET    /api/shelf-life/inventory/{inventory_id}         Get latest shelf life prediction
GET    /api/shelf-life/history/{inventory_id}           Get shelf life prediction history
POST   /api/storage-conditions                            Log storage environmental conditions
GET    /api/storage-conditions/inventory/{inventory_id} Get storage conditions history
```

---

## Future Milestones & Roadmap

- **Milestone 4**: Automated Cold-Storage Sensor Telemetry Streams (IoT integration).
- **Milestone 5**: Storage Optimization & Smart Waste Reduction Recommendation Engine.
