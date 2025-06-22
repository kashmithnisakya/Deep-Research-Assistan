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
   openai_api_key=your_openai_api_key
   openai_api_key=your_serper_api_key
   ```
3. nstall dependencies (if running locally):
   ```bash
   pip install -r requirements.txt
   ```
4. Build and run with Docker Compose:
    ```bash
    docker-compose up --build
    ```
5. Access the application:
   Open your browser and go to `http://localhost:8501`.
## Note 
* Run tests with pytest tests/.
