# Finance Dashboard Backend API

Production-ready Django REST API for financial record management and analytics.

## Project Structure

This repository is organized as a Django backend with the following main apps:

Main apps:

- `users`
- `transactions`
- `dashboard`

## Features

- JWT authentication (login + refresh)
- Role-based access control (Viewer, Analyst, Admin)
- Transactions CRUD with filtering, search, pagination
- Soft delete for transactions
- Dashboard analytics endpoints
- Standardized API response format
- Swagger and Redoc documentation

## Tech Stack

- Python 3.11
- Django 5
- Django REST Framework
- PostgreSQL (or SQLite for quick local run)
- SimpleJWT
- drf-spectacular

## API Response Format

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

## Role-Based Access

### Viewer

- Can view profile
- Can read transactions
- Cannot create, update, or delete transactions
- Cannot access dashboard analytics

### Analyst

- All Viewer permissions
- Can access dashboard analytics
- Cannot create, update, or delete transactions

### Admin

- Full transaction CRUD
- Full dashboard access
- Full user management access

## Key Endpoints

Auth and users:

- `POST /api/users/register/`
- `POST /api/users/login/`
- `POST /api/users/token/refresh/`
- `GET /api/users/me/`

Transactions:

- `GET /api/transactions/`
- `POST /api/transactions/`
- `GET /api/transactions/{id}/`
- `PUT /api/transactions/{id}/`
- `PATCH /api/transactions/{id}/`
- `DELETE /api/transactions/{id}/` (soft delete)

Dashboard:

- `GET /api/dashboard/analytics/`
- `GET /api/dashboard/summary/`

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and update values.

Quick local run with SQLite:

```env
DB_ENGINE=sqlite
DJANGO_ENV=development
DJANGO_DEBUG=True
```

### 3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Start server

```bash
python manage.py runserver
```

Server: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## API Docs

- Swagger UI: `/api/docs/swagger/`
- Redoc: `/api/docs/redoc/`
- OpenAPI schema: `/api/schema/`

## Postman Collection

- `postman/Finance Dashboard API.postman_collection.json`

## Testing Notes

- APIs tested using Postman
- Role-based access paths validated for Viewer, Analyst, and Admin
