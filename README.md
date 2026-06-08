# LangChain Quick Reference & Study Guide

This document serves as a comprehensive study guide and quick reference for the topics covered in this repository. It tracks concepts, implementation steps, and code patterns for LangChain model integration, agents, tool calling, streaming, and batching.

---

## Table of Contents
1. [Environment Setup & Installation](#1-environment-setup--installation)
2. [LangChain Agent & Tool Integration](#2-langchain-agent--tool-integration)
3. [Unified Model Initialization (`init_chat_model`)](#3-unified-model-initialization-init_chat_model)
4. [Model Invocations: Invoke, Stream, and Batch](#4-model-invocations-invoke-stream-and-batch)
5. [Key LangChain Message Classes](#5-key-langchain-message-classes)

---

## 1. Environment Setup & Installation

### Project Setup with `uv`
The project uses the `uv` package manager for fast, reliable dependency and virtual environment management.

* **Reference File:** [README.md](file:///f:/WeCloudData/AI/AgenticAI/langchain_ai/README.md)
* **Configuration:** [pyproject.toml](file:///f:/WeCloudData/AI/AgenticAI/langchain_ai/pyproject.toml)

#### Initializing the Environment
```bash
# Initialize a new project
uv init

# Create a virtual environment
uv venv

# Activate the virtual environment (Windows PowerShell)
.venv\Scripts\activate
```

#### Installing Dependencies
Dependencies are listed in [requirements.txt](file:///f:/WeCloudData/AI/AgenticAI/langchain_ai/requirements.txt). Install them using:
```bash
uv add -r requirements.txt
```

### Environment Variables
Credentials and API keys are stored in a local `.env` file and loaded using `dotenv`.

* **Reference File:** [.env](file:///f:/WeCloudData/AI/AgenticAI/langchain_ai/.env)

```env
OPENAI_API_KEY="your_openai_api_key"
GROQ_API_KEY="your_groq_api_key"
GEMINI_API_KEY="your_gemini_api_key"
```

To load these variables into Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
```

---

## 2. LangChain Agent & Tool Integration

* **Reference Notebook:** [01_lanchain_intro.ipynb](file:///f:/WeCloudData/AI/AgenticAI/langchain_ai/langchain/01_lanchain_intro.ipynb)

An agent uses an LLM to decide a sequence of actions. It binds tools (functions) to the model, allowing the model to invoke external resources as needed.

### Tool Definition
In LangChain, a Python function can be converted into a tool simply by writing standard type hints and a descriptive docstring. The LLM uses the docstring and parameter types to construct its function-calling arguments.

```python
def get_weather(city: str) -> str:
    """Get the weather for a city"""
    return f"The weather in {city} is sunny."
```

### Initializing the Model & Agent
We bind the model to the tool using `create_agent` from the `langchain.agents` module (which builds a `CompiledStateGraph` from LangGraph under the hood):

```python
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini Model
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

# Compile the Agent with a Custom Tool & Prompt
agent = create_agent(
    model=gemini_model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)
```

### Invoking the Agent
We invoke the agent by passing it a state containing list-formatted messages:

```python
response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the weather like in New York?"
        }
    ]
})

# To extract the final output from the agent's message list:
final_output = response['messages'][-1].content
print(final_output)  # "The weather in New York is sunny."
```

---

## 3. Unified Model Initialization (`init_chat_model`)

* **Reference Notebook:** [02_model_integration.ipynb](file:///f:/WeCloudData/AI/AgenticAI/langchain_ai/langchain/02_model_integration.ipynb)

LangChain provides a standard wrapper, `init_chat_model`, to initialize chat models from different providers in a unified way. This allows you to switch between providers (OpenAI, Groq, Google, etc.) dynamically by simply changing a string identifier.

### Usage Syntax
```python
from langchain.chat_models import init_chat_model

# 1. Initialize Google Gemini (using the Google GenAI SDK integration)
gemini_lite = init_chat_model("google_genai:gemini-2.5-flash-lite")

# 2. Initialize Groq (using Qwen model hosted on Groq)
groq_qwen = init_chat_model("groq:qwen/qwen3-32b")
```

### Supported Providers & Models

| Provider Code | Model Name | Use Case / Characteristics |
| :--- | :--- | :--- |
| `google_genai` | `gemini-2.5-flash-lite` | Efficient, fast, native multimodal understanding. |
| `groq` | `qwen/qwen3-32b` | Low latency inference, open weights, powerful reasoning. |

---

## 4. Model Invocations: Invoke, Stream, and Batch

* **Reference Notebook:** [02_model_integration.ipynb](file:///f:/WeCloudData/AI/AgenticAI/langchain_ai/langchain/02_model_integration.ipynb)

All chat models inheriting from LangChain's `BaseChatModel` support the standard runnable interface: `invoke`, `stream`, and `batch`.

### A. Invoke (Standard Query)
Sends a prompt and returns the full generated message synchronously once complete.

```python
model = init_chat_model("google_genai:gemini-2.5-flash-lite")
response = model.invoke("Explain about Google Gemini")
print(response.content)
```

### B. Stream (Real-Time Progressive Generation)
Returns an iterator yielding response chunks as they are generated. This improves user experience for long outputs by reducing perceived latency.

```python
# Stream output chunk-by-chunk in real-time
for chunk in model.stream("Write me a 200-word paragraph on artificial intelligence"):
    print(chunk.text, end="|", flush=True)  # Or chunk.content depending on integration
```

### C. Batch (Parallel execution)
Executes multiple independent queries in parallel. This is highly optimized for performance and reduces cost by utilizing concurrent execution under the hood.

```python
responses = model.batch([
    "why do parrots have colorful feathers",
    "How do aeroplanes fly?",
    "what is quantum computing?"
])

for response in responses:
    print(response.content)
```

### D. Batch with Concurrency Control
You can configure a limit on how many requests are sent concurrently using `config` and `max_concurrency`.

```python
responses = model.batch(
    [
        "why do parrots have colorful feathers",
        "How do aeroplanes fly?",
        "what is quantum computing?"
    ],
    config={"max_concurrency": 2}  # Restricts concurrent executions to 2
)
```

---

## 5. Key LangChain Message Classes

When interacting with chat models or agents, LangChain uses structured message objects to represent different roles.

| Message Class | Represents | Typical Attributes |
| :--- | :--- | :--- |
| **`HumanMessage`** | Input message sent by the user. | `content` |
| **`AIMessage`** | Output message generated by the assistant. | `content`, `response_metadata`, `tool_calls` |
| **`ToolMessage`** | Message containing execution result of a tool function, sent back to the LLM. | `content`, `name`, `tool_call_id` |

### Example Message History Structure
When executing an agent invocation with tool-calling (such as checking the weather), the message flow looks like this:

1. **`HumanMessage`**: *"What is the weather like in New York?"*
2. **`AIMessage`**: (Empty text content, but containing a `tool_calls` list with arguments: `{'city': 'New York'}`)
3. **`ToolMessage`**: (Content: *"The weather in New York is sunny."*, matched with the `tool_call_id` of the request)
4. **`AIMessage`**: (Text content: *"The weather in New York is sunny."* based on the tool result)
