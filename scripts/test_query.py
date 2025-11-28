"""Script to test queries against the RAG agent"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.pipeline import MLOpsPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to test queries"""
    pipeline = MLOpsPipeline()
    
    # Try to load existing vector store
    from src.vector_store import FAISSVectorStore
    import numpy as np
    
    embedding_dim = 384  # Default for all-MiniLM-L6-v2
    pipeline.vector_store = FAISSVectorStore(
        dimension=embedding_dim,
        index_path="./data/faiss_index"
    )
    
    if pipeline.vector_store.index.ntotal == 0:
        logger.error("Vector store is empty. Please run ingest_documents.py first.")
        return
    
    pipeline.initialize_rag_agent()
    
    # Test queries
    test_queries = [
        "What is the return policy?",
        "How do I contact customer support?",
        "What are the shipping options?"
    ]
    
    for query in test_queries:
        logger.info(f"\n{'='*50}")
        logger.info(f"Query: {query}")
        logger.info(f"{'='*50}")
        
        result = pipeline.query(query, log_to_mlflow=False)
        
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Sources: {result.get('sources', [])}")
        logger.info(f"Confidence: {result.get('confidence', 0.0):.2%}")
        
        if result.get('error'):
            logger.error(f"Error: {result['error']}")

if __name__ == "__main__":
    main()

