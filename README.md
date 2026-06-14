# 📚 Project Overview

This repository is a **learning sandbox** that walks through four major topics in modern LLM‑centric development:

- **LangChain** – core agents, tool binding, middleware, structured output.
- **LangGraph** – graph‑based state management and orchestration.
- **RAG** (Retrieval‑Augmented Generation) – embedding creation, vector stores, and query pipelines.
- **MCP** – Multi‑Channel Protocol integration (example utilities for connecting external services).

## 🎯 Typical End‑to‑End Pipeline

```mermaid
flowchart TD
    A[Load .env & Config] --> B[Init Chat Model]
    B --> C[Define Tools & Bind]
    C --> D[Create Agent / LangGraph StateGraph]
    D --> E[User Prompt]
    E --> F[Agent Loop]
    F --> G{Middleware?}
    G -->|Yes| H[Run Middleware Hooks]
    H --> I[Model Call]
    I --> J["Tool Calls (if any)"]
    J --> K["Post-Processing (Structured Output)"]
    G -->|No| I
    K --> L[Return Final Message]
    L --> M[Display to User]
```

## 📂 Repository Layout

- `langchain/` – notebooks `01_…` to `06_…` covering core LangChain concepts.
- `langGraph/` – examples of state graphs and node/edge definitions.
- `RAG/` – embedding notebooks, vector store setup, retrieval pipelines.
- `MCP/` – configuration and usage examples for the Multi‑Channel Protocol.
- `doc/` – generated architecture & flow diagrams (see `architecture.md`).

## 📄 Navigation

- [LangChain README](./langchain/README.md)
- [LangGraph README](./langGraph/README.md)
- [RAG README](./RAG/README.md)
- [MCP README](./MCP/README.md)

---

*This README serves as a quick‑reference study guide. Each sub‑directory contains a detailed README with topic‑specific explanations and diagrams.*
