# 📦 LangGraph Study Guide

This subfolder demonstrates **LangGraph**, the graph‑based orchestration layer built on top of LangChain. LangGraph lets you define **state‑graphs** where each node performs a specific task (e.g., call a model, run a tool) and edges dictate the flow based on the agent’s output.

## 📂 Directory Layout
```
langGraph/
├─ 01_basic_chatbot.ipynb   # Minimal chatbot built with a LangGraph StateGraph
├─ basic_finanical_usecase/ # Example use‑case (not covered here)
└─ README.MD                # **You are reading it!**
```

## 🎯 Core Concepts
| Concept | Description |
|---------|-------------|
| **State** | A typed dictionary (`TypedDict`) that holds the mutable data the graph passes between nodes (e.g., `messages`). |
| **Node** | A Python function that receives the current `state` and returns a new (or modified) `state`. Nodes can call LLMs, tools, or any custom logic. |
| **Edge** | A directed connection between two nodes. Edges can be unconditional (`add_edge`) or conditional (`add_conditional_edges`) based on the content of the state. |
| **START / END** | Special sentinel nodes that mark the entry and exit points of the graph. |
| **StateGraph** | The builder object (`StateGraph(state_schema)`) that collects nodes, edges, and compiles them into a runnable graph (`graph.compile()`). |
| **ToolNode** | A helper node that executes a list of LangChain `Tool`s and routes back to the graph based on `tools_condition`. |

## 🛠️ Building a Simple Chatbot (from `01_basic_chatbot.ipynb`)
### 1. Define the State
```python
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import add_messages

class State(TypedDict):
    # `messages` is a list that is automatically appended to on each turn.
    messages: Annotated[list, add_messages]
```
### 2. Create Node Functions
```python
# Simple echo bot – just returns the last user message.
def chatbot(state: State) -> State:
    return {"messages": [AIMessage(content="You said: " + state["messages"][-1].content)]}
```
### 3. Initialise the Graph Builder
```python
from langgraph.graph import StateGraph, START, END

graph_builder = StateGraph(State)
```
### 4. Add Nodes & Edges
```python
# Register the chatbot node.
graph_builder.add_node("chatbot", chatbot)

# Connect START → chatbot → END (unconditional flow).
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
```
### 5. Compile & Run
```python
graph = graph_builder.compile()
# Invoke with an initial user message.
result = graph.invoke({"messages": [HumanMessage(content="Hello!")]})
print(result["messages"][-1].content)  # → "You said: Hello!"
```

## 📈 More Advanced Example – Chatbot With Tools
The notebook also shows a **tool‑enabled** graph using `ToolNode` and `tools_condition`:
```python
# Define a LangChain tool (e.g., a calculator).
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Bind the tool to the model.
llm_with_tools = llm.bind_tools([multiply])

# Node that calls the LLM with tools.
def chatbot_with_tools(state: State) -> State:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build the graph with a conditional edge.
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot_with_tools", chatbot_with_tools)
graph_builder.add_node("tools", ToolNode([multiply]))

graph_builder.add_edge(START, "chatbot_with_tools")
# If the LLM requests a tool the condition routes to the tool node.
graph_builder.add_conditional_edges(
    "chatbot_with_tools",
    tools_condition,  # provided by `langgraph.prebuilt`
)
graph_builder.add_edge("tools", END)
```
This pattern lets the agent **decide dynamically** whether to call a tool or finish the conversation.

## 🔁 Typical LangGraph Execution Flow (Mermaid)
```mermaid
flowchart TD
    A[START] --> B[Chatbot Node]
    B -->|Result| C{Tool Call?}
    C -->|Yes| D[ToolNode (exec tool)]
    D --> E[END]
    C -->|No| E[END]
```
- The `tools_condition` helper inspects the last LLM message; if it contains a `tool_call` the graph follows the **Yes** branch.

## 📚 Study Tips & Checklist
- **Run the notebooks** (`01_basic_chatbot.ipynb`) to see the graph in action.
- **Inspect the compiled graph**: `graph.get_graph().draw_mermaid_png()` (requires `graphviz`).
- **Experiment**: add a new node that accesses a database, then route to it conditionally based on a keyword in the LLM response.
- **Combine with other topics**: you can embed a LangGraph state graph inside a LangChain `create_agent` pipeline, or use the RAG retrieval step as a node.

---
*All diagrams above are embedded as Mermaid code, which renders automatically in most markdown viewers. For a static PNG export, run `graph.get_graph().draw_mermaid_png()` from the notebook and save the image.*
