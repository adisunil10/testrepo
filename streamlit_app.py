"""Streamlit UI for the LLM Customer Support Agent"""
import streamlit as st
import requests
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="LLM Customer Support Agent",
    page_icon="🤖",
    layout="wide"
)

# API endpoint
API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_available" not in st.session_state:
    st.session_state.api_available = False

# Check API health
def check_api_health():
    """Check if API is available"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"API health check failed: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Health Check
    health = check_api_health()
    if health:
        st.session_state.api_available = True
        st.success("✅ API Connected")
        st.json(health)
    else:
        st.session_state.api_available = False
        st.error("❌ API Not Available")
        st.info(f"Make sure the API is running at {API_URL}")
    
    st.divider()
    
    # Document Upload
    st.subheader("📄 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload PDF document",
        type=["pdf"],
        help="Upload a PDF document to add to the knowledge base"
    )
    
    if uploaded_file is not None:
        if st.button("Upload & Process"):
            with st.spinner("Uploading and processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success("✅ Document uploaded and processed!")
                        st.json(response.json())
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error uploading document: {str(e)}")
    
    st.divider()
    
    # Ingest Documents
    if st.button("🔄 Re-ingest Documents"):
        with st.spinner("Ingesting documents..."):
            try:
                response = requests.post(f"{API_URL}/ingest")
                if response.status_code == 200:
                    st.success("✅ Documents ingested!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Stats
    if st.button("📊 View Statistics"):
        try:
            response = requests.get(f"{API_URL}/stats")
            if response.status_code == 200:
                st.json(response.json())
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Main content
st.title("🤖 LLM Customer Support Agent")
st.markdown("Ask questions about your company's documentation and get AI-powered answers!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources if available
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.text(f"• {source}")

# Chat input
if prompt := st.chat_input("Ask a question about your documentation..."):
    if not st.session_state.api_available:
        st.error("⚠️ API is not available. Please start the FastAPI server first.")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": prompt, "log_to_mlflow": True},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result["answer"]
                    sources = result.get("sources", [])
                    confidence = result.get("confidence", 0.0)
                    
                    st.markdown(answer)
                    
                    # Display confidence
                    st.caption(f"Confidence: {confidence:.2%}")
                    
                    # Display sources
                    if sources:
                        with st.expander("📚 Sources"):
                            for source in sources:
                                st.text(f"• {source}")
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "confidence": confidence
                    })
                else:
                    error_msg = f"Error: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
            except Exception as e:
                error_msg = f"Error connecting to API: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Footer
st.divider()
st.caption("Powered by LangChain, HuggingFace, MLflow, and FAISS | Built with FastAPI and Streamlit")

