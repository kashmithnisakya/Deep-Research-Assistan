# Setup Instructions

## Prerequisites
- Docker and Docker Compose
- OpenAI API key
- Serper API key (for web search)

## Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/deep_research_assistant.git
   cd deep_research_assistant
   ```
2. Create a `.env` file in the root directory with the following content:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key
   ```
3. Build and run with Docker Compose:
    ```bash
    docker-compose up --build
    ```
4. Access the application:
   Open your browser and go to `http://localhost:8501`.
## Note 
* Ensure the vector store (data/vector_store) is pre-populated with documents for retrieval.
* Run tests with pytest tests/.
