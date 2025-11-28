"""Script to ingest documents into the vector store"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.pipeline import MLOpsPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to ingest documents"""
    logger.info("Starting document ingestion...")
    
    pipeline = MLOpsPipeline()
    result = pipeline.ingest_documents()
    
    if result["status"] == "success":
        logger.info("Document ingestion completed successfully!")
        logger.info(f"Processed {result['documents_processed']} documents")
        logger.info(f"Created {result['chunks_created']} chunks")
        logger.info(f"Stored {result['vectors_stored']} vectors")
        
        # Initialize RAG agent
        pipeline.initialize_rag_agent()
        logger.info("RAG agent initialized and ready!")
    else:
        logger.warning(f"Ingestion completed with status: {result['status']}")
        logger.warning(result.get('message', ''))

if __name__ == "__main__":
    main()

