"""Document processing module for PDF ingestion"""
import os
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process PDF documents and extract text"""
    
    def __init__(self, documents_path: str):
        self.documents_path = Path(documents_path)
        self.documents_path.mkdir(parents=True, exist_ok=True)
    
    def load_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            logger.info(f"Successfully loaded PDF: {file_path}")
            return text
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {str(e)}")
            raise
    
    def load_all_documents(self) -> List[Dict[str, str]]:
        """Load all PDF documents from the documents directory"""
        documents = []
        
        if not self.documents_path.exists():
            logger.warning(f"Documents directory does not exist: {self.documents_path}")
            return documents
        
        for pdf_file in self.documents_path.glob("*.pdf"):
            try:
                text = self.load_pdf(str(pdf_file))
                documents.append({
                    "content": text,
                    "source": pdf_file.name,
                    "path": str(pdf_file)
                })
                logger.info(f"Loaded document: {pdf_file.name}")
            except Exception as e:
                logger.error(f"Failed to load {pdf_file.name}: {str(e)}")
        
        return documents
    
    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - chunk_overlap
        
        return chunks

