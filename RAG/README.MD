# 📚 RAG (Retrieval‑Augmented Generation) Study Guide

## 🎯 What is RAG?
Retrieval‑Augmented Generation combines **external knowledge retrieval** with **LLM generation**. Instead of relying solely on the model’s internal parameters, we first fetch relevant documents (or vectors) and feed the retrieved context into the LLM, enabling:
- Up‑to‑date factual answers
- Handling large corpora without increasing model size
- Faster inference for domain‑specific queries

## 📂 Repository Structure
```
RAG/
├─ foundation/          # Core notebooks – data loading, embedding creation
│   └─ 03_embedding.ipynb
├─ data/                # Sample PDFs / text files used for embeddings
├─ RAG_pipeline.ipynb   # End‑to‑end retrieval‑generation pipeline
└─ README.MD            # **(You are reading it!)**
```

## 🛠️ Core Components
1. **Document Loaders** – `DirectoryLoader` + `PyMuPDFLoader` to ingest PDFs.
2. **Embedding Model** – any `langchain_community.embeddings` model (e.g., `OpenAIEmbeddings`).
3. **Vector Store** – `FAISS`, `Chroma`, or other similarity index.
4. **Retriever** – `vector_store.as_retriever(k=4)`.
5. **RAG Chain** – `RetrievalQA` or custom chain that:
   - Retrieves docs →
   - Formats a prompt with retrieved snippets →
   - Calls the LLM →
   - Returns a synthesized answer.

## 🔁 Typical RAG Flow
```mermaid
flowchart TD
    A[Load Documents] --> B[Chunk & Clean]
    B --> C[Create Embeddings]
    C --> D[Build Vector Store]
    D --> E[Retriever (k‑nearest neighbours)]
    E --> F[User Query]
    F --> G[Retrieve Relevant Docs]
    G --> H[Prompt Assembly]
    H --> I[LLM Generation]
    I --> J[Answer to User]
```

## 📓 Notebook Walk‑through
### 03_embedding.ipynb (found in `foundation/`)
- **Goal:** Load PDFs from `data/`, generate embeddings, and persist the vector store.
- **Key Steps:**
  1. `DirectoryLoader(path=dir_path, glob='/*.pdf', loader_cls=PyMuPDFLoader)`
  2. `embeddings = OpenAIEmbeddings()` (or any configured model)
  3. `vectorstore = FAISS.from_documents(documents, embeddings)`
  4. `vectorstore.save_local('faiss_index')`
- **Output:** Prints the number of loaded documents and creates a searchable index.

### RAG_pipeline.ipynb
- Demonstrates loading the saved index, creating a `RetrievalQA` chain, and running a query like:
  ```python
  answer = qa.run("What is the purpose of LangChain middleware?")
  print(answer)
  ```
- Showcases **tool integration** – the same LLM used for LangChain agents can be reused for RAG.

## ⚙️ How RAG Interacts with the Rest of the Project
- **LangChain Agents** can call the `Retriever` as a tool, effectively turning a user query into a *knowledge‑enhanced* request.
- **LangGraph** can orchestrate a state graph where the first node performs retrieval and the second node runs generation, allowing multi‑step reasoning.
- **MCP** (Multi‑Channel Protocol) can expose the RAG service over HTTP/WebSocket so external apps can query the knowledge base.

## 📚 Quick Reference Checklist
- ✅ Load & chunk documents
- ✅ Choose an embedding model compatible with your LLM
- ✅ Build & persist a vector store (FAISS/Chroma)
- ✅ Create a retriever (`as_retriever(k=…)`)
- ✅ Wire the retriever into a `RetrievalQA` or custom chain
- ✅ Test with diverse queries to verify relevance

---
*All code snippets are directly runnable from the notebooks in this folder. Feel free to modify the embedding model or vector store to experiment with performance trade‑offs.*
