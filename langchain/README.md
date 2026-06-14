# 📘 LangChain Study Guide

## Overview
This folder contains notebooks that walk through the core **LangChain** concepts used in this project:
- **Agents** – creation via `create_agent`.
- **Tool Binding** – exposing Python functions to the LLM.
- **Middleware** – hooks to intercept model calls and tool execution.
- **Structured Output** – using Pydantic, TypedDict, and dataclasses.

## Notebook Flow
```mermaid
flowchart TD
    A[01_lanchain_intro.ipynb] --> B[02_model_integration.ipynb]
    B --> C[03_tools.ipynb]
    C --> D[04_messages.ipynb]
    D --> E[05_structured_output.ipynb]
    E --> F[06_middleware.ipynb]
```

### 1. Agent Creation
```mermaid
flowchart LR
    Model[Chat Model] -->|bind_tools| Tools[Tool List]
    Model -->|system_prompt| Prompt[System Prompt]
    Model --> Agent[Compiled Agent (StateGraph)]
    Agent -->|invoke| User[User Message]
```

### 2. Tool Definition & Binding
```mermaid
flowchart TB
    Func[Python Function] -->|type hints| Tool[LangChain Tool]
    Tool --> Model.bind_tools([ ... ])
```

### 3. Middleware Hooks
```mermaid
flowchart TD
    subgraph Middleware
        BM[before_model]
        AM[after_model]
        BT[before_tool]
        AT[after_tool]
    end
    BM --> ModelCall
    ModelCall --> AM
    BT --> ToolExec
    ToolExec --> AT
```

### 4. Structured Output
```mermaid
flowchart LR
    ModelOutput --> SO[Structured Output]
    SO -->|Pydantic| PydModel[BaseModel]
    SO -->|TypedDict| TDict[TypedDict]
    SO -->|Dataclass| DClass[Dataclass]
```

---

*Each notebook contains runnable examples. Refer to the code cells for concrete implementations.*
