# LLM Customer Support Agent - Full MLOps Pipeline

A production-ready LLM customer support agent that answers questions using a company's documentation, with full MLOps capabilities: tracking (MLflow), vector search, guardrails, API, UI, Docker, and cloud deployment.

## 🏗️ Architecture

```
User → Streamlit UI → FastAPI Backend → RAG Pipeline → Vector DB + LLM → Response
                                    ↓
                              MLflow Tracking
```

## ✨ Features

- **Document Ingestion**: Process PDF documents and create embeddings
- **Vector Search**: FAISS-based semantic search for document retrieval
- **RAG Agent**: Retrieval Augmented Generation using LangChain
- **Guardrails**: Query validation and safety checks (Pydantic + Rebuff)
- **MLflow Integration**: Experiment tracking and model registry
- **FastAPI Backend**: Production-ready REST API
- **Streamlit UI**: User-friendly web interface
- **Docker Support**: Containerized deployment
- **CI/CD**: GitHub Actions pipeline
- **AWS Deployment**: Terraform and deployment scripts
- **Model Optimization**: BitsAndBytes quantization support

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **LLM Framework**: LangChain
- **Models**: HuggingFace Transformers (Mistral, Llama) or OpenAI API
- **Embeddings**: Sentence Transformers
- **Vector DB**: FAISS (local) or Pinecone/Weaviate (cloud)
- **MLOps**: MLflow
- **Backend**: FastAPI
- **UI**: Streamlit
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Cloud**: AWS (ECS, ECR)

## 📦 Installation

### Prerequisites

- Python 3.10+
- Docker and Docker Compose (optional)
- AWS CLI (for deployment)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd testrepo
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Create data directories**:
   ```bash
   mkdir -p data/documents data/faiss_index data/vector_db
   ```

## 🚀 Quick Start

### 1. Add Documents

Place your PDF documents in `data/documents/` directory.

### 2. Ingest Documents

```bash
python scripts/ingest_documents.py
```

This will:
- Load all PDF documents
- Create text chunks
- Generate embeddings
- Store in FAISS vector database
- Log to MLflow

### 3. Start the API

```bash
python api/main.py
```

Or using uvicorn:
```bash
uvicorn api.main:app --reload
```

API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 4. Start Streamlit UI

```bash
streamlit run streamlit_app.py
```

UI will be available at `http://localhost:8501`

### 5. Test Queries

```bash
python scripts/test_query.py
```

Or use the Streamlit UI to interact with the agent.

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This starts:
- FastAPI backend on port 8000
- Streamlit UI on port 8501
- MLflow tracking server on port 5000

### Using Docker

```bash
# Build image
docker build -t llm-support-agent .

# Run API
docker run -p 8000:8000 -v $(pwd)/data:/app/data llm-support-agent

# Run Streamlit
docker run -p 8501:8501 -v $(pwd)/data:/app/data llm-support-agent streamlit run streamlit_app.py
```

## 📡 API Endpoints

### `GET /`
Root endpoint with API information

### `GET /health`
Health check endpoint

### `POST /query`
Query the RAG agent
```json
{
  "question": "What is the return policy?",
  "log_to_mlflow": true
}
```

### `POST /ingest`
Trigger document ingestion

### `POST /upload`
Upload a PDF document

### `GET /stats`
Get pipeline statistics

## 🔒 Guardrails

The system includes multiple layers of guardrails:

1. **Pydantic Validation**: Query format and length validation
2. **Pattern Detection**: Detects unsafe query patterns
3. **Rebuff Integration**: Advanced injection attack detection (optional)

## 📊 MLflow Tracking

MLflow tracks:
- Document ingestion metrics
- Query processing metrics
- Model performance
- Experiment parameters

Access MLflow UI:
```bash
mlflow ui
# Or via Docker Compose at http://localhost:5000
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov=api --cov-report=html
```

## 🚢 AWS Deployment

### Prerequisites

1. AWS CLI configured
2. Docker installed
3. Terraform installed (optional)

### Deploy with Script

```bash
chmod +x aws/deploy.sh
./aws/deploy.sh
```

### Deploy with Terraform

```bash
cd aws/terraform
terraform init
terraform plan
terraform apply
```

## 🔄 CI/CD Pipeline

GitHub Actions workflow includes:
- Code linting (flake8, black)
- Unit tests
- Docker image building
- AWS deployment (on main branch)

Configure secrets in GitHub:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `DOCKER_USERNAME` (optional)
- `DOCKER_PASSWORD` (optional)

## 📁 Project Structure

```
testrepo/
├── src/                    # Core source code
│   ├── __init__.py
│   ├── config.py           # Configuration
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── guardrails.py
│   ├── rag_agent.py
│   └── pipeline.py
├── api/                    # FastAPI backend
│   └── main.py
├── scripts/                # Utility scripts
│   ├── ingest_documents.py
│   └── test_query.py
├── tests/                  # Unit tests
├── aws/                    # AWS deployment
│   ├── deploy.sh
│   └── terraform/
├── data/                   # Data directory
│   ├── documents/          # PDF documents
│   ├── faiss_index/        # FAISS index
│   └── vector_db/          # Vector database
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Configuration

Key configuration options in `.env`:

- `EMBEDDING_MODEL`: HuggingFace embedding model
- `LLM_MODEL`: Local LLM model (or use OpenAI)
- `USE_OPENAI`: Use OpenAI API instead of local model
- `VECTOR_DB_TYPE`: Vector database type (faiss/pinecone/weaviate)
- `ENABLE_GUARDRAILS`: Enable/disable guardrails
- `USE_QUANTIZATION`: Enable 8-bit quantization

## 🎯 Usage Examples

### Python API

```python
from src.pipeline import MLOpsPipeline

pipeline = MLOpsPipeline()
pipeline.ingest_documents()
pipeline.initialize_rag_agent()

result = pipeline.query("What is the return policy?")
print(result["answer"])
```

### REST API

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the return policy?", "log_to_mlflow": true}'
```

## 🔧 Model Optimization

The system supports:
- **8-bit Quantization**: Reduces memory usage (requires CUDA)
- **Model Caching**: Caches models for faster startup
- **Batch Processing**: Efficient batch embedding generation

## 📝 Notes

- For local LLM models, ensure you have sufficient GPU memory (8GB+ recommended)
- For OpenAI API, set `USE_OPENAI=true` and provide `OPENAI_API_KEY`
- FAISS index is stored locally; for production, consider Pinecone or Weaviate
- MLflow tracking requires MLflow server running (included in docker-compose)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License

## 🙏 Acknowledgments

- LangChain for RAG framework
- HuggingFace for models and transformers
- MLflow for experiment tracking
- FAISS for vector search

---

**Built with ❤️ for production MLOps**
