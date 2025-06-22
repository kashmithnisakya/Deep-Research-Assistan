# Architecture

The Deep Research Assistant is built using a modular, agentic architecture with LangGraph for orchestration. The system consists of:

1. **Research Agent**: Plans and reasons through the query, generating a step-by-step plan and final answer.
2. **Tool Agent**: Executes tools (web search, document retrieval) based on the plan.
3. **Tools**:
   - Web Search: Uses Serper API for real-time web results.
   - Document Retriever: Uses FAISS vector store for local document retrieval.
4. **Workflow**: LangGraph orchestrates the multi-step flow (plan → execute tools → generate answer).
5. **UI**: Streamlit provides a user-friendly interface.
6. **Configuration**: Pydantic manages settings and environment variables.

The system is dockerized for scalability and easy deployment.