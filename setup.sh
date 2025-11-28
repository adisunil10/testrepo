#!/bin/bash
# Setup script for LLM Customer Support Agent

set -e

echo "🚀 Setting up LLM Customer Support Agent..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/documents
mkdir -p data/faiss_index
mkdir -p data/vector_db
mkdir -p mlruns

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cat > .env << EOF
# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=llm-customer-support

# Model Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.1
USE_OPENAI=false
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo

# Vector DB Configuration
VECTOR_DB_TYPE=faiss
VECTOR_DB_PATH=./data/vector_db
FAISS_INDEX_PATH=./data/faiss_index

# Document Processing
DOCUMENTS_PATH=./data/documents
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# RAG Configuration
TOP_K_RETRIEVAL=5
TEMPERATURE=0.7
MAX_TOKENS=512

# Guardrails
ENABLE_GUARDRAILS=true
REBUFF_API_KEY=
MAX_QUERY_LENGTH=500

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Model Optimization
USE_QUANTIZATION=true
QUANTIZATION_BITS=8
EOF
    echo "✅ .env file created. Please edit it with your configuration."
else
    echo "✅ .env file already exists."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add PDF documents to data/documents/"
echo "2. Run: python scripts/ingest_documents.py"
echo "3. Start API: python api/main.py"
echo "4. Start UI: streamlit run streamlit_app.py"
echo ""
echo "Or use Docker: docker-compose up"

