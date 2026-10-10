# Food Freshness Monitoring Platform - System Architecture

This document describes the high-level architecture, module dependencies, data flow, computer vision pipeline, predictive shelf-life engine, role-based security layer, and containerized deployment for the **AI-Powered Food Freshness Detection and Predictive Shelf Life Monitoring Platform** (Milestones 1–4).

---

## 1. System Overview & Component Diagram

```text
+-----------------------------------------------------------------------------------------+
|                                    CLIENT APPLICATION                                   |
|                React 18 + Vite + Tailwind CSS + Lucide Icons + SPA Router                |
+-----------------------------------------------------------------------------------------+
                                             |
                                             | HTTP / JSON / Multipart (JWT Bearer Auth)
                                             v
+-----------------------------------------------------------------------------------------+
|                                  NGINX REVERSE PROXY                                    |
|         Port 80 / 5173 ──> /api/ ──> Backend:8000 | /uploads/ ──> Backend:8000          |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                    FASTAPI BACKEND                                      |
|                                                                                         |
|  +-------------------+  +-------------------+  +-------------------+  +---------------+ |
|  |    Auth Router    |  |   Users Router    |  | Food Items Router |  | Inventory Rtr | |
|  | (/api/auth)       |  | (/api/users)      |  | (/api/food-items) |  | (/api/invent.)| |
|  +-------------------+  +-------------------+  +-------------------+  +---------------+ |
|                                                                                         |
|  +-------------------+  +-------------------+  +-------------------+  +---------------+ |
|  |  Freshness Router |  | Storage / IoT Rtr |  |  Shelf-Life Rtr   |  | Reports Router| |
|  | (/api/freshness)  |  | (/api/storage)    |  | (/api/shelf-life) |  | (/api/reports)| |
|  +-------------------+  +-------------------+  +-------------------+  +---------------+ |
|                                                                                         |
|  +------------------------------------------------------------------------------------+ |
|  |                                Stats & Analytics Router                            | |
|  |  Real database aggregates, facility telemetry, CV distribution, spoilage alerts    | |
|  +------------------------------------------------------------------------------------+ |
|                                                                                         |
|  +------------------------------------------------------------------------------------+ |
|  |                                   AI & ML ENGINES                                  | |
|  |  [Computer Vision Pipeline]                     [Predictive Shelf-Life Engine]     | |
|  |  • Preprocessing & Blur Detection               • shelf-life-baseline-v1           | |
|  |  • Browning Index & HSV/LAB color               • Multi-factor decay formula       | |
|  |  • GLCM texture homogeneity                     • Timestamp degradation velocity   | |
|  |  • Spoilage indicator identification            • Transparent heuristic confidence | |
|  +------------------------------------------------------------------------------------+ |
|                                                                                         |
|  +------------------------------------------------------------------------------------+ |
|  |                    Security Layer (Passlib / bcrypt + PyJWT RBAC)                  | |
|  +------------------------------------------------------------------------------------+ |
|                                                                                         |
|  +------------------------------------------------------------------------------------+ |
|  |                             SQLAlchemy ORM Data Engine                             | |
|  +------------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------------+
                                             |
                      +----------------------+----------------------+
                      |                                             |
                      v                                             v
        +---------------------------+                 +---------------------------+
        |        POSTGRESQL         |                 |      SQLITE FALLBACK      |
        |  (Production / Docker)    |                 |   (Local Dev & Pytest)    |
        +---------------------------+                 +---------------------------+
                      |
                      v
        +---------------------------+
        |  DOCKER PERSISTENT VOLS   |
        |  • postgres_data          |
        |  • uploads_data           |
        +---------------------------+
```

---

## 2. Computer Vision Freshness Pipeline (Milestone 2)

The CV module (`backend/app/ml/`) extracts physical visual degradation metrics directly from uploaded food inspection images:

