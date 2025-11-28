"""Tests for document processor"""
import pytest
from pathlib import Path
from src.document_processor import DocumentProcessor
import tempfile
import os


def test_chunk_text():
    """Test text chunking"""
    processor = DocumentProcessor(documents_path="./data/documents")
    
    text = "a" * 5000
    chunks = processor.chunk_text(text, chunk_size=1000, chunk_overlap=200)
    
    assert len(chunks) > 0
    assert all(len(chunk) <= 1000 for chunk in chunks)


def test_load_all_documents_empty_dir():
    """Test loading documents from empty directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        processor = DocumentProcessor(documents_path=tmpdir)
        documents = processor.load_all_documents()
        assert len(documents) == 0

