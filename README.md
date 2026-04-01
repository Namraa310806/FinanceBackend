# Finance Dashboard Backend API

Production-oriented Django REST API for financial record management and analytics, built for backend assessment standards.

## Project Overview

This project implements a modular finance backend with:

- JWT-based authentication and role-driven authorization
- clean architecture through app-level service layers
- robust validation and standardized API response envelopes
- transaction lifecycle management with soft delete
- analytics endpoints for dashboard use cases

Apps included:

- users
- transactions
- dashboard

## Features

- Custom User model with roles: VIEWER, ANALYST, ADMIN
- Register, login, refresh token, profile APIs
- Admin-only user management APIs
- Transaction CRUD APIs with:
- filtering by date range, category, type
- search support
- pagination
- soft delete (no hard data loss)
- Dashboard analytics APIs with aggregations:
- total income
- total expense
- net balance
- category-wise totals
- recent transactions
- monthly trends
- Global error handling and consistent response contracts
- OpenAPI schema + Swagger + Redoc

## Tech Stack

- Python 3.11
- Django 5
- Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt
- drf-spectacular
- python-decouple

## Response Contract

All APIs follow a consistent structure.

Success:

```json
{
  "status": "success",
  "message": "Short message",
  "data": {}
}
```

Error:

```json
{
  "status": "error",
  "message": "Error message",
  "errors": {}
}
```

## Role-Based Access Explanation

### Viewer

- Can authenticate and fetch own profile
- Can read transactions
- Cannot create, update, or delete transactions
- Cannot access dashboard analytics
- Cannot manage users

### Analyst

- Inherits all Viewer access
- Can access dashboard analytics endpoints
- Cannot create, update, or delete transactions
- Cannot manage users

### Admin

- Full transaction CRUD
- Full access to dashboard endpoints
- Full user management access (list/create/update/delete users)

## API Endpoints (With Examples)

Base path: /api

### 1. Register User

- Endpoint: /api/users/register/
- Method: POST

Sample request:

```http
POST /api/users/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "StrongPass@123",
  "first_name": "John",
  "last_name": "Doe"
}
```

Sample response (201):

```json
{
  "status": "success",
  "message": "User registered successfully.",
  "data": {
    "id": 5,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "VIEWER",
    "is_active": true,
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

### 2. Login

- Endpoint: /api/users/login/
- Method: POST

Sample request:

```http
POST /api/users/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "StrongPass@123"
}
```

Sample response (200):

```json
{
  "status": "success",
  "message": "Login successful.",
  "data": {
    "refresh": "<refresh-token>",
    "access": "<access-token>",
    "user": {
      "id": 5,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "VIEWER",
      "is_active": true,
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2026-04-01T12:00:00Z"
    }
  }
}
```

### 3. Create Transaction (Admin)

- Endpoint: /api/transactions/
- Method: POST

Sample request:

```http
POST /api/transactions/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "amount": "2500.00",
  "type": "INCOME",
  "category": "Salary",
  "date": "2026-04-01",
  "notes": "Monthly payroll"
}
```

Sample response (201):

```json
{
  "status": "success",
  "message": "Transaction created successfully.",
  "data": {
    "id": 42,
    "amount": "2500.00",
    "type": "INCOME",
    "category": "Salary",
    "date": "2026-04-01",
    "notes": "Monthly payroll",
    "created_at": "2026-04-01T13:00:00Z"
  }
}
```

### 4. List Transactions (Filtered + Search + Pagination)

- Endpoint: /api/transactions/?start_date=2026-01-01&end_date=2026-03-31&type=EXPENSE&category=Food&search=dinner&page=1&page_size=10
- Method: GET

Sample response (200):

```json
{
  "status": "success",
  "message": "Transactions fetched successfully.",
  "data": {
    "count": 12,
    "next": "http://127.0.0.1:8000/api/transactions/?page=2",
    "previous": null,
    "results": [
      {
        "id": 77,
        "amount": "1200.00",
        "type": "EXPENSE",
        "category": "Food",
        "date": "2026-03-11",
        "notes": "Team dinner",
        "created_at": "2026-03-11T17:10:00Z"
      }
    ]
  }
}
```

### 5. Dashboard Analytics (Analyst/Admin)

- Endpoint: /api/dashboard/analytics/
- Method: GET

Sample response (200):

```json
{
  "status": "success",
  "message": "Dashboard analytics fetched successfully.",
  "data": {
    "total_income": "50000.00",
    "total_expense": "30000.00",
    "net_balance": "20000.00",
    "category_breakdown": {
      "Food": "5000.00",
      "Salary": "50000.00"
    },
    "recent_transactions": [
      {
        "id": 101,
        "amount": "1800.00",
        "type": "EXPENSE",
        "category": "Rent",
        "date": "2026-04-01",
        "notes": "Monthly rent"
      }
    ],
    "monthly_trends": [
      {
        "month": "2026-03",
        "income": "20000.00",
        "expense": "12000.00",
        "net": "8000.00",
        "transaction_count": 15
      }
    ]
  }
}
```

### 6. Validation Error Example

- Endpoint: /api/transactions/
- Method: POST

Sample request:

```http
POST /api/transactions/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "amount": "0",
  "type": "INVALID",
  "category": "",
  "date": "bad-date"
}
```

Sample response (400):

```json
{
  "status": "error",
  "message": "Validation failed.",
  "errors": {
    "amount": ["Amount must be greater than zero."],
    "type": ["Type must be either INCOME or EXPENSE."],
    "category": ["Category cannot be blank."],
    "date": ["Date must be in YYYY-MM-DD format."]
  }
}
```

## Setup Instructions

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd Zorvyn
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a .env file at project root using [.env.example](.env.example):

```env
DJANGO_SECRET_KEY=replace-with-secure-key
DJANGO_ENV=development
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=finance_dashboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

