# Database Schema - Food Freshness Monitoring Platform

This document details the relational schema design for PostgreSQL (and SQLite fallback).

## Entity Relationship Summary

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
                                                    | 1 : N
                                                    v
                                          +-------------------+
                                          |     inventory     |
                                          |-------------------|
                                          | id (PK)           |
                                          | food_item_id (FK) |
                                          | batch_number      |
                                          | quantity          |
                                          | unit              |
                                          | purchase_date     |
                                          | expiry_date       |
                                          | storage_temp      |
                                          | storage_humidity  |
                                          | packaging_type    |
                                          | storage_duration  |
                                          | created_at        |
                                          | updated_at        |
                                          +-------------------+
```

---

## Table Specifications

### 1. `users`
Stores user profile credentials, assigned system role, and status.

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
Stores master food product details and product taxonomy.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique food item identifier |
| `name` | String(150) | Not Null, Indexed | Product name (e.g. Organic Gala Apple) |
| `category` | String(50) | Not Null, Indexed | Category (`Fruits`, `Vegetables`, `Dairy Products`, `Meat & Poultry`, `Seafood`, `Bakery Products`, `Packaged Foods`, `Beverages`) |
| `description` | Text | Nullable | Detailed product description |
| `created_by` | Integer | FK (`users.id`), Not Null | User ID of creator |
| `created_at` | DateTime | Not Null | Record creation timestamp |
| `updated_at` | DateTime | Not Null | Record update timestamp |

---

### 3. `inventory`
Stores physical batch telemetry, quantities, storage conditions, and expiry dates.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto Increment | Unique batch inventory identifier |
| `food_item_id` | Integer | FK (`food_items.id`), Not Null | Associated food item |
| `batch_number` | String(100) | Not Null, Indexed | Tracking batch number (e.g. BATCH-2026-0801) |
| `quantity` | Float | Not Null | Numerical quantity |
| `unit` | String(30) | Not Null | Unit of measurement (`kg`, `grams`, `liters`, `units`, `boxes`) |
| `purchase_date` | Date | Not Null | Date of purchase/reception |
| `expiry_date` | Date | Not Null, Indexed | Product expiration date |
| `storage_temperature` | Float | Not Null | Temperature reading in °C |
| `storage_humidity` | Float | Not Null | Relative humidity % |
| `packaging_type` | String(100) | Not Null | Packaging type (e.g., Vacuum Sealed, Plastic Tray, Cardboard Box) |
| `storage_duration` | Integer | Not Null | Storage duration in days |
| `created_at` | DateTime | Not Null | Record creation timestamp |
| `updated_at` | DateTime | Not Null | Record update timestamp |

---
