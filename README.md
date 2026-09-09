# AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## Description

The **AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform** is designed to use food image analysis, environmental cold-chain conditions, and storage telemetry to estimate food freshness, predict remaining shelf life, detect spoilage indicators, and generate intelligent storage recommendations across food supply chains.

---

## Milestone 2 Implementation Scope (COMPLETED)

Milestone 2 expands the platform with full **Image Analysis & Visual Freshness Assessment** capabilities:

- **Food Image Upload & Validation**: Secure file dropzone supporting JPG, PNG, and WEBP formats up to 10MB, with size/format verification and filename sanitization.
- **Computer Vision Pipeline (`backend/app/ml/`)**:
  - **Preprocessing**: RGB conversion, standardization, resizing, and blur detection via Laplacian variance.
  - **Color Analysis**: RGB to HSV & LAB color space conversion, Browning Index (BI) calculation, and surface discoloration ratio estimation.
  - **Texture Analysis**: Grayscale local homogeneity, GLCM contrast, and Laplacian gradient variance.
  - **Spoilage Indicator Detection**: Multi-indicator analysis for Color Degradation, Surface Texture Changes, Mold Spot Detection, Bruising/Soft Spots, and Physical Damage.
  - **Freshness Classification**: Multi-class classification into 5 categories (`Fresh`, `Good`, `Acceptable`, `Near Spoilage`, `Spoiled`) with softmax probability distributions.
  - **Freshness Score**: Transparent 0–100 Freshness Score formula and Spoilage Probability ($P(\text{Near Spoilage}) + P(\text{Spoiled})$).
- **Database Schema Extension**: `AnalysisResult` SQLAlchemy model storing complete metric JSON payloads, visual indicators, model versions, and uploaded image paths.
- **ML Training Infrastructure (`ml/`)**: Synthetic feature dataset generator, training script (`train_classifier.py`), baseline classifier, and evaluation metrics report (`eval_report.md` - Test Accuracy: 97.33%).
- **Frontend Analysis & Inspection Workflows**:
  - Interactive `/freshness-analysis` page with live preview, score gauge, color/texture decomposition cards, and spoilage indicators audit.
  - Printable / downloadable formal Freshness Inspection Report.
  - Inventory Page integration with batch-linked Freshness History modal.

---

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy ORM, Pydantic v2, PyJWT, bcrypt, Pillow, OpenCV, NumPy
- **Frontend**: React.js, JavaScript, Tailwind CSS, Lucide Icons, Vite
- **Database**: PostgreSQL (Primary) / SQLite (Development fallback)
- **ML & Computer Vision**: Pillow, OpenCV, NumPy, Scikit-learn (Baseline nearest centroid & softmax classifier)
- **Authentication**: JWT (JSON Web Tokens), OAuth2 Password Bearer, bcrypt
- **Tools & Infrastructure**: Git, GitHub, Docker, Docker Compose, Pytest, Uvicorn

---

## Features Implemented (Milestones 1 & 2)

- **Authentication System**: User registration, JWT login, profile endpoint (`/api/auth/me`), and frontend logout.
- **Role-Based Authorization**: Granular route guards for 5 distinct roles (`CONSUMER`, `RETAIL_MANAGER`, `WAREHOUSE_OPERATOR`, `FOOD_QUALITY_INSPECTOR`, `ADMINISTRATOR`).
- **Inventory & Batch Tracking**: Manage food products, batch codes, quantities, purchase dates, and expiration dates.
- **Cold-Chain Environmental Telemetry**: Track storage temperature (°C), relative humidity (%), packaging formats, and storage duration.
- **Visual Image Freshness Analysis**: Upload food images to compute 0-100 freshness score, 5-category classification, and spoilage probabilities.
- **Color & Texture Decomposition**: Quantitative browning index, surface discoloration %, and local GLCM texture roughness scores.
- **Spoilage Indicators Audit**: Automated detection of color degradation, texture shriveling, mold spot clusters, bruising, and surface cuts.
- **Inventory Batch Linkage & History**: Attach visual freshness analysis results directly to physical inventory batches and view timeline history.
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
│   │   ├── pages/             # Landing, Login, Register, Dashboard, FreshnessAnalysis, FreshnessReport, Inventory, AddItem, Batches, Users, Datasets, Profile, Settings
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
│   │   ├── ml/                # Computer Vision & ML Pipeline Engine (Preprocessing, Color, Texture, Spoilage, Classifier, Scoring, Predictor)
│   │   ├── models/            # SQLAlchemy database models (User, FoodItem, Inventory, AnalysisResult)
│   │   ├── schemas/           # Pydantic schemas (User, FoodItem, Inventory, Freshness)
│   │   ├── routers/           # Auth, Users, FoodItems, Inventory, Stats, Freshness
│   │   └── services/          # Seed demo data service
│   ├── tests/                 # Pytest test suite (Auth, Users, FoodItems, Inventory, Freshness)
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

### Key Freshness Analysis Endpoints

```text
POST   /api/freshness/upload                             Upload image file
POST   /api/freshness/analyze                            Run complete image analysis pipeline
GET    /api/freshness/results                            List analysis history
GET    /api/freshness/results/{analysis_id}              Get detailed analysis result
DELETE /api/freshness/results/{analysis_id}              Delete analysis result
GET    /api/inventory/{inventory_id}/freshness-history  Get freshness history for inventory batch
```

---

## Future Milestones & Roadmap

- **Milestone 3**: Predictive Remaining Shelf-Life Engine & Spoilage Forecast Models.
- **Milestone 4**: Automated Cold-Storage Sensor Telemetry Streams (IoT integration).
- **Milestone 5**: Storage Optimization & Smart Waste Reduction Recommendation Engine.

---
