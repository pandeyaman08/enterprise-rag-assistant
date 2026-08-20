# Enterprise RAG Knowledge Assistant

A production-grade enterprise knowledge platform enabling organizations to securely upload, process, index, and search documents using Retrieval-Augmented Generation (RAG).

> 🚧 **Status: Under active development.** Being built incrementally following clean architecture and production-engineering practices. See [Development Status](#development-status) for progress.

## Overview

This project is not a demo chatbot. It is designed as a multi-tenant enterprise platform supporting:

- Multiple LLM providers (OpenAI, Anthropic, Gemini, Ollama, OpenRouter) via a swappable provider abstraction
- Organization → Workspace → Project hierarchy with RBAC
- Full document ingestion pipeline: upload → parsing → chunking → embedding → vector indexing
- Hybrid semantic search with reranking
- Streaming chat with source citations

## Problem Statement

Freelancers, consultants, and small teams accumulate large amounts of unstructured knowledge across contracts, project notes, client documents, and reports — but this information becomes progressively harder to search and retrieve as it grows. Generic search tools rely on exact keyword matches and fail when the phrasing of a query differs from the phrasing in the source document.

This project is being built to explore how a properly engineered RAG (Retrieval-Augmented Generation) system — with semantic search, hybrid retrieval, and reranking — can let a user query their own document corpus in natural language and receive accurate, cited answers, instead of manually searching through files.

While the underlying architecture (multi-tenant organizations, RBAC, provider-agnostic LLM integration) is designed to scale to enterprise use cases, the core problem it solves — "let me ask questions about my own documents and get a trustworthy answer" — is broadly useful to any individual or small team managing a growing body of documents.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| API Framework | FastAPI |
| Validation | Pydantic v2 |
| Database | PostgreSQL + SQLAlchemy 2.x |
| Migrations | Alembic |
| Cache | Redis |
| Vector Store | Qdrant |
| Embeddings | Sentence Transformers |
| Background Jobs | Celery + Redis |
| Dependency Management | uv |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |

## Project Structure

app/
├── core/ # Cross-cutting concerns: settings, security
├── api/v1/ # Versioned API routes
├── modules/ # Feature-based domains (auth, organizations, documents, chat)
└── shared/ # Database session management, custom exceptions

## Local Development Setup

### Prerequisites
- Python 3.12+ (managed via `pyenv`)
- `uv` package manager
- Docker Desktop

### Setup

```bash
git clone https://github.com/pandeyaman08/enterprise-rag-assistant.git
cd enterprise-rag-assistant

uv sync

cp .env.example .env   # then fill in the values

uv run uvicorn app.main:app --reload --port 8000
```

### Run with Docker

```bash
docker compose up --build
```

Once running, visit:
- API health check: http://localhost:8000/health
- Interactive API docs (Swagger UI): http://localhost:8000/docs

## Features

- ✅ RESTful API with versioning (FastAPI)
- ✅ Dockerized development environment
- ✅ Structured configuration via Pydantic Settings

## Development Status

This project is being built incrementally, one module at a time, following clean architecture and production-engineering practices — each phase is fully implemented, tested, and committed before the next begins.

### Completed
- Project foundation — FastAPI bootstrap, Docker dev environment, linting/formatting pipeline (Ruff, Black)
- Database schema — 12 normalized PostgreSQL tables via SQLAlchemy 2.x, with full Alembic migration history covering authentication/RBAC, multi-tenant organization hierarchy, document/chunk storage, chat/messaging, and audit logging

### In Progress / Upcoming
- Authentication & RBAC (JWT, refresh tokens, role-based permissions)
- Document upload & processing pipeline
- Embeddings & vector indexing (Qdrant)
- RAG retrieval: hybrid search, reranking, multi-provider LLM integration
- Streaming chat with source citations
- Security hardening, observability, automated test suite
- CI/CD pipeline and deployment

## License

TBD