# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f
```

Services will be available at:
- FastAPI: http://localhost:8000
- Streamlit UI: http://localhost:8501
- MLflow: http://localhost:5000

### Option 2: Local Setup

1. **Run setup script**:
   ```bash
   ./setup.sh
   ```

2. **Add PDF documents**:
   ```bash
   # Place your PDF files in data/documents/
   cp your-document.pdf data/documents/
   ```

3. **Ingest documents**:
   ```bash
   source venv/bin/activate
   python scripts/ingest_documents.py
   ```

4. **Start the API**:
   ```bash
   python api/main.py
   ```

5. **Start the UI** (in another terminal):
   ```bash
   streamlit run streamlit_app.py
   ```

## 📝 Example Usage

### Using the Streamlit UI

1. Open http://localhost:8501
2. Upload a PDF document (optional, if not already ingested)
3. Ask questions like:
   - "What is the return policy?"
   - "How do I contact customer support?"
   - "What are the shipping options?"

### Using the API

```bash
# Query the agent
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the return policy?",
    "log_to_mlflow": true
  }'
```

### Using Python

```python
from src.pipeline import MLOpsPipeline

# Initialize pipeline
pipeline = MLOpsPipeline()

# Ingest documents (if not already done)
pipeline.ingest_documents()

# Initialize RAG agent
pipeline.initialize_rag_agent()

# Query
result = pipeline.query("What is the return policy?")
print(result["answer"])
```

## 🔧 Configuration

Edit `.env` file to configure:
- Model selection (local vs OpenAI)
- Vector database settings
- Guardrails options
- API settings

## 🐛 Troubleshooting

### API not starting
- Check if port 8000 is available
- Ensure dependencies are installed: `pip install -r requirements.txt`

### No documents found
- Place PDF files in `data/documents/` directory
- Run `python scripts/ingest_documents.py`

### Model loading errors
- For local models, ensure sufficient GPU memory (8GB+)
- Consider using OpenAI API: set `USE_OPENAI=true` in `.env`
- Or use a smaller model

### MLflow not tracking
- Start MLflow server: `mlflow ui` or use docker-compose
- Check `MLFLOW_TRACKING_URI` in `.env`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the API documentation at http://localhost:8000/docs
- Explore MLflow experiments at http://localhost:5000

