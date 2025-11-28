"""FastAPI backend for the LLM Customer Support Agent"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import logging
import uvicorn
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import settings
from src.pipeline import MLOpsPipeline
from src.guardrails import Guardrails

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LLM Customer Support Agent API",
    description="Production-ready MLOps LLM pipeline for customer support",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline and guardrails
pipeline = MLOpsPipeline()
guardrails = Guardrails(settings.ENABLE_GUARDRAILS)

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    log_to_mlflow: bool = True

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    vector_store_ready: bool
    rag_agent_ready: bool

@app.on_event("startup")
async def startup_event():
    """Initialize pipeline on startup"""
    logger.info("Starting up API server...")
    try:
        # Try to load existing vector store
        from src.vector_store import FAISSVectorStore
        import numpy as np
        embedding_dim = 384  # Default for all-MiniLM-L6-v2
        pipeline.vector_store = FAISSVectorStore(
            dimension=embedding_dim,
            index_path=settings.FAISS_INDEX_PATH
        )
        
        if pipeline.vector_store.index.ntotal > 0:
            pipeline.initialize_rag_agent()
            logger.info("Pipeline initialized with existing vector store")
        else:
            logger.info("Vector store is empty. Please ingest documents first.")
    except Exception as e:
        logger.warning(f"Could not initialize pipeline on startup: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LLM Customer Support Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    vector_store_ready = pipeline.vector_store is not None and pipeline.vector_store.index.ntotal > 0
    rag_agent_ready = pipeline.rag_agent is not None
    
    return HealthResponse(
        status="healthy" if (vector_store_ready and rag_agent_ready) else "initializing",
        vector_store_ready=vector_store_ready,
        rag_agent_ready=rag_agent_ready
    )

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Query the RAG agent"""
    try:
        # Guardrails check
        validation = guardrails.validate_query(request.question)
        if not validation["is_valid"] or not validation["is_safe"]:
            raise HTTPException(
                status_code=400,
                detail=f"Query validation failed: {validation.get('error', 'Unsafe query detected')}"
            )
        
        # Process query
        result = pipeline.query(request.question, log_to_mlflow=request.log_to_mlflow)
        
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        return QueryResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            confidence=result.get("confidence", 0.0),
            error=result.get("error")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_documents():
    """Trigger document ingestion"""
    try:
        result = pipeline.ingest_documents()
        if result["status"] == "success":
            pipeline.initialize_rag_agent()
        return result
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document"""
    try:
        # Save uploaded file
        documents_path = Path(settings.DOCUMENTS_PATH)
        documents_path.mkdir(parents=True, exist_ok=True)
        
        file_path = documents_path / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Uploaded document: {file.filename}")
        
        # Re-ingest documents
        result = pipeline.ingest_documents()
        if result["status"] == "success":
            pipeline.initialize_rag_agent()
        
        return {
            "status": "success",
            "message": f"Document {file.filename} uploaded and processed",
            "result": result
        }
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get pipeline statistics"""
    try:
        stats = {}
        if pipeline.vector_store:
            stats["vector_store"] = pipeline.vector_store.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )

