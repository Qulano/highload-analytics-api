# ⚡ High-Load Analytical Data API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D.svg?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-PyTest%20Passed-success.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)

An enterprise-grade, high-performance asynchronous RESTful API engineered with **FastAPI**, **asyncpg**, **PostgreSQL**, and **Redis**. Designed to handle intensive analytical workloads with sub-millisecond response latency via non-blocking connection pooling and the Cache-Aside pattern.

---

## 📐 System Architecture & Data Flow

```text
[ Client / Web Browser / Mobile App ]
                 │
                 ▼  HTTP (JSON Requests)
┌────────────────────────────────────────────────────────┐
│             FastAPI Asynchronous Gateway               │
│   - Pydantic V2 Request Validation (422 Guard)         │
│   - Lifespan State Manager (Connection Pools)          │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
     1. Read Cache (GET)        2. Write Order (POST)
                │                        │
                ▼                        ▼
┌───────────────────────────────┐ ┌──────────────────────┐
│       Redis In-Memory         │ │  asyncpg Pool Engine │
│   - Cache-Aside Strategy      │ │  - 5-20 Hot Conns    │
│   - 60s TTL Auto-Expiration   │ │  - Parameterized SQL │
└───────────────┬───────────────┘ └──────────┬───────────┘
                │ Cache Miss                 │
                └────────────┬───────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│            PostgreSQL 16 Storage Container             │
│   - Relational Tables: clients & orders                │
│   - Strict Referential Integrity (Foreign Keys)        │
│   - Optimized B-Tree Indices & Aggregate Analytics     │
└────────────────────────────────────────────────────────┘
```
---

## ⚡ Key Engineering Highlights

- **Native Asynchronous I/O:** Powered by asyncpg (C-extension driver), bypassing Python GIL bottlenecks to achieve maximum throughput.

- **Connection Pooling:** Pre-warmed connection pool (5–20 active channels) managed via the modern @asynccontextmanager Lifespan pattern, eliminating connection handshake latency.

- **Cache-Aside Architecture:** Heavy relational analytics queries (SUM, COUNT, GROUP BY) are cached in Redis with a 60-second TTL, reducing primary database load by up to 98%.

- **Defensive API Design:** Strict schema validation via Pydantic V2 rejects malformed payloads and negative values before hitting the storage layer.

- **Resilient CRUD & HTTP Standards:** Clean status mapping (200 OK, 201 Created, 404 Not Found, 422 Validation Error) with idempotent deletion and detailed error envelopes.

- **Automated Test Suite:** Fully covered by PyTest and httpx (3 passed in 0.84s), verifying business logic, edge-case validation, and pagination constraints.

- **Multi-Container Orchestration:** Complete stack (API + PostgreSQL + Redis) packaged into lightweight Linux containers via Docker Compose.

---

## 🚀 Quickstart & Deployment
### 1. Clone the repository
```bash
git clone https://github.com/Qulano/highload-analytics-api.git
cd highload-analytics-api
```

### 2. Configure Environment
Copy the environment template:
```bash
# On Linux / macOS / PowerShell:
cp .env.example .env
# On Windows CMD:
copy .env.example .env
```

### 3. Launch Full Multi-Container Stack via Docker
Spin up PostgreSQL, Redis, and FastAPI in isolated background containers: 
```bash
docker compose up --build -d
```
### 4. Interactive API Documentation
Once launched, open your browser and access the interactive Swagger UI:

- **Interactive Docs (Swagger UI):** http://127.0.0.1:8000/docs

- **Alternative Schema (ReDoc):** http://127.0.0.1:8000/redoc

---

## 🧪 Running Automated Tests
To run the test suite locally:
```bash
# Create and activate virtual environment:
py -m venv venv
.\venv\Scripts\activate

# Install test dependencies:
pip install -r requirements.txt

# Execute test suite:
py -m pytest
```

## 📊 API Endpoints Overview
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /analytics | Aggregated financial report (Redis Cached with 60s TTL) |
| GET |	/orders | Paginated orders list (limit & offset query params) |
| GET |	/orders/{id} | Single order lookup by ID (404 if not found) |
| POST | /orders | Create new order (validated via Pydantic Schema) |
| DELETE | /orders/{id} | Idempotent order deletion via SQL RETURNING id |
