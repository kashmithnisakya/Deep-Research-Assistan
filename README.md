# Deep Research Assistant

A production-grade agentic application for answering analytical questions using LangGraph, Streamlit, and Docker.

## Features
- Multi-step reasoning with LangGraph
- Web search and document retrieval
- User-friendly Streamlit UI
- Dockerized for easy deployment
- Unit tests and comprehensive documentation

## Setup
## Setup
1. Clone the repository and navigate to the project directory.
2. Create a `.env` file with your OpenAI and Serper API keys.
3. Start the application with `docker-compose up --build`.
4. Access at `http://localhost:8501`.
See [docs/setup.md](docs/setup.md) for instructions.

## Usage
See [docs/usage.md](docs/usage.md) for details.

## Architecture
See [architecture](docs/architecture.md) for an overview.


## Deployment
Push to a public GitHub repository.
Follow `docs/setup.md` for local or cloud deployment instructions using Docker Compose.

## Scalability
Use Chroma for efficient vector search.
Modular design allows adding new agents/tools.
Docker enables horizontal scaling.