TIME_ZONE=UTC
JWT_ACCESS_TOKEN_MINUTES=30
JWT_REFRESH_TOKEN_DAYS=1
THROTTLE_ANON_RATE=60/minute
THROTTLE_USER_RATE=120/minute
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create admin user

```bash
python manage.py createsuperuser
```

### 6. Run server

```bash
python manage.py runserver
```

Server URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## API Documentation

- OpenAPI schema: /api/schema/
- Swagger UI: /api/docs/swagger/
- Redoc: /api/docs/redoc/

## Testing

- APIs were tested using Postman collections with JWT auth flows.
- Role-based access was explicitly verified for Viewer, Analyst, and Admin.
- Validation scenarios were tested for incorrect amount, type, date, and missing required fields.
- Permission scenarios were tested for unauthorized write attempts and restricted dashboard access.

## Postman Collection

Postman collection file:

- [postman/Finance Dashboard API.postman_collection.json](postman/Finance%20Dashboard%20API.postman_collection.json)

How to use:

1. Open Postman and click Import.
2. Select [postman/Finance Dashboard API.postman_collection.json](postman/Finance%20Dashboard%20API.postman_collection.json).
3. Set collection variable base_url to your running server, for example [http://127.0.0.1:8000](http://127.0.0.1:8000).
4. Run Login (JWT). The test script automatically stores access_token and refresh_token.
5. For transaction update/delete/retrieve endpoints, set transaction_id to an existing record ID.
6. Execute requests folder-wise: Auth & Users, Transactions, then Dashboard.

Notes:

- Authorization header is preconfigured as Bearer {{access_token}} for protected APIs.
- Register and Login requests do not require Authorization.

## Assumptions

- Public signup always creates a VIEWER user (prevents privilege escalation).
- Admin role assignment/promotion is done through secure admin-only flows.
- Transaction delete is soft delete only to preserve auditability and history.
- All transaction reads are user-scoped and exclude soft-deleted records.
- Dashboard analytics only use active (non-deleted) records.
- PostgreSQL is the default target database for assessment environments.

## Notes for Evaluators

- Architecture emphasizes separation of concerns via serializers, permissions, service layer, and thin views.
- Error handling and response contracts are standardized for production-readiness.
- Endpoint docs and examples are intentionally explicit for quick assessment review.
#   F i n a n c e B a c k e n d  
 