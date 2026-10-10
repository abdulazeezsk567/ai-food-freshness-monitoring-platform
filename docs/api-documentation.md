# API Documentation - Food Freshness Monitoring Platform

The backend provides a comprehensive, RESTful JSON API implemented in FastAPI with OpenAPI 3.0 specification compliance. Interactive documentation is automatically served at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

---

## Authentication & Security

All protected endpoints require an HTTP Bearer JWT token in the request headers:
```text
Authorization: Bearer <your_jwt_access_token>
```
Endpoints enforce role-based access control (RBAC) across five roles:
- `CONSUMER`
- `RETAIL_MANAGER`
- `WAREHOUSE_OPERATOR`
- `FOOD_QUALITY_INSPECTOR`
- `ADMINISTRATOR`

---

## Endpoint Reference

### 1. System Health & Overview

#### `GET /`
- **Description**: Returns system status, environment, and API version.
- **Access**: Public.
- **Response** (200 OK):
  ```json
  {
    "status": "online",
    "app": "Food Freshness Monitoring Platform",
    "environment": "development",
    "version": "4.0.0"
  }
  ```

#### `GET /health`
- **Description**: Docker and orchestrator health check probe.
- **Access**: Public.
- **Response** (200 OK):
  ```json
  {
    "status": "healthy",
    "app": "Food Freshness Monitoring Platform",
    "environment": "development",
    "version": "4.0.0"
  }
  ```

---

### 2. Authentication Router (`/api/auth`)

#### `POST /api/auth/register`
- **Description**: Registers a new user account.
- **Access**: Public.

#### `POST /api/auth/login`
- **Description**: Authenticates user and returns JWT bearer token. Accepts JSON or URL-encoded form data.
- **Access**: Public.

#### `GET /api/auth/me`
- **Description**: Returns profile information for the authenticated token.
- **Access**: Any authenticated user.

---

### 3. User Management Router (`/api/users`)

- `GET /api/users` — List platform users (`ADMINISTRATOR` or `FOOD_QUALITY_INSPECTOR`).
- `GET /api/users/{id}` — Get single user profile.
- `PUT /api/users/{id}` — Update user name, role, or active status.
- `DELETE /api/users/{id}` — Deactivate or remove user (`ADMINISTRATOR` only).

---

### 4. Food Items Router (`/api/food-items`)

- `POST /api/food-items` — Create new food item taxonomy entry.
- `GET /api/food-items` — List food items with optional query filter (`?search=...&category=...`).
- `GET /api/food-items/{id}` — Get details of a single food item.
- `PUT /api/food-items/{id}` — Update food item metadata.
- `DELETE /api/food-items/{id}` — Delete food item (`RETAIL_MANAGER`, `WAREHOUSE_OPERATOR`, `ADMINISTRATOR`).

---

### 5. Inventory Router (`/api/inventory`)

- `POST /api/inventory` — Create inventory batch record with storage parameters.
- `GET /api/inventory` — List inventory records with status computation (`Fresh`, `Expiring Soon`, `Expired`).
- `GET /api/inventory/{id}` — Get single inventory record by ID.
- `PUT /api/inventory/{id}` — Update batch details, quantities, or storage parameters.
- `DELETE /api/inventory/{id}` — Delete batch record.

---

### 6. Freshness Analysis Router (`/api/freshness`)

#### `POST /api/freshness/upload`
- **Description**: Upload a food inspection image (JPEG, PNG, WEBP, max 10MB).
- **Access**: Authenticated.
- **Response** (201 Created):
  ```json
  {
    "file_path": "uploads/freshness/a1b2c3d4_apple.jpg",
    "filename": "a1b2c3d4_apple.jpg",
    "size": 154320,
    "content_type": "image/jpeg"
  }
  ```

#### `POST /api/freshness/analyze`
- **Description**: Run OpenCV and heuristic CV extraction (color degradation, GLCM texture, Browning Index, spoilage indicators, 5-tier classification).
- **Access**: Authenticated.
- **Request Body**:
  ```json
  {
    "image_path": "uploads/freshness/a1b2c3d4_apple.jpg",
    "food_category": "Fruits",
    "inventory_id": 1,
    "notes": "Store inspection"
  }
  ```

#### `GET /api/freshness`
- **Description**: List historical visual freshness assessments.

#### `GET /api/freshness/{id}`
- **Description**: Retrieve complete inspection report for a specific assessment.

