# MCP Client--Server Example with LangChain

## Overview

This project demonstrates how to use **MCP (Model Context Protocol)**
servers as tool providers for a LangChain agent.

The solution consists of:

-   A **Math MCP Server** exposing arithmetic tools.
-   A **Weather MCP Server** exposing weather-related tools.
-   A **LangChain Agent** that discovers and uses these tools through
    MCP.

------------------------------------------------------------------------

# High-Level Architecture

``` text
+-------------------+
|    User Query     |
+---------+---------+
          |
          v
+-------------------+
| LangChain Agent   |
| (ChatGroq Model)  |
+---------+---------+
          |
          v
+-------------------+
| MCP Client        |
| MultiServerMCP    |
+---------+---------+
          |
    +-----+-----+
    |           |
    v           v
+--------+  +---------+
| Math   |  | Weather |
| Server |  | Server  |
+--------+  +---------+
```

------------------------------------------------------------------------

# Components

## 1. MCP Client

The client is responsible for:

-   Connecting to one or more MCP servers.
-   Discovering available tools.
-   Making those tools available to the LangChain agent.
-   Routing tool calls to the appropriate MCP server.

### Configured Servers

### Math Server

Uses the **stdio** transport.

``` python
{
    "math": {
        "command": "python",
        "args": [os.path.abspath("MCP/math_server.py")],
        "transport": "stdio"
    }
}
```

The client launches the server as a local subprocess and communicates
through stdin/stdout.

### Weather Server

Uses the **streamable-http** transport.

``` python
{
    "weather": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable-http"
    }
}
```

The client communicates with a running HTTP MCP server.

------------------------------------------------------------------------

## 2. Math MCP Server

The Math server exposes arithmetic operations as MCP tools.

### Available Tools

-   add(a, b)
-   sub(a, b)
-   multiply(a, b)
-   divide(a, b)

Example:

``` python
@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b
```

### Transport

``` python
mcp.run(transport="stdio")
```

Communication happens through standard input and standard output.

------------------------------------------------------------------------

## 3. Weather MCP Server

The Weather server exposes weather-related functionality.

### Available Tool

``` python
@mcp.tool()
async def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny."
```

### Transport

``` python
mcp.run(transport="streamable-http")
```

Communication occurs through HTTP.

------------------------------------------------------------------------

# Tool Discovery Flow

When the application starts:

``` python
tools = await client.get_tools()
```

The following occurs:

1.  Connect to Math MCP Server.
2.  Connect to Weather MCP Server.
3.  Request available tool definitions.
4.  Receive tool metadata.
5.  Convert MCP tools into LangChain-compatible tools.
6.  Return the combined tool list.

Result:

``` text
[
    add,
    sub,
    multiply,
    divide,
    get_weather
]
```

------------------------------------------------------------------------

# Agent Execution Flow

The tools are attached to the agent:

``` python
agent = create_agent(
    model=model,
    tools=tools
)
```

When a user submits a query:

``` python
await agent.ainvoke(...)
```

The workflow is:

``` text
User Question
      |
      v
LangChain Agent
      |
      v
LLM decides whether a tool is required
      |
      v
Tool Invocation
      |
      v
MCP Client
      |
      v
Appropriate MCP Server
      |
      v
Tool Execution
      |
      v
Tool Result
      |
      v
LLM generates final answer
```

------------------------------------------------------------------------

# Example: Math Question

User:

``` text
What's (3 + 5) × 12?
```

Agent:

``` text
add(3, 5)
```

Result:

``` text
8
```

Agent:

``` text
multiply(8, 12)
```

Result:

``` text
96
```

Final Response:

``` text
The result is 96.
```

------------------------------------------------------------------------

# Example: Weather Question

User:

``` text
What is the weather in California?
```

Agent:

``` text
get_weather("California")
```

Tool Result:

``` text
The weather in California is sunny.
```

Final Response:

``` text
The weather in California is sunny.
```

------------------------------------------------------------------------

# Why Async Is Used

The implementation uses asyncio because MCP communication is I/O-bound.

Examples of operations that require waiting:

-   Starting MCP server processes.
-   Network communication.
-   HTTP requests.
-   API calls.
-   Database access.

## Loading Tools

``` python
tools = await client.get_tools()
```

Meaning:

> Connect to MCP servers and wait until all tool definitions are
> received.

## Invoking the Agent

``` python
response = await agent.ainvoke(...)
```

Meaning:

> Run the agent and wait for all model and tool interactions to
> complete.

------------------------------------------------------------------------

# Understanding `await`

Example:

``` python
tools = await client.get_tools()
print("Loaded")
```

Execution order:

``` text
Start get_tools()
      |
      v
Wait for MCP servers
      |
      v
Receive tool definitions
      |
      v
Assign tools
      |
      v
Print "Loaded"
```

`await` pauses the current coroutine until the operation completes.

It does **not** automatically continue to the next line while the result
is pending.

However, while waiting, Python's event loop can run other async tasks.

------------------------------------------------------------------------

# Summary

This project demonstrates:

-   MCP server creation using FastMCP.
-   Multiple MCP transports (stdio and streamable-http).
-   Tool discovery through MCP.
-   LangChain agent integration.
-   Async MCP communication.
-   Tool execution across multiple servers.

The LangChain agent acts as the orchestrator, while MCP servers provide
reusable capabilities that can be shared across applications.
