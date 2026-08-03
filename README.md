# Generic Data Ingestion Service

## Overview

This project is a configuration-driven data ingestion service developed in Python. It fetches data from multiple REST APIs, supports different pagination strategies, stores the fetched data into a SQLite database, and exposes HTTP endpoints to trigger ingestion and monitor the application.

The application is designed to be modular, extensible, and easy to deploy using Docker.

---

# Features

- Generic configuration-based ingestion
- Supports multiple REST APIs
- Query and Offset pagination
- SQLite database using SQLAlchemy
- Retry mechanism for failed API requests
- REST endpoints for ingestion and monitoring
- Docker support
- Modular project structure
- Error handling and logging

---

# Project Structure

```
ingestion_project/
│
├── ingestion_service/
│   ├── __init__.py
│   ├── client.py
│   ├── database.py
│   ├── ingestor.py
│   ├── models.py
│   ├── pagination.py
│   └── storage.py
│
├── config.json
├── server.py
├── create_db.py
├── check_db.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── database.db
└── README.md
```

---

# Architecture

```
                    config.json
                         │
                         ▼
                 Ingestion Engine
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
 JSONPlaceholder API            DummyJSON API
          │                             │
          └──────────────┬──────────────┘
                         ▼
                  Pagination Module
                         ▼
                    HTTP Client
                         ▼
                  SQLite Database
                         ▼
                   HTTP API Server
```

---

# Technologies Used

- Python 3.13
- SQLite
- SQLAlchemy
- Requests
- Docker
- Docker Compose
- Python HTTP Server

---

# Configuration

The APIs to ingest are defined in `config.json`.

Example:

```json
{
  "sources": [
    {
      "name": "jsonplaceholder-posts",
      "url": "https://jsonplaceholder.typicode.com/posts",
      "pagination": {
        "type": "query",
        "page_param": "_page",
        "page_size_param": "_limit",
        "page_size": 3,
        "max_pages": 2
      },
      "record_path": null
    },
    {
      "name": "dummyjson-products",
      "url": "https://dummyjson.com/products",
      "pagination": {
        "type": "query",
        "page_param": "skip",
        "page_size_param": "limit",
        "page_size": 2,
        "max_pages": 2,
        "page_strategy": "offset"
      },
      "record_path": "products"
    }
  ]
}
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd ingestion_project
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Create Database

```bash
python create_db.py
```

---

# Run the Application

```bash
python server.py
```

Server starts at

```
http://localhost:8000
```

---

# API Endpoints

## Health Check

### Request

```
GET /health
```

### Response

```json
{
    "status": "ok"
}
```

---

## Configured Sources

### Request

```
GET /sources
```

Returns the configured API sources.

---

## Ingest Data

### Request

```
POST /ingest
```

Request Body

```json
{}
```

### Sample Response

```json
{
    "status": "success",
    "summary": [
        {
            "source": "jsonplaceholder-posts",
            "records_ingested": 6,
            "pages_processed": 2
        },
        {
            "source": "dummyjson-products",
            "records_ingested": 4,
            "pages_processed": 2
        }
    ],
    "total_records": 10
}
```

---

## View Stored Records

### Request

```
GET /records
```

Returns all stored records from SQLite.

---

# Database

Database: SQLite

File:

```
database.db
```

Table:

```
records
```

Columns

| Column | Type |
|---------|------|
| id | Integer |
| source | String |
| endpoint | String |
| data | JSON |
| created_at | DateTime |

---

# Pagination

The application supports two pagination strategies.

### Query Pagination

Example

```
?_page=1&_limit=3
```

### Offset Pagination

Example

```
?skip=2&limit=2
```

---

# Retry Logic

The HTTP client retries failed requests up to **3 times** before reporting an error.

Benefits

- Handles temporary network failures
- Improves reliability
- Prevents unnecessary ingestion failures

---

# Running with Docker

## Build Image

```bash
docker build -t ingestion-service .
```

---

## Run Container

```bash
docker compose up --build
```

---

## Stop Container

```bash
docker compose down
```

---

# Testing

Health

```
http://localhost:8000/health
```

Sources

```
http://localhost:8000/sources
```

Records

```
http://localhost:8000/records
```

Ingest

```
POST http://localhost:8000/ingest
```

---

# Design Decisions

- Used a configuration-driven architecture to allow adding new APIs without changing code.
- Implemented a generic pagination module supporting multiple pagination strategies.
- Used SQLite for lightweight storage.
- Used SQLAlchemy ORM for database interactions.
- Organized the application into separate modules for better maintainability.
- Added retry logic to improve reliability during temporary API failures.
- Dockerized the application for consistent deployment.

---

# Trade-offs

- SQLite is ideal for local development but is not intended for high-concurrency production environments.
- The ingestion process is synchronous. Asynchronous processing could improve performance for larger workloads.
- JSON storage provides flexibility but limits advanced relational querying.

---

# Future Improvements

- Duplicate detection
- Scheduled ingestion
- Authentication support
- PostgreSQL/MySQL support
- Incremental ingestion
- Metrics and monitoring
- Unit and integration tests

---

# AI Usage

AI assistance was used for:

- Designing the project structure
- Debugging Python import issues
- Implementing SQLite integration
- Adding retry logic
- Creating Docker support
- Preparing project documentation

One issue encountered during development was a Docker build failure caused by using a `requirements.txt` generated from a global Python environment. The file contained many unrelated packages, including Windows-specific dependencies (`pywin32`, `pypiwin32`), which could not be installed inside the Linux Docker container. The issue was resolved by creating a minimal `requirements.txt` containing only the dependencies required by this project (`requests` and `SQLAlchemy`).

---

# Author

**Silla Manoj Kumar**

B.Tech – Artificial Intelligence & Machine Learning

GitHub: https://github.com/<your-username>

Email: sillamanojsilla@gmail.com