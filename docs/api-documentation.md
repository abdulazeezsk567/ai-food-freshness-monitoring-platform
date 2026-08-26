# API Documentation - Food Freshness Monitoring Platform

The backend provides RESTful JSON endpoints. Complete OpenAPI interactive documentation is generated automatically by FastAPI at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Authentication

All protected endpoints require HTTP Bearer authentication token passed in headers:
```text
Authorization: Bearer <your_jwt_access_token>
```

---

## Endpoint Reference

### 1. Authentication Router (`/api/auth`)

#### `POST /api/auth/register`
- **Description**: Registers a new user account.
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "role": "RETAIL_MANAGER"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "RETAIL_MANAGER",
    "is_active": true,
    "created_at": "2026-08-26T21:00:00Z"
  }
  ```

#### `POST /api/auth/login`
- **Description**: Authenticates user and returns JWT bearer token.
- **Request Body** (`application/x-www-form-urlencoded` or JSON):
  ```json
  {
    "username": "john@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "role": "RETAIL_MANAGER"
    }
  }
  ```

#### `GET /api/auth/me`
- **Description**: Fetches current authenticated user profile.
- **Header**: `Authorization: Bearer <token>`
- **Response** (200 OK): User object.

---

### 2. User Management Router (`/api/users`)

- `GET /api/users` (Admin/Inspector only) - List users
- `GET /api/users/{id}` - Get user details by ID
- `PUT /api/users/{id}` - Update user name/role/status
- `DELETE /api/users/{id}` (Admin only) - Remove user account

---

### 3. Food Items Router (`/api/food-items`)

- `POST /api/food-items` - Register a food product
- `GET /api/food-items` - List food products with search/category filtering
- `GET /api/food-items/{id}` - Get food product details
- `PUT /api/food-items/{id}` - Update food product
- `DELETE /api/food-items/{id}` - Delete food product

---

### 4. Inventory Router (`/api/inventory`)

- `POST /api/inventory` - Create inventory batch record
- `GET /api/inventory` - List inventory records with status calculations
- `GET /api/inventory/{id}` - Get single batch record details
- `PUT /api/inventory/{id}` - Update batch storage/quantity info
- `DELETE /api/inventory/{id}` - Delete inventory batch

---

### 5. Stats Router (`/api/stats`)

- `GET /api/stats/dashboard` - Returns aggregate counts (Total Food Items, Active Batches, Expiring Soon, Expired, Fresh, Near Spoilage).

---
