# Zorvyn Finance Backend API

A robust, scalable finance data processing and access control backend built with FastAPI, SQLAlchemy, and PostgreSQL.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication with role-based access control
- **User Management**: Multi-role system (Admin, Analyst, Viewer) with granular permissions
- **Transaction Management**: Complete CRUD operations for financial transactions
- **Dashboard Analytics**: Real-time financial insights and trends
- **Data Validation**: Comprehensive input validation with Pydantic schemas
- **Database Migrations**: Alembic-based schema management
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Testing Suite**: Full test coverage with pytest and async support

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Environment Setup](#environment-setup)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [API Documentation](#api-documentation)
7. [Authentication](#authentication)
8. [API Endpoints](#api-endpoints)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Contributing](#contributing)

## 🛠 Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Node.js (for frontend development)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd finance_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration (optional)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🗄️ Database Setup

### Option 1: Using Docker (Recommended)

```bash
docker run --name postgres-finance \
  -e POSTGRES_DB=finance_db \
  -e POSTGRES_USER=finance_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:13
```

### Option 2: Local PostgreSQL

1. Install PostgreSQL on your system
2. Create a database:
   ```sql
   CREATE DATABASE finance_db;
   CREATE USER finance_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE finance_db TO finance_user;
   ```

### Database Migrations

1. **Initialize Alembic** (if not already done):
   ```bash
   alembic init alembic
   ```

2. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

3. **Create new migration** (after model changes):
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

### Seed Data

Populate the database with sample data:

```bash
# Using psql
psql -h localhost -U finance_user -d finance_db -f seeds/demo_seed.sql

# Or using Python (after setting up .env)
python -c "
import asyncio
from app.infra.database import engine
from app.models import Base
from seeds.demo_seed import seed_data

async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()

asyncio.run(setup())
"
```

## 🚀 Running the Application

### Development Mode

```bash
# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the run script
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Production server with workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Swagger UI
Visit `http://localhost:8000/docs` for interactive API documentation.

### ReDoc
Visit `http://localhost:8000/redoc` for alternative documentation.

### OpenAPI Spec
Access the raw OpenAPI specification at `http://localhost:8000/openapi.json`

## 🔐 Authentication

### Getting a Token

1. **Register a user** (or use existing demo users):
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@zorvyn.com",
       "full_name": "Admin User",
       "password": "Admin1234!"
     }'
   ```

2. **Login to get token**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@zorvyn.com",
       "password": "Admin1234!"
     }'
   ```

3. **Use the token** in API requests:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/transactions" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

### Demo Users

| Role | Email | Password |
|-------|-------|----------|
| Admin | admin@zorvyn.com | Admin1234! |
| Analyst | analyst@zorvyn.com | Analyst1234! |
| Viewer | viewer@zorvyn.com | Viewer1234! |

## 🛣 API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|---------|-----------|-------------|----------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login and get token | No |

### Users (`/api/v1/users`)

| Method | Endpoint | Description | Auth Required | Role Required |
|---------|-----------|-------------|----------------|---------------|
| GET | `/` | List all users | Yes | Admin |
| GET | `/{user_id}` | Get user by ID | Yes | Admin |
| POST | `/` | Create new user | Yes | Admin |
| PUT | `/{user_id}` | Update user | Yes | Admin |
| DELETE | `/{user_id}` | Delete user | Yes | Admin |

### Transactions (`/api/v1/transactions`)

| Method | Endpoint | Description | Auth Required | Role Required |
|---------|-----------|-------------|----------------|---------------|
| GET | `/` | List transactions | Yes | Any |
| POST | `/` | Create transaction | Yes | Admin, Analyst |
| GET | `/{transaction_id}` | Get transaction by ID | Yes | Any |
| PUT | `/{transaction_id}` | Update transaction | Yes | Admin, Analyst |
| DELETE | `/{transaction_id}` | Soft delete transaction | Yes | Admin, Analyst |

**Query Parameters for GET /transactions:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `type`: Filter by type (INCOME/EXPENSE)
- `category`: Filter by category
- `date_from`: Filter by start date (YYYY-MM-DD)
- `date_to`: Filter by end date (YYYY-MM-DD)

### Dashboard (`/api/v1/dashboard`)

| Method | Endpoint | Description | Auth Required | Role Required |
|---------|-----------|-------------|----------------|---------------|
| GET | `/summary` | Get financial summary | Yes | Any |
| GET | `/category-totals` | Get totals by category | Yes | Any |
| GET | `/trends` | Get financial trends | Yes | Analyst, Admin |

**Query Parameters for GET /dashboard/trends:**
- `period`: Time period (MONTHLY/WEEKLY)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Structure

```
tests/
├── conftest.py          # Test configuration and fixtures
├── test_auth.py         # Authentication tests
├── test_users.py        # User management tests
├── test_transactions.py # Transaction tests
└── test_dashboard.py    # Dashboard analytics tests
```

### Test Fixtures

The test suite includes:
- **Database isolation**: Each test runs with a fresh in-memory SQLite database
- **User fixtures**: Pre-configured users with different roles
- **Sample data**: Test transactions and data for comprehensive testing

## 🚀 Deployment

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t zorvyn-finance-api .
   ```

2. **Run with Docker Compose**:
   ```yaml
   version: '3.8'
   services:
     api:
       build: .
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/finance_db
       depends_on:
         - db
     
     db:
       image: postgres:13
       environment:
         - POSTGRES_DB=finance_db
         - POSTGRES_USER=user
         - POSTGRES_PASSWORD=pass
       volumes:
         - postgres_data:/var/lib/postgresql/data
   ```

### Environment Variables for Production

```env
# Production Database
DATABASE_URL=postgresql+asyncpg://user:secure_password@db-host:5432/finance_db

# Security
SECRET_KEY=your-production-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

## 🏗 Project Structure

```
finance_backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── dashboard.py     # Dashboard analytics
│   │       ├── router.py        # API router aggregation
│   │       ├── transactions.py # Transaction management
│   │       └── users.py         # User management
│   ├── core/
│   │   ├── config.py         # Configuration settings
│   │   ├── dependencies.py   # FastAPI dependencies
│   │   └── security.py      # JWT and security utilities
│   ├── infra/
│   │   └── database.py      # Database configuration
│   ├── models/
│   │   ├── base.py          # Base model classes
│   │   ├── transaction.py   # Transaction model
│   │   └── user.py          # User model
│   ├── schemas/
│   │   ├── auth.py          # Auth request/response schemas
│   │   ├── transaction.py   # Transaction schemas
│   │   └── user.py          # User schemas
│   ├── services/
│   │   └── dashboard_service.py # Business logic for dashboard
│   └── main.py              # FastAPI application entry point
├── alembic/
│   ├── versions/             # Database migration files
│   ├── env.py              # Alembic configuration
│   └── script.py.mako      # Migration template
├── seeds/
│   ├── demo_seed.sql        # Sample data for development
│   └── schema.sql          # Database schema reference
├── tests/
│   ├── conftest.py         # Test configuration
│   ├── test_auth.py         # Authentication tests
│   ├── test_dashboard.py     # Dashboard tests
│   ├── test_transactions.py # Transaction tests
│   └── test_users.py        # User management tests
├── requirements.txt         # Python dependencies
├── alembic.ini           # Alembic configuration
├── pytest.ini            # Pytest configuration
└── README.md             # This file
```


### Development Guidelines

- Follow PEP 8 for code style
- Add type hints for all functions
- Write tests for new features
- Update documentation for API changes
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the [API Documentation](#api-documentation)
2. Review existing [Issues](../../issues)
3. Create a new issue with detailed information

## 🔄 Version History

- **v1.0.0** - Initial release with core features
  - User authentication and authorization
  - Transaction management
  - Dashboard analytics
  - Role-based access control

---

**Built with  using FastAPI, SQLAlchemy, and PostgreSQL**
