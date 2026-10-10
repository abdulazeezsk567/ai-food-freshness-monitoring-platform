# Database Schema - Food Freshness Monitoring Platform

This document details the relational schema design for PostgreSQL (and SQLite fallback).

## Entity Relationship Overview

```text
+-------------------+        1 : N        +-------------------+
|       users       | ------------------> |    food_items     |
|-------------------|                     |-------------------|
| id (PK)           |                     | id (PK)           |
| name              |                     | name              |
| email (Unique)    |                     | category          |
| password_hash     |                     | description       |
| role              |                     | created_by (FK)   |
| is_active         |                     | created_at        |
| created_at        |                     | updated_at        |
| updated_at        |                     +-------------------+
+-------------------+                               |
       |         |                                  | 1 : N
       |         |                                  v
       |         |                        +-------------------+
       |         | 1 : N                  |     inventory     |
       |         +----------------------> |-------------------|
       |                                  | id (PK)           |
       |                                  | food_item_id (FK) |
       |                                  | batch_number      |
       |                                  | quantity          |
       |                                  | unit              |
       |                                  | purchase_date     |
       |                                  | expiry_date       |
       |                                  | storage_temp      |
       |                                  | storage_humidity  |
       |                                  | packaging_type    |
       |                                  | storage_duration  |
       |                                  | created_at        |
       |                                  | updated_at        |
       |                                  +-------------------+
       |                                            |
       |            +-------------------------------+-------------------------------+
       |            | 1 : N                         | 1 : N                         | 1 : N
       v            v                               v                               v
+------------------------+             +------------------------+      +--------------------------+
|    analysis_results    |             |   storage_conditions   |      |  shelf_life_predictions  |
|------------------------|             |------------------------|      |--------------------------|
| id (PK)                |             | id (PK)                |      | id (PK)                  |
| user_id (FK)           |             | inventory_id (FK)      |      | inventory_id (FK)        |
| inventory_id (FK)      |             | user_id (FK)           |      | analysis_id (FK)         |
| image_path             |             | temperature            |      | user_id (FK)             |
| food_category          |             | humidity               |      | estimated_remaining_days |
| predicted_category     |             | storage_location       |      | estimated_expiry_date    |
| freshness_score        |             | packaging_type         |      | risk_level               |
| spoilage_probability   |             | storage_condition      |      | confidence               |
| confidence             |             | storage_duration_days  |      | trend                    |
| color_analysis (JSON)  |             | notes                  |      | storage_impact (JSON)    |
| texture_analysis(JSON) |             | created_at             |      | contributing_factors(JSON|
| spoilage_indicators(JSON             +------------------------+      | storage_guidance (JSON)  |
| model_version          |                                             | input_features (JSON)    |
| created_at             |                                             | model_version            |
+------------------------+                                             | created_at               |
            |                                                          +--------------------------+
            +--------------------------- 0..1 : N -----------------------------------+
```

---

## Table Specifications

### 1. `users`
Stores user profile credentials, assigned system role, and active status.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique user identifier |
| `name` | String(100) | Not Null | Full user name |
| `email` | String(255) | Not Null, Unique, Indexed | Login email address |
| `password_hash` | String(255) | Not Null | Bcrypt hashed password |
| `role` | String(50) | Not Null, Default 'CONSUMER' | Role (`CONSUMER`, `RETAIL_MANAGER`, `WAREHOUSE_OPERATOR`, `FOOD_QUALITY_INSPECTOR`, `ADMINISTRATOR`) |
| `is_active` | Boolean | Not Null, Default True | Account activation state |
| `created_at` | DateTime | Not Null | Record creation timestamp |
| `updated_at` | DateTime | Not Null | Record update timestamp |

---

### 2. `food_items`
Stores master food product definitions and product taxonomy.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique food item identifier |
| `name` | String(150) | Not Null, Indexed | Product name (e.g., Organic Gala Apple) |
| `category` | String(50) | Not Null, Indexed | Food Category (`Fruits`, `Vegetables`, `Dairy Products`, `Meat & Poultry`, `Seafood`, `Bakery Products`, `Packaged Foods`, `Beverages`) |
| `description` | Text | Nullable | Detailed product description |
| `created_by` | Integer | FK (`users.id`), Not Null | User ID of creator |
| `created_at` | DateTime | Not Null | Record creation timestamp |
| `updated_at` | DateTime | Not Null | Record update timestamp |

---

