"""RAG (Retrieval Augmented Generation) agent using LangChain"""
import logging
import numpy as np
from typing import List, Dict, Optional
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS as LangChainFAISS
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
import torch
from src.config import settings
from src.vector_store import FAISSVectorStore
from src.embeddings import EmbeddingGenerator
from src.guardrails import Guardrails

logger = logging.getLogger(__name__)


class RAGAgent:
    """RAG agent for question answering using retrieved documents"""
    
    def __init__(self, vector_store: FAISSVectorStore, use_quantization: bool = True):
        self.vector_store = vector_store
        self.guardrails = Guardrails(settings.ENABLE_GUARDRAILS)
        self.embedding_generator = EmbeddingGenerator()
        
        # Initialize LLM
        if settings.USE_OPENAI:
            from langchain.llms import OpenAI
            self.llm = OpenAI(
                model_name=settings.OPENAI_MODEL,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
        else:
            self.llm = self._load_local_llm(use_quantization)
        
        # Initialize LangChain FAISS vector store wrapper
        self.langchain_vectorstore = self._create_langchain_vectorstore()
        
        # Create RAG chain
        self.qa_chain = self._create_qa_chain()
        
        logger.info("RAG Agent initialized successfully")
    
    def _load_local_llm(self, use_quantization: bool = True):
        """Load local LLM with optional quantization"""
        model_name = settings.LLM_MODEL
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Loading LLM: {model_name} on {device}")
        
        try:
            # Configure quantization if enabled
            quantization_config = None
            if use_quantization and device == "cuda":
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_threshold=6.0
                )
                logger.info("Using 8-bit quantization")
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=quantization_config,
                device_map="auto" if device == "cuda" else None,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            
            # Create pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                do_sample=True,
                device=0 if device == "cuda" else -1
            )
            
            llm = HuggingFacePipeline(pipeline=pipe)
            logger.info("Local LLM loaded successfully")
            return llm
            
        except Exception as e:
            logger.error(f"Error loading local LLM: {str(e)}")
            logger.warning("Falling back to a simpler model or API-based LLM")
            # Fallback to a smaller model
            try:
                from langchain.llms import HuggingFaceHub
                llm = HuggingFaceHub(
                    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
                    model_kwargs={"temperature": settings.TEMPERATURE, "max_length": settings.MAX_TOKENS}
                )
                return llm
            except:
                raise Exception("Could not load LLM. Please check model configuration or use OpenAI API.")
    
    def _create_langchain_vectorstore(self):
        """Create LangChain FAISS vector store from our custom vector store"""
        # This is a simplified wrapper - in production, you'd convert the FAISS index
        # For now, we'll use LangChain's FAISS with embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        
        # Create a temporary FAISS index using LangChain
        # In production, you'd load from the existing index
        return None  # Will be set up during document ingestion
    
    def _create_qa_chain(self):
        """Create the QA chain with custom prompt"""
        prompt_template = """Use the following pieces of context to answer the question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Be concise and accurate.

Context: {context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # For now, return a simple chain structure
        # In production, this would use LangChain's RetrievalQA
        return {
            "prompt": PROMPT,
            "top_k": settings.TOP_K_RETRIEVAL
        }
    
    def query(self, question: str) -> Dict:
        """Process a query and return answer with sources"""
        # Guardrails check
        if self.guardrails.should_refuse_query(question):
            return {
                "answer": "I cannot process this query due to safety concerns.",
                "sources": [],
                "error": "Query failed guardrails validation"
            }
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embedding(question)
            
            # Retrieve relevant documents
            results = self.vector_store.search(
                np.array(query_embedding),
                k=settings.TOP_K_RETRIEVAL
            )
            
            if not results:
                return {
                    "answer": "I couldn't find relevant information to answer your question.",
                    "sources": [],
                    "error": None
                }
            
            # Extract context from retrieved documents
            context = "\n\n".join([doc["content"] for doc, _ in results])
            
            # Generate answer using LLM
            if settings.USE_OPENAI:
                from langchain.llms import OpenAI
                llm = OpenAI(temperature=settings.TEMPERATURE)
            else:
                llm = self.llm
            
            # Simple answer generation (in production, use full LangChain chain)
            prompt = f"""Context: {context}\n\nQuestion: {question}\n\nAnswer:"""
            
            try:
                answer = llm(prompt)
            except Exception as e:
                logger.error(f"LLM generation error: {str(e)}")
                # Fallback: return top retrieved document
                answer = results[0][0]["content"][:500] + "..."
            
            # Extract sources
            sources = [doc["source"] for doc, _ in results]
            
            return {
                "answer": answer.strip(),
                "sources": sources,
                "confidence": 1.0 - (results[0][1] / 10.0) if results else 0.0,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "answer": "I encountered an error while processing your question.",
                "sources": [],
                "error": str(e)
            }

