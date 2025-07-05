# RAG + Local LLM Chat Application

A Retrieval-Augmented Generation (RAG) system that enables question-answering over documents using local language models. This project combines the power of Chroma vector database, Ollama's local LLM, and FastAPI to create a document-based question-answering system.

## Features

- **Document Processing**: Automatically processes PDF files into searchable chunks
- **Local LLM Integration**: Uses Ollama's local language models for responses
- **Vector Search**: Implements semantic search using Chroma vector database
- **REST API**: Provides a FastAPI-based interface for document queries
- **Docker Support**: Easy deployment using Docker and docker-compose

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- Ollama with the `deepseek-r1:14b` model installed

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd RAG+LLM
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Ollama is running with the required model:
   ```bash
   ollama pull deepseek-r1:14b
   ```

## Usage

### Adding Documents

1. Place your PDF files in the `data` directory
2. Process the PDFs into the Chroma database:
   ```bash
   python createDB.py
   ```

### Running the API

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

- **POST /ask**
  - Request body:
    ```json
    {
        "question": "Your question here",
        "file_name": "your_document.pdf"
    }
    ```
  - Response:
    ```json
    {
        "res": "The answer to your question in bullet points"
    }
    ```

## Docker Deployment

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

The service will be available at `http://localhost:8000`

## Project Structure

- `main.py`: FastAPI application and API endpoints
- `query.py`: Handles RAG queries and LLM interactions
- `createDB.py`: Processes PDFs and builds the Chroma database
- `local_embedding_function.py`: Custom embedding function for Chroma
- `data/`: Directory for storing PDF documents
- `chroma/`: Chroma database storage
- `Dockerfile` & `docker-compose.yml`: Container configuration
- `requirements.txt`: Python dependencies

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [LangChain](https://python.langchain.com/) for the LLM framework
- [Chroma](https://www.trychroma.com/) for vector storage
- [Ollama](https://ollama.ai/) for local LLM support
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
