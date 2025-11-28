"""Main pipeline for document ingestion and RAG setup"""
import logging
import mlflow
from pathlib import Path
from typing import List, Dict
from src.config import settings
from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingGenerator
from src.vector_store import FAISSVectorStore
from src.rag_agent import RAGAgent

logger = logging.getLogger(__name__)


class MLOpsPipeline:
    """Main MLOps pipeline for document ingestion and RAG setup"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor(settings.DOCUMENTS_PATH)
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = None
        self.rag_agent = None
        
        # Initialize MLflow
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
    
    def ingest_documents(self) -> Dict:
        """Ingest documents, create embeddings, and build vector store"""
        with mlflow.start_run(run_name="document_ingestion"):
            logger.info("Starting document ingestion pipeline")
            
            # Load documents
            documents = self.document_processor.load_all_documents()
            
            if not documents:
                logger.warning("No documents found to ingest")
                return {
                    "status": "warning",
                    "message": "No documents found",
                    "documents_processed": 0
                }
            
            # Chunk documents
            all_chunks = []
            all_metadatas = []
            
            for doc in documents:
                chunks = self.document_processor.chunk_text(
                    doc["content"],
                    chunk_size=settings.CHUNK_SIZE,
                    chunk_overlap=settings.CHUNK_OVERLAP
                )
                
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_metadatas.append({
                        "content": chunk,
                        "source": doc["source"],
                        "chunk_index": i,
                        "path": doc["path"]
                    })
            
            logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
            
            # Generate embeddings
            logger.info("Generating embeddings...")
            embeddings = self.embedding_generator.generate_embeddings(all_chunks)
            
            # Create vector store
            import numpy as np
            embedding_dim = len(embeddings[0])
            self.vector_store = FAISSVectorStore(
                dimension=embedding_dim,
                index_path=settings.FAISS_INDEX_PATH
            )
            
            # Add to vector store
            embeddings_array = np.array(embeddings).astype('float32')
            self.vector_store.add_documents(embeddings_array, all_metadatas)
            self.vector_store.save()
            
            # Log to MLflow
            mlflow.log_param("num_documents", len(documents))
            mlflow.log_param("num_chunks", len(all_chunks))
            mlflow.log_param("chunk_size", settings.CHUNK_SIZE)
            mlflow.log_param("chunk_overlap", settings.CHUNK_OVERLAP)
            mlflow.log_param("embedding_model", settings.EMBEDDING_MODEL)
            mlflow.log_metric("total_vectors", self.vector_store.index.ntotal)
            
            logger.info("Document ingestion completed successfully")
            
            return {
                "status": "success",
                "documents_processed": len(documents),
                "chunks_created": len(all_chunks),
                "vectors_stored": self.vector_store.index.ntotal
            }
    
    def initialize_rag_agent(self):
        """Initialize the RAG agent"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Run ingest_documents() first.")
        
        logger.info("Initializing RAG agent...")
        self.rag_agent = RAGAgent(
            vector_store=self.vector_store,
            use_quantization=settings.USE_QUANTIZATION
        )
        logger.info("RAG agent initialized successfully")
    
    def query(self, question: str, log_to_mlflow: bool = True) -> Dict:
        """Process a query through the RAG agent"""
        if self.rag_agent is None:
            self.initialize_rag_agent()
        
        if log_to_mlflow:
            with mlflow.start_run(run_name="query_processing", nested=True):
                mlflow.log_param("query", question)
                result = self.rag_agent.query(question)
                mlflow.log_metric("num_sources", len(result.get("sources", [])))
                mlflow.log_metric("confidence", result.get("confidence", 0.0))
                return result
        else:
            return self.rag_agent.query(question)

