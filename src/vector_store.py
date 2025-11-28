"""Vector database management using FAISS"""
import os
import pickle
import logging
from typing import List, Dict, Tuple
import faiss
import numpy as np
from pathlib import Path
from src.config import settings

logger = logging.getLogger(__name__)


class FAISSVectorStore:
    """FAISS-based vector store for document embeddings"""
    
    def __init__(self, dimension: int = 384, index_path: str = None):
        self.dimension = dimension
        self.index_path = Path(index_path or settings.FAISS_INDEX_PATH)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []  # Store document metadata alongside vectors
        self._load_index()
    
    def _load_index(self):
        """Load existing index if available"""
        index_file = self.index_path / "index.faiss"
        metadata_file = self.index_path / "metadata.pkl"
        
        if index_file.exists() and metadata_file.exists():
            try:
                self.index = faiss.read_index(str(index_file))
                with open(metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
                logger.info(f"Loaded existing index with {self.index.ntotal} vectors")
            except Exception as e:
                logger.warning(f"Could not load existing index: {str(e)}")
                self.index = faiss.IndexFlatL2(self.dimension)
        else:
            logger.info("Creating new FAISS index")
    
    def add_documents(self, embeddings: np.ndarray, metadatas: List[Dict]):
        """Add document embeddings to the index"""
        if len(embeddings) != len(metadatas):
            raise ValueError("Number of embeddings must match number of metadatas")
        
        # Convert to numpy array if needed
        if not isinstance(embeddings, np.ndarray):
            embeddings = np.array(embeddings).astype('float32')
        
        # Ensure correct dimension
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} doesn't match index dimension {self.dimension}")
        
        self.index.add(embeddings)
        self.metadata.extend(metadatas)
        logger.info(f"Added {len(embeddings)} documents to index. Total: {self.index.ntotal}")
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar documents"""
        if not isinstance(query_embedding, np.ndarray):
            query_embedding = np.array([query_embedding]).astype('float32')
        
        if query_embedding.shape[1] != self.dimension:
            raise ValueError(f"Query embedding dimension {query_embedding.shape[1]} doesn't match index dimension {self.dimension}")
        
        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(distance)))
        
        return results
    
    def save(self):
        """Save index and metadata to disk"""
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        index_file = self.index_path / "index.faiss"
        metadata_file = self.index_path / "metadata.pkl"
        
        faiss.write_index(self.index, str(index_file))
        with open(metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)
        
        logger.info(f"Saved index with {self.index.ntotal} vectors to {self.index_path}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "index_path": str(self.index_path)
        }

