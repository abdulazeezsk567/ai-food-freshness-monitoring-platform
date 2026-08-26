# Food Freshness Monitoring Platform - System Architecture

This document describes the high-level architecture, module dependencies, role-based security layer, and database integrations for the Food Freshness Monitoring Platform (Milestone 1).

## 1. System Overview

The Food Freshness Monitoring Platform is a full-stack web platform built for tracking food inventory, storage environmental parameters, batch metadata, and freshness status across consumers, retail managers, warehouse operators, food quality inspectors, and system administrators.

```text
+-----------------------------------------------------------------------+
|                             REACT FRONTEND                            |
|  (Vite + Tailwind CSS + Lucide Icons + Axios / Fetch + Auth Context) |
+-----------------------------------------------------------------------+
                                   |
                                   | REST API (JSON / HTTP Bearer JWT)
                                   v
+-----------------------------------------------------------------------+
|                            FASTAPI BACKEND                            |
|                                                                       |
|  +---------------------+  +---------------------+  +---------------+  |
|  |     Auth Router     |  |    Users Router     |  | Food Router   |  |
|  | (/api/auth/login...) |  |   (/api/users...)   |  | (/api/food...) |  |
|  +---------------------+  +---------------------+  +---------------+  |
|                                                                       |
|  +---------------------+  +---------------------+  +---------------+  |
|  |  Inventory Router   |  |    Stats Router     |  | AI Stubs Svc  |  |
|  |  (/api/inventory..) |  |   (/api/stats...)   |  | (Future M2/3) |  |
|  +---------------------+  +---------------------+  +---------------+  |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  |          Security Layer (Passlib / bcrypt + PyJWT RBAC)        |  |
|  +-----------------------------------------------------------------+  |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  |                   SQLAlchemy ORM Data Engine                    |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
                                   |
                 +-----------------+-----------------+
                 |                                   |
                 v                                   v
    +-------------------------+         +-------------------------+
    |       POSTGRESQL        |         |     SQLITE FALLBACK     |
    | (Docker / Prod Database)|         |  (Local Dev & Testing)  |
    +-------------------------+         +-------------------------+
```

---

## 2. Security & Role-Based Access Control (RBAC)

The system defines 5 roles with distinct privilege boundaries:

| Role | Scope | Key Capabilities |
| :--- | :--- | :--- |
| **CONSUMER** | Individual User | View personal dashboard, add/view personal food items & inventory. |
| **RETAIL_MANAGER** | Retail Store | Manage store inventory & batches, view expiry alerts, track freshness stats. |
| **WAREHOUSE_OPERATOR** | Warehouse Facility | Monitor storage environmental metrics (temp, humidity), manage bulk batch inventory. |
| **FOOD_QUALITY_INSPECTOR** | Quality Compliance | Audit food item quality ratings, inspect spoilage reports, approve batch status. |
| **ADMINISTRATOR** | System Wide | Full platform access, manage users, modify system configuration, view platform analytics. |

Security enforcement is performed at the FastAPI route level using custom dependency injection (`require_roles([...])`), parsing JWT payload signatures on every protected endpoint.

---

## 3. Future AI Pipeline Integration Design

Milestone 1 defines clean service interfaces to seamlessly integrate computer vision and predictive models in upcoming milestones:

```text
[Food Image Upload] ──> [Food Image Analysis Engine (M2)] ──> [Freshness Assessment Engine (M2)]
                                                                          │
[Storage Temp & Humidity] ────────────────────────────────────────────────┤
                                                                          ▼
                                                         [Shelf-Life Prediction Model (M3)]
                                                                          │
                                                                          ▼
                                                         [Recommendation & Alerts Engine]
                                                                          │
                                                                          ▼
                                                         [Dashboard Telemetry Cards & APIs]
```

---
