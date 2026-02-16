# DAM POC — Digital Asset Management System

## Overview

This project is a Proof of Concept (POC) for a scalable Digital Asset Management (DAM) system designed to manage digital media assets including images, audio, and video.

The system separates metadata from binary storage, enabling scalable ingest pipelines, media processing, and delivery workflows.

This architecture follows patterns used in enterprise media platforms and is designed to evolve into a production-grade system.

---

# Architecture Overview

## High-Level Architecture

```
                ┌──────────────┐
                │    Client     │
                │ (UI / API)    │
                └──────┬───────┘
                       │
                       ▼
               ┌──────────────┐
               │ FastAPI      │
               │ Backend API  │
               └──────┬───────┘
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│ PostgreSQL │  │   MinIO    │  │   Redis    │
│ Metadata   │  │ Object     │  │ Queue      │
│ Storage    │  │ Storage    │  │ System     │
└────────────┘  └────────────┘  └──────┬─────┘
                                        │
                                        ▼
                                   ┌──────────┐
                                   │ Worker   │
                                   │ Processor│
                                   └──────────┘
```

---

## Component Responsibilities

### FastAPI Backend

Responsible for:

* Asset metadata creation
* Upload coordination
* Asset retrieval
* Storage orchestration

Stateless service.

---

### PostgreSQL

Stores structured metadata:

```
asset_id
filename
storage_path
created_at
```

Source of truth for asset identity.

---

### MinIO Object Storage

Stores binary media files.

S3-compatible interface.

Can be replaced with:

* AWS S3
* Dell Isilon
* Azure Blob Storage
* Google Cloud Storage

---

### Redis

Acts as message broker for background processing.

Enables asynchronous workflows.

---

### Worker

Handles background tasks such as:

* Transcoding
* Thumbnail generation
* Media analysis

Currently scaffolded for future expansion.

---

# Asset Ingest Sequence Diagram

This shows how assets are created and uploaded.

```
Client                Backend              PostgreSQL             MinIO
  │                     │                      │                    │
  │ POST /assets       │                      │                    │
  │───────────────────▶│                      │                    │
  │                     │ INSERT metadata     │                    │
  │                     │────────────────────▶│                    │
  │                     │ COMMIT              │                    │
  │                     │◀────────────────────│                    │
  │ UUID returned      │                      │                    │
  │◀───────────────────│                      │                    │
  │                     │                      │                    │
  │ POST /assets/{id}/upload                 │                    │
  │───────────────────▶│                      │                    │
  │                     │ Verify asset exists │                    │
  │                     │────────────────────▶│                    │
  │                     │ OK                  │                    │
  │                     │◀────────────────────│                    │
  │                     │ Upload file        │───────────────────▶│
  │                     │                    │                    │
  │ Success returned   │                    │                    │
  │◀───────────────────│                    │                    │
```

---

# Asset Retrieval Sequence

```
Client             Backend              PostgreSQL
  │                  │                      │
  │ GET /assets/{id}│                      │
  │────────────────▶│                      │
  │                  │ Query metadata      │
  │                  │────────────────────▶│
  │                  │ Return metadata     │
  │                  │◀────────────────────│
  │ Return result    │                      │
  │◀────────────────│                      │
```

---

# Future Processing Pipeline Sequence

```
Upload complete
     │
     ▼
 Backend
     │
     ▼
 Redis Queue
     │
     ▼
 Worker
     │
     ├── Transcode video
     ├── Generate thumbnails
     ├── Extract metadata
     └── Update database
```

---

# Repository Structure

```
dam-poc/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── db.py
│   ├── storage.py
│   └── requirements.txt
│
├── worker/
│   ├── worker.py
│   ├── transcoder.py
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
├── docker-compose.yml
├── harness.yaml
├── README.md
└── .gitignore
```

---

# Local Development Setup

## Start infrastructure

```
docker compose up -d
```

Starts:

* PostgreSQL
* MinIO
* Redis

---

## Start backend

```
cd backend
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

---

## Access API documentation

```
http://127.0.0.1:8000/docs
```

---

## Access MinIO console

```
http://localhost:9001
```

Credentials:

```
minio
minio123
```

---

# Testing Workflow

## Create asset

```
POST /assets
```

Returns UUID.

---

## Upload file

```
POST /assets/{asset_id}/upload
```

Stores binary file.

---

## Retrieve asset

```
GET /assets/{asset_id}
```

Returns metadata.

---

# Storage Model

Metadata stored in PostgreSQL.

Binary stored in MinIO.

Relationship:

```
PostgreSQL record → references → MinIO object
```

---

# Design Principles

## Metadata-first ingest

Asset identity created before upload.

Enables reliable workflows.

---

## Stateless services

Backend stores no local files.

All state in storage systems.

---

## Storage abstraction

S3-compatible interface enables portability.

---

## Horizontal scalability

Backend and workers scale independently.

---

# Harness Validation

Harness validates:

* Service startup
* Health endpoint
* Asset creation
* Upload
* Retrieval

Ensures system correctness.

---

# Future Enhancements

Planned:

* Video transcoding pipeline
* HLS/DASH streaming
* Open-source media player integration
* Metadata search indexing
* Authentication and authorization
* Cloud deployment
* AI tagging

---

# System Properties

This system is:

* Stateless
* Horizontally scalable
* Storage-independent
* Extensible
* Cloud-portable

---

# Startup Summary

Start system:

```
docker compose up -d
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

System becomes operational.

---

