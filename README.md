# Deep Research Assistant

A production-grade agentic application for answering analytical questions using LangGraph, Streamlit, and Docker.

## Features
- Multi-step reasoning with LangGraph
- Web search and document retrieval
- User-friendly Streamlit UI
- Dockerized for easy deployment
- Unit tests and comprehensive documentation

## Setup
See [docs/setup.md](docs/setup.md) for instructions.

## Usage
See [docs/usage.md](docs/usage.md) for details.

## Architecture
See [architecture](docs/architecture.md) for an overview.


## Deployment
Push to a public GitHub repository.
Follow `docs/setup.md` for local or cloud deployment instructions using Docker Compose.

## Scalability
Use FAISS for efficient vector search.
Modular design allows adding new agents/tools.
Docker enables horizontal scaling.

## Testing
Run pytest tests/ to execute unit tests for agents and tools.