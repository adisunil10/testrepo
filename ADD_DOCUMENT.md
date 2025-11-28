# Adding Your RBC Annual Report

## ✅ Yes, You Can Use It!

RBC Investor Services' annual report is a **perfect document** for testing your LLM Customer Support Agent because:

1. **Publicly Available**: Annual reports are meant to be public documents
2. **Rich Content**: Contains company information, policies, services, financial data
3. **Real-World**: Represents actual business documentation
4. **Comprehensive**: Covers multiple topics that customers might ask about

## 📥 How to Add the Document

### Step 1: Place the PDF

Copy your RBC annual report PDF to the documents folder:

```bash
# If the PDF is in your Downloads folder
cp ~/Downloads/RBC_Investor_Services_Annual_Report_2024.pdf data/documents/

# Or manually:
# 1. Open Finder
# 2. Navigate to: testrepo/data/documents/
# 3. Copy/paste your PDF file there
```

### Step 2: Verify It's There

```bash
ls -la data/documents/
```

You should see your PDF file listed.

### Step 3: Ingest the Document

```bash
python scripts/ingest_documents.py
```

This will:
- Extract text from the PDF
- Create embeddings
- Store in the vector database
- Log to MLflow

### Step 4: Test It!

Once ingested, you can ask questions like:

- "What services does RBC Investor Services offer?"
- "What was the company's performance in 2024?"
- "What are the key highlights from the annual report?"
- "What are the company's strategic priorities?"
- "What is the company's approach to risk management?"

## 🎯 Why Annual Reports Are Great for Testing

Annual reports typically contain:

- ✅ **Company Overview**: Services, products, business model
- ✅ **Financial Information**: Performance metrics, results
- ✅ **Strategic Priorities**: Future plans and direction
- ✅ **Risk Management**: Policies and procedures
- ✅ **Governance**: Corporate structure and policies
- ✅ **Market Information**: Industry context and trends

All of these are perfect for testing your customer support agent!

## 💡 Pro Tips

1. **Multiple Documents**: You can add multiple PDFs - the system will process all of them
2. **Mix Document Types**: Combine the annual report with other documents (policies, FAQs, etc.)
3. **Test Various Questions**: Try questions about:
   - Services offered
   - Financial performance
   - Company strategy
   - Risk management
   - Market position

## 🔍 Example Queries to Test

Once your document is ingested, try these:

```python
# Using Python
from src.pipeline import MLOpsPipeline

pipeline = MLOpsPipeline()
pipeline.ingest_documents()
pipeline.initialize_rag_agent()

# Test queries
queries = [
    "What services does RBC Investor Services provide?",
    "What were the key financial highlights in 2024?",
    "What are the company's strategic priorities?",
    "How does the company manage risk?",
    "What is the company's market position?"
]

for query in queries:
    result = pipeline.query(query)
    print(f"\nQ: {query}")
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")
```

Or use the Streamlit UI or API:

```bash
# Using API
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What services does RBC Investor Services provide?", "log_to_mlflow": true}'
```

## ⚠️ Note on Copyright

- Annual reports are **publicly distributed documents** meant for shareholders and the public
- Using them for **testing and development** purposes is typically fine
- For **production use**, ensure you comply with any terms of use
- The document is being used for **internal testing/development**, not redistribution

## ✅ Next Steps

1. **Add the PDF**: Place it in `data/documents/`
2. **Ingest**: Run `python scripts/ingest_documents.py`
3. **Start Services**: 
   ```bash
   python api/main.py  # Terminal 1
   streamlit run streamlit_app.py  # Terminal 2
   ```
4. **Test Queries**: Use the UI or API to ask questions about the report

---

**Your RBC annual report is an excellent choice for testing! It's comprehensive, real-world, and contains the kind of information a customer support agent would need to answer.**
