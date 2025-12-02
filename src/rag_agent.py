"""RAG (Retrieval Augmented Generation) agent using LangChain"""
import logging
import numpy as np
from typing import List, Dict, Optional
from langchain.prompts import PromptTemplate
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
            self.llm = None  # Will use OpenAI API directly
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY must be set when USE_OPENAI=true")
        else:
            self.llm = self._load_local_llm(use_quantization)
        
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
            hf_pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                do_sample=True,
                device=0 if device == "cuda" else -1
            )
            
            logger.info("Local LLM loaded successfully")
            return hf_pipeline
            
        except Exception as e:
            logger.error(f"Error loading local LLM: {str(e)}")
            raise Exception("Could not load local LLM. Please verify model configuration or enable USE_OPENAI.")
    
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
    
    def _generate_openai_response(self, prompt: str) -> str:
        """Generate a response using OpenAI API directly"""
        try:
            import openai
            from openai import OpenAI
            
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant. Always provide complete, well-structured answers that fully address the user's question. Start your responses directly with the answer (don't repeat the question). Use clear paragraphs or bullet points when appropriate. Ensure your answers are never cut off mid-sentence."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
            return response.choices[0].message.content.strip()
        except ImportError:
            raise ImportError("OpenAI package not installed. Install it with: pip install openai")
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def _generate_response(self, llm, prompt: str) -> str:
        """Generate a response from HuggingFace pipeline"""
        result = llm(
            prompt,
            max_new_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
            do_sample=True
        )
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").strip()
        if isinstance(result, str):
            return result.strip()
        return str(result)
    
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
            context_parts = []
            for item in results:
                try:
                    if isinstance(item, tuple) and len(item) >= 1:
                        doc = item[0]
                        if isinstance(doc, dict) and "content" in doc:
                            context_parts.append(doc["content"])
                except (IndexError, TypeError, AttributeError) as e:
                    logger.warning(f"Error extracting context from result: {str(e)}")
                    continue
            
            if not context_parts:
                return {
                    "answer": "I couldn't find relevant information to answer your question from the retrieved documents.",
                    "sources": [],
                    "error": None
                }
            
            context = "\n\n".join(context_parts)
            
            # Generate answer using LLM with improved prompt
            prompt = f"""Based on the following context from company documents, please answer the question completely and clearly.

Context:
{context}

Question: {question}

Instructions:
- Provide a complete answer that fully addresses the question
- Start your answer directly without repeating the question
- Use clear, structured sentences
- If the context doesn't contain sufficient information, clearly state that
- Ensure your answer is complete and not cut off mid-sentence

Answer:"""
            
            try:
                if settings.USE_OPENAI:
                    answer = self._generate_openai_response(prompt)
                else:
                    answer = self._generate_response(self.llm, prompt)
            except Exception as e:
                logger.error(f"LLM generation error: {str(e)}")
                # Fallback: return top retrieved document
                if results and len(results) > 0 and isinstance(results[0], tuple) and len(results[0]) > 0:
                    doc = results[0][0]
                    if isinstance(doc, dict) and "content" in doc:
                        answer = doc["content"][:500] + "..."
                    else:
                        answer = "I found relevant documents but couldn't generate an answer. Please try rephrasing your question."
                else:
                    answer = "I couldn't generate an answer. Please try again."
            
            # Extract sources
            sources = []
            for item in results:
                if isinstance(item, tuple) and len(item) >= 1:
                    doc = item[0]
                    if isinstance(doc, dict) and "source" in doc:
                        sources.append(doc["source"])
            
            # Calculate confidence from distance (lower distance = higher confidence)
            confidence = 0.0
            if results and len(results) > 0:
                try:
                    # results[0] is (metadata_dict, distance)
                    distance = results[0][1]
                    confidence = max(0.0, min(1.0, 1.0 - (distance / 10.0)))
                except (IndexError, TypeError) as e:
                    logger.warning(f"Could not calculate confidence: {str(e)}")
                    confidence = 0.8  # Default confidence
            
            return {
                "answer": answer.strip(),
                "sources": sources,
                "confidence": confidence,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "answer": "I encountered an error while processing your question.",
                "sources": [],
                "error": str(e)
            }

