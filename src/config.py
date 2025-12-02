"""Configuration settings for the LLM Customer Support Agent"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # MLflow Configuration
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MLFLOW_EXPERIMENT_NAME: str = "llm-customer-support"
    
    # Model Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.1"  # Can use OpenAI API as alternative
    USE_OPENAI: bool = False
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Vector DB Configuration
    VECTOR_DB_TYPE: str = "faiss"  # Options: faiss, pinecone, weaviate
    VECTOR_DB_PATH: str = "./data/vector_db"
    FAISS_INDEX_PATH: str = "./data/faiss_index"
    
    # Pinecone Configuration (if using)
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX_NAME: Optional[str] = None
    
    # Document Processing
    DOCUMENTS_PATH: str = "./data/documents"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # RAG Configuration
    TOP_K_RETRIEVAL: int = 5
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000  # Increased for more complete answers
    
    # Guardrails
    ENABLE_GUARDRAILS: bool = True
    REBUFF_API_KEY: Optional[str] = None
    MAX_QUERY_LENGTH: int = 500
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Model Optimization
    USE_QUANTIZATION: bool = True
    QUANTIZATION_BITS: int = 8
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