```text
[Input Image: JPG / PNG / WEBP]
        │
        ├──> [Preprocessing & Standardization] (Resizing, Laplacian blur verification)
        │
        ├──> [Color Analysis] ──> RGB to HSV & LAB color spaces
        │                        ├──> Browning Index (BI) calculation
        │                        └──> Surface discoloration ratio
        │
        ├──> [Texture Analysis] ──> Grayscale GLCM (Gray-Level Co-occurrence Matrix)
        │                          ├──> Homogeneity & contrast metrics
        │                          └──> Laplacian gradient variance
        │
        ├──> [Defect & Spoilage Indicators]
        │    ├── Color Degradation Detection
        │    ├── Surface Texture Irregularity
        │    ├── Mold Spot / Dark Patch Segmentation
        │    └── Bruising / Physical Soft Spot Estimation
        │
        └──> [Freshness Classification & Scoring]
             ├── 5-Category Classification (Fresh, Good, Acceptable, Near Spoilage, Spoiled)
             ├── Transparent 0–100 Freshness Score
             └── Spoilage Probability: P(Near Spoilage) + P(Spoiled)
```

---

## 3. Predictive Shelf-Life Engine: `shelf-life-baseline-v1` (Milestone 3)

The remaining shelf life is computed via a transparent, multi-factor deterministic baseline formula:

$$\text{Remaining Shelf Life} = \max\left(0, \left(\text{Base Days} \times F_{\text{fresh}} \times F_{\text{spoil}} \times F_{\text{temp}} \times F_{\text{humidity}} \times F_{\text{pkg}} \times F_{\text{cond}} \times F_{\text{trend}}\right) - \text{Age}\right)$$

### Key Components:
- **Baseline Days**: Food item category baselines (Fruits: 14d, Vegetables: 10d, Dairy: 7d, Meat & Poultry: 5d, Seafood: 3d, Bakery: 4d, Beverages: 30d, Pantry: 90d).
- **Assisted vs. Baseline Mode**: Accurately flags whether an assessment is assisted by visual computer vision (`has_image_analysis: true`) or derived strictly from inventory and storage telemetry (`has_image_analysis: false`).
- **Degradation Velocity ($\Delta \text{Score} / \Delta t$)**: Uses actual historical inspection timestamps to calculate score decay per elapsed day, returning trajectory states (`Declining`, `Stable`, `Improving`, or `Insufficient Data`).
- **Transparent Heuristic Confidence**: Statistically uncalibrated fixed values are strictly avoided; confidence is deterministically calculated from input feature completeness.
- **Interactive What-If Simulation**: Overrides temperature, humidity, storage environment, or packaging to simulate immediate shelf-life impact.

---

## 4. Platform Analytics & Reporting Service (Milestone 4)

- **Real Database Metrics**: Eliminates all mock/hardcoded statistics. The `/api/stats/dashboard` endpoint calculates live facility averages, risk distributions, and spoilage alerts directly from PostgreSQL/SQLite.
- **RFC-4180 CSV Streaming**: Enables complete inventory exports for warehouse management.
- **Downloadable Inspection & Forecast JSON Certificates**: Standalone portable records containing model versions, feature snapshots, timestamps, and compliance audit data.
- **Simulated IoT Stream Ingestion**: `/api/storage-conditions/batch-telemetry` supports bulk sensor logging with strict boundary verification and configurable safety thresholds.

---

## 5. Security & Role-Based Access Control (RBAC)

The system enforces 5 distinct roles with hierarchical and domain-specific permissions:

| Role | Scope | Key Capabilities |
| :--- | :--- | :--- |
| **CONSUMER** | Individual User | View personal dashboard, track domestic produce, run visual freshness analysis. |
| **RETAIL_MANAGER** | Retail Store | Manage store batches, export CSVs, run what-if shelf-life simulations, monitor expiry risk. |
| **WAREHOUSE_OPERATOR** | Warehouse Facility | Log cold-chain telemetry, ingest IoT sensor batch streams, monitor storage deviations. |
| **FOOD_QUALITY_INSPECTOR** | Quality Compliance | Audit freshness grades, download formal JSON inspection certificates, oversee spoilage alerts. |
| **ADMINISTRATOR** | System Wide | Full platform access, manage users and roles, inspect system health and global metrics. |

---

## 6. Deployment & Containerization Architecture

- **Multi-Stage Frontend**: Builds static assets via Node 18, serves via lightweight Nginx Alpine container.
- **Reverse Proxy**: Nginx routes `/api/` and `/uploads/` to the FastAPI backend with HTTP headers preserved.
- **Data Persistence**: Dedicated Docker volumes (`postgres_data`, `uploads_data`) guarantee that database records and uploaded food images survive container rebuilds.
- **Health Probes**: Automated Docker health checks ping `/health` to ensure robust orchestrator lifecycle management.
