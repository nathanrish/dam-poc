
# DAM POC — Digital Asset Management Platform

## Overview

This project is a Proof-of-Concept (POC) Digital Asset Management (DAM) system designed to validate a scalable, production-ready architecture using open source components.

The system provides:

- Asset creation and metadata management
- File upload and storage using S3-compatible object storage (MinIO)
- Metadata persistence using PostgreSQL
- Retrieval of asset metadata and storage location
- Worker pipeline readiness for future media processing

This POC establishes the architectural foundation for a future enterprise media platform supporting images, audio, and video assets.

---

## Objectives

The primary goal of this POC is to validate the complete asset ingestion lifecycle:

```

Client → Backend → Metadata Database → Object Storage → Retrieval

```

Specifically, this POC validates:

- Backend service connectivity to PostgreSQL
- Object storage integration using MinIO
- Asset metadata creation and persistence
- File upload and storage in object storage
- Consistent linkage between metadata and storage

Future phases will extend this to include media processing, streaming, and search.

---

## Architecture

High-level system architecture:

```

```
             ┌─────────────┐
             │  Frontend   │
             │ (Upload UI) │
             └──────┬──────┘
                    │
             ┌──────▼──────┐
             │   FastAPI   │
             │   Backend   │
             └──────┬──────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
```

┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐  
│ PostgreSQL │ │ MinIO │ │ Redis │  
│ Metadata │ │ Object Store│ │ Queue │  
└─────────────┘ └─────────────┘ └─────────────┘

```

Component roles:

| Component | Purpose |
|--------|---------|
| FastAPI | Control plane, API and metadata management |
| PostgreSQL | Persistent metadata storage |
| MinIO | S3-compatible object storage |
| Redis | Queue for future media processing |
| Worker | Future media processing pipeline |
| Frontend | Upload and playback interface (POC) |

---

## Repository Structure

```

dam-poc/

backend/  
main.py  
db.py  
models.py  
storage.py  
requirements.txt

worker/  
worker.py  
transcoder.py  
requirements.txt

frontend/  
index.html

storage/  
(MinIO runtime storage — not tracked in git)

docker-compose.yml  
harness.yaml  
README.md  
.gitignore

```

---

## Prerequisites

Required software:

- Docker
- Python 3.13+
- Git

Optional tools:

- curl
- Postman

---

## Setup Instructions

### 1. Clone repository

```

git clone  
cd dam-poc

```

---

### 2. Start infrastructure services

```

docker compose up -d

```

This starts:

- PostgreSQL → localhost:5432
- MinIO → localhost:9000
- MinIO Console → http://localhost:9001
- Redis → localhost:6379

---

### 3. Create MinIO bucket

Open:

```

[http://localhost:9001](http://localhost:9001/)

```

Login:

```

Username: minio  
Password: minio123

```

Create bucket:

```

media

```

---

### 4. Start backend service

```

cd backend  
pip install -r requirements.txt  
uvicorn main:app --reload --host 0.0.0.0 --port 8000

```

Verify backend is running:

```

[http://localhost:8000/health](http://localhost:8000/health)

```

Expected response:

```

{"status":"ok"}

```

---

## API Usage

Interactive API documentation:

```

[http://localhost:8000/docs](http://localhost:8000/docs)

```

---

### Create Asset

```

POST /assets

```

Response:

```

{  
"asset_id": "UUID"  
}

```

---

### Upload Asset File

```

POST /assets/{asset_id}/upload

```

Uploads file to MinIO and updates metadata.

---

### Retrieve Asset Metadata

```

GET /assets/{asset_id}

```

Returns asset metadata and storage path.

---

## Storage Model

Object storage structure:

```

media/  
asset-id/  
original.file

```

Metadata stored separately in PostgreSQL.

This separation allows:

- Independent scaling of storage and metadata
- Storage backend abstraction
- Future migration to cloud storage

---

## Development and Validation

This project includes automated validation using Harness.

Harness executes integration tests to verify:

- Backend startup
- Database connectivity
- Asset creation
- File upload
- Object storage integration
- Metadata retrieval

Harness configuration:

```

harness.yaml

```

Harness ensures system integrity during development and prevents regressions.

Harness is a development and validation tool and is not required for runtime operation.

---

## Autonomous Development (Antigravity)

Antigravity is used as an autonomous development agent during implementation.

Antigravity operates in conjunction with Harness:

```

Harness detects failures  
↓  
Antigravity applies fixes  
↓  
Harness re-validates system

```

This enables rapid development convergence and automated correction of integration issues.

Antigravity is a development tool and is not required for production deployment.

---

## Development Workflow

Recommended workflow:

```

Modify code  
Commit changes  
Run Harness validation  
Allow Antigravity to resolve failures if present  
Verify system stability

```

---

## Future Enhancements

Planned features:

- Video transcoding using FFmpeg
- Streaming support (HLS / DASH)
- Video playback integration
- Search indexing (OpenSearch)
- Authentication and authorization
- Cloud storage integration (AWS S3)
- Kubernetes deployment
- Media processing pipeline

---

## Production Migration Path

POC components map directly to production infrastructure:

| POC | Production |
|---|---|
MinIO | AWS S3 |
Postgres container | Managed database (RDS, Cloud SQL) |
Redis container | Managed Redis |
Docker Compose | Kubernetes |
Local worker | Distributed worker cluster |

No architectural redesign required.

---

## Architectural Principles

This system is designed using the following principles:

- Storage abstraction
- Metadata-driven asset management
- Separation of control plane and data plane
- Immutable asset storage model
- Event-driven processing readiness
- Horizontal scalability readiness

---

## Current Status

Current phase:

```

POC — Asset ingestion and storage validation

```

Next phase:

```

Media processing and streaming support

```

---

## Summary

This POC validates the foundational architecture for a scalable Digital Asset Management system capable of evolving into a full enterprise media platform.

The system successfully demonstrates:

- Asset metadata management
- Object storage integration
- Storage abstraction
- Future-ready architecture for media processing and streaming
```

---
