# AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## Description

The **AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform** uses visual food image analysis, environmental storage conditions, packaging formats, and quality degradation velocity to estimate food freshness, predict remaining shelf life, detect visual spoilage indicators, and generate storage recommendations across supply chains.

---

## Milestone 3 Implementation & Hardening Scope (COMPLETED)

Milestone 3 delivers **Predictive Shelf-Life Monitoring & Risk Assessment** powered by a deterministic, multi-factor baseline model (`shelf-life-baseline-v1`):

### 1. Deterministic Predictive Baseline Model (`shelf-life-baseline-v1`)
The remaining shelf-life calculation follows a transparent, deterministic multi-factor formula:

$$\text{Remaining Shelf Life} = \max\left(0, \left(\text{Base Days} \times \text{Freshness Factor} \times \text{Spoilage Factor} \times \text{Temp Factor} \times \text{Humidity Factor} \times \text{Packaging Factor} \times \text{Condition Factor} \times \text{Trend Factor}\right) - \text{Food Age}\right)$$

> **Transparency Note**: `shelf-life-baseline-v1` is a heuristic baseline model designed for operational forecasting. It is **not** a trained statistical ML model, nor a certified food safety guarantee.

### 2. Multi-Factor Impact Breakdown
- **Category Baseline Days**: Food item category baselines (Fruits: 14d, Vegetables: 10d, Dairy: 7d, Meat & Poultry: 5d, Seafood: 3d, Bakery: 4d, Beverages: 30d, Pantry: 90d).
- **Freshness & Spoilage Factors**: Derived from visual computer vision analysis if available (`has_image_analysis: true`), or defaults to baseline starting freshness (`has_image_analysis: false`).
- **Temperature & Humidity Factors**: Quantifies environmental deviation from optimal temperature (°C) and relative humidity (%).
- **Packaging Format Factor**: Multipliers for Vacuum Sealed (1.25x), Aseptic (1.15x), MAP (1.10x), Standard/Plastic (1.0x), Paper (0.85x), and Loose (0.70x).
- **Storage Condition Factor**: Multipliers for Frozen (1.8x), Refrigerated (1.0x), Room Temperature penalty for perishables (0.40x), Controlled Storage (1.15x).
- **Timestamp-Based Degradation Velocity**: Calculates exact score change over elapsed days ($\Delta \text{Score} / \Delta t$) across historical visual assessments (`Declining`, `Stable`, `Improving`, `Insufficient Data`).
- **Transparent Heuristic Confidence Score**: Calculated based on data completeness (image analysis +0.30, storage log +0.20, historical trend +0.15, specialized packaging +0.05).

### 3. Backend Input Validation & Safety Guarantees
- Strict Pydantic v2 validation for inputs:
  - `freshness_score`: Range 0–100
  - `spoilage_probability`: Range 0.0–1.0
  - `humidity`: Range 0.0%–100.0%
  - `temperature`: Range -30.0°C to 60.0°C
  - `storage_duration_days`: $\ge 0$
  - `storage_condition`: Allowed set (`Refrigerated`, `Frozen`, `Room Temperature`, `Controlled Storage`, `Unknown`)
  - `packaging_type`: Allowed set (`Standard Packaging`, `Vacuum Sealed`, `Aseptic Packaging`, `Modified Atmosphere Packaging (MAP)`, `Plastic Tray with Film`, `Paper Wrapping`, `Unpackaged / Loose`)
- **Guaranteed Consistency**: Remaining days $\ge 0$, estimated expiry date strictly equals $\text{today} + \text{remaining\_days}$, no contradictory risk states.

---

## Milestone 2 Implementation Scope (COMPLETED)

Milestone 2 expands the platform with **Image Analysis & Visual Freshness Assessment** capabilities:
- **Food Image Upload & Validation**: Dropzone for JPG, PNG, and WEBP formats up to 10MB.
- **Computer Vision Pipeline (`backend/app/ml/`)**: Preprocessing, color analysis (Browning Index), texture analysis (GLCM), spoilage indicator detection, and 5-category freshness classification.
- **Frontend Inspection Workflows**: `/freshness-analysis` page, printable inspection reports, and batch freshness history.

---

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy ORM, Pydantic v2, PyJWT, bcrypt, Pillow, OpenCV, NumPy
- **Frontend**: React.js, JavaScript, Tailwind CSS, Lucide Icons, Vite
- **Database**: PostgreSQL (Primary) / SQLite (Development fallback)
- **ML & Predictive Engine**: Custom Baseline Engine (`shelf-life-baseline-v1`), OpenCV, NumPy, Scikit-learn
- **Authentication**: JWT (JSON Web Tokens), OAuth2 Password Bearer, bcrypt
- **Tools & Infrastructure**: Git, GitHub, Docker, Pytest, Uvicorn

---

## Features Implemented (Milestones 1, 2 & 3)

- **Authentication System**: User registration, JWT login, profile endpoint, and frontend logout.
- **Role-Based Authorization**: Granular route guards for 5 distinct roles (`CONSUMER`, `RETAIL_MANAGER`, `WAREHOUSE_OPERATOR`, `FOOD_QUALITY_INSPECTOR`, `ADMINISTRATOR`).
- **Inventory & Batch Tracking**: Manage food products, batch codes, quantities, purchase dates, and expiration dates.
- **Cold-Chain Telemetry Logging**: Track storage temperature (°C), relative humidity (%), storage facility types, and packaging formats.
- **Visual Image Freshness Analysis**: Upload food images to compute 0-100 freshness score, 5-category classification, and spoilage probabilities.
- **Predictive Shelf-Life Forecasting**: Compute remaining days, estimated expiry date, degradation velocity, risk tier, and trend.
- **Interactive Storage What-If Simulator**: Tweak storage temperature, humidity, storage environment, or packaging to dynamically recalculate shelf-life.
- **Actionable Storage Guidance**: Data-driven recommendations to extend food shelf life and minimize waste.
- **Printable Inspection Reports**: Generate formal certificates with scores, metrics, timestamps, and model version.

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
│   │   │   ├── shelf_life_features.py   # Feature extraction & timestamp degradation rate
│   │   │   ├── shelf_life_model.py      # Deterministic shelf-life model (shelf-life-baseline-v1)
│   │   │   └── shelf_life_predictor.py  # Master predictor orchestrator
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
- **Backend API Docs**: `http://localhost:8000/docs`

---

## Backend Test Suite

Run all backend tests:

```bash
cd backend
python -m pytest tests/ -v
```

Output:
```text
31 passed in 5.05s
```

---

## Model & Safety Disclaimers

- **Baseline Model**: `shelf-life-baseline-v1` is a transparent heuristic baseline formula.
- **Safety Exclaust**: Predictions are operational guidelines and do **not** replace certified food safety regulations or laboratory shelf-life testing.