#### `GET /api/freshness/inventory/{inventory_id}/history`
- **Description**: Retrieve time-series inspection history for a specific inventory batch.

---

### 7. Storage Conditions & IoT Telemetry Router (`/api/storage-conditions`)

#### `POST /api/storage-conditions`
- **Description**: Log a single environmental storage observation for a batch.

#### `GET /api/storage-conditions/{inventory_id}`
- **Description**: Retrieve the most recent storage conditions logged for an inventory batch.

#### `POST /api/storage-conditions/batch-telemetry` (Alias: `/simulate-stream`)
- **Description**: Ingest a batch of simulated or real IoT telemetry readings with safe limits ($\le 50$ readings) and strict physical boundary validation (-30°C to 60°C, 0–100% RH).
- **Access**: Authenticated (`WAREHOUSE_OPERATOR`, `RETAIL_MANAGER`, `ADMINISTRATOR`).
- **Request Body**:
  ```json
  {
    "readings": [
      {
        "inventory_id": 1,
        "temperature": 4.2,
        "humidity": 87.0,
        "storage_location": "Cold Room A",
        "packaging_type": "Plastic Tray with Film",
        "storage_condition": "Refrigerated",
        "storage_duration_days": 2,
        "notes": "IoT Sensor Sensor-01"
      }
    ]
  }
  ```
- **Response** (201 Created): Returns count of ingested readings, inventory batch IDs updated, and any generated environmental threshold warnings.

---

### 8. Predictive Shelf-Life Router (`/api/shelf-life`)

#### `POST /api/shelf-life/predict`
- **Description**: Execute `shelf-life-baseline-v1` multi-factor shelf-life forecast. Supports interactive what-if simulation overrides.
- **Request Body**:
  ```json
  {
    "inventory_id": 1,
    "temperature_override": 4.0,
    "humidity_override": 85.0,
    "storage_condition_override": "Refrigerated",
    "packaging_type_override": "Vacuum Sealed"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "id": 1,
    "inventory_id": 1,
    "estimated_remaining_days": 12,
    "estimated_expiry_date": "2026-10-22",
    "risk_level": "LOW RISK",
    "confidence": 0.85,
    "trend": "Stable",
    "degradation_rate_per_day": 0.5,
    "has_image_analysis": true,
    "storage_impact": { ... },
    "contributing_factors": [ ... ],
    "storage_guidance": [ ... ],
    "model_version": "shelf-life-baseline-v1"
  }
  ```

#### `GET /api/shelf-life/{inventory_id}`
- **Description**: Get current active shelf-life prediction for an inventory batch.

#### `GET /api/shelf-life/{inventory_id}/history`
- **Description**: Get chronological prediction history for trend auditing.

---

### 9. Dashboard Statistics Router (`/api/stats`)

#### `GET /api/stats/dashboard`
- **Description**: Returns real-time aggregate platform metrics calculated directly from database records.
- **Response Payload**:
  - `total_food_items`: Master catalogue count
  - `active_batches`: Tracked inventory records
  - `expiring_soon`: Batches expiring within 3 days
  - `expired`: Expired batches
  - `facility_telemetry`: Real mean storage temperature (°C) and relative humidity (%) across all monitored batches
  - `shelf_life_analytics`: Risk breakdown (`CRITICAL`, `HIGH RISK`, `MEDIUM RISK`, `LOW RISK`), average remaining shelf-life days, total predictions
  - `freshness_analytics`: Average CV freshness score, total inspections, breakdown by freshness category
  - `spoilage_alerts`: Priority alert list with batch numbers, risk levels, and trigger reasons

---

### 10. Reporting & Export Router (`/api/reports`)

#### `GET /api/reports/inventory/csv`
- **Description**: Stream full inventory catalogue in RFC-4180 compliant CSV format.
- **Response**: `text/csv; charset=utf-8` file attachment (`inventory_report_<timestamp>.csv`).

#### `GET /api/reports/freshness/{analysis_id}/json`
- **Description**: Download complete computer vision inspection certificate in JSON format.
- **Response**: `application/json` file attachment (`freshness_certificate_<id>.json`).

#### `GET /api/reports/shelf-life/{prediction_id}/json`
- **Description**: Download formal shelf-life forecast audit certificate with feature snapshots and impact breakdowns.
- **Response**: `application/json` file attachment (`shelflife_forecast_<id>.json`).