### 3. `inventory`
Stores physical batch telemetry, quantities, storage conditions, and expiration tracking.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique batch inventory identifier |
| `food_item_id` | Integer | FK (`food_items.id`), Not Null | Associated food item |
| `batch_number` | String(100) | Not Null, Indexed | Unique tracking batch code (e.g., BATCH-2026-0801) |
| `quantity` | Float | Not Null | Numerical quantity |
| `unit` | String(30) | Not Null | Unit of measurement (`kg`, `grams`, `liters`, `units`, `boxes`) |
| `purchase_date` | Date | Not Null | Date of reception / harvest |
| `expiry_date` | Date | Not Null, Indexed | Manufacturer or estimated expiry date |
| `storage_temperature` | Float | Not Null | Storage temperature reading in °C |
| `storage_humidity` | Float | Not Null | Relative humidity percentage (0.0%–100.0%) |
| `packaging_type` | String(100) | Not Null | Packaging format (e.g., Vacuum Sealed, Plastic Tray with Film) |
| `storage_duration` | Integer | Not Null | Elapsed storage duration in days |
| `created_at` | DateTime | Not Null | Record creation timestamp |
| `updated_at` | DateTime | Not Null | Record update timestamp |

---

### 4. `analysis_results`
Stores computer vision image analysis results, freshness grading, texture/color indicators, and spoilage probability.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique analysis record identifier |
| `user_id` | Integer | FK (`users.id`, CASCADE), Not Null | Inspector or user performing analysis |
| `inventory_id` | Integer | FK (`inventory.id`, SET NULL), Nullable | Linked inventory batch (optional) |
| `image_path` | String(500) | Not Null | Relative filesystem path to uploaded inspection image |
| `food_category` | String(50) | Not Null, Indexed | Selected food category |
| `predicted_category` | String(50) | Not Null, Indexed | Freshness Grade (`Fresh`, `Good`, `Acceptable`, `Near Spoilage`, `Spoiled`) |
| `freshness_score` | Integer | Not Null | Deterministic score (0–100) |
| `spoilage_probability` | Float | Not Null | Probability of spoilage (0.0–1.0) |
| `confidence` | Float | Not Null | Heuristic assessment confidence (0.0–1.0) |
| `color_analysis` | Text | Not Null | JSON payload with RGB, HSV, LAB, Browning Index, discoloration ratio |
| `texture_analysis` | Text | Not Null | JSON payload with GLCM contrast, homogeneity, Laplacian gradient variance |
| `spoilage_indicators` | Text | Not Null | JSON payload with detected defects (mold, bruising, discoloration, texture defect) |
| `model_version` | String(50) | Not Null, Default 'v1.0.0-CV' | CV pipeline model version |
| `created_at` | DateTime | Not Null | Assessment timestamp |

---

### 5. `storage_conditions`
Stores time-series environmental logs, warehouse telemetry, and cold-chain monitoring events.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique storage telemetry record identifier |
| `inventory_id` | Integer | FK (`inventory.id`, CASCADE), Not Null | Associated inventory batch |
| `user_id` | Integer | FK (`users.id`, CASCADE), Not Null | Operator or IoT client logging condition |
| `temperature` | Float | Not Null, Default 4.0 | Storage temperature in °C |
| `humidity` | Float | Not Null, Default 85.0 | Relative humidity percentage (0.0%–100.0%) |
| `storage_location` | String(100) | Not Null | Warehouse facility or cold room zone |
| `packaging_type` | String(100) | Not Null | Active packaging format |
| `storage_condition` | String(50) | Not Null | Environment (`Refrigerated`, `Frozen`, `Room Temperature`, `Controlled Storage`) |
| `storage_duration_days` | Integer | Not Null, Default 1 | Accumulated storage duration in days |
| `notes` | Text | Nullable | Sensor calibration notes or operator comments |
| `created_at` | DateTime | Not Null | Timestamp of telemetry reading |

---

### 6. `shelf_life_predictions`
Stores predictive shelf-life forecasts generated by `shelf-life-baseline-v1`, degradation velocities, risk classifications, and guidance.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique prediction record identifier |
| `inventory_id` | Integer | FK (`inventory.id`, CASCADE), Not Null | Target inventory batch |
| `analysis_id` | Integer | FK (`analysis_results.id`, SET NULL), Nullable | Linked CV image analysis (if available) |
| `user_id` | Integer | FK (`users.id`, CASCADE), Not Null | Generating operator or system agent |
| `estimated_remaining_days` | Integer | Not Null | Predicted days until expiration ($\ge 0$) |
| `estimated_expiry_date` | Date | Not Null | Calculated expiration calendar date |
| `risk_level` | String(50) | Not Null, Indexed | Spoilage risk (`LOW RISK`, `MEDIUM RISK`, `HIGH RISK`, `CRITICAL`) |
| `confidence` | Float | Not Null | Transparent heuristic confidence (0.0–1.0) |
| `trend` | String(50) | Not Null | Historical trajectory (`Declining`, `Stable`, `Improving`, `Insufficient Data`) |
| `storage_impact` | Text | Not Null | JSON breakdown of temperature, humidity, and condition impacts |
| `contributing_factors` | Text | Not Null | JSON list of key factors driving degradation |
| `storage_guidance` | Text | Not Null | JSON list of actionable optimization recommendations |
| `input_features` | Text | Not Null | JSON snapshot of exact input features used at prediction time |
| `model_version` | String(50) | Not Null, Default 'shelf-life-baseline-v1' | Predictive engine identifier |
| `created_at` | DateTime | Not Null | Timestamp of prediction generation |
