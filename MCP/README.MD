# 📦 MCP (Model Context Protocol) Study Guide

This subfolder contains a lightweight **Model Context Protocol (MCP)** implementation used to expose external tools/services (e.g., a math server or a weather server) to LLM agents.

## 📂 Directory Contents
- `client.py` – example client that connects to the MCP server, sends a request, and receives a JSON response.
- `math_server.py` – tiny HTTP server exposing a `calculate(a, b, op)` endpoint.
- `weather_server.py` – mock weather service returning a forecast for a given city.
- `docs.MD` – additional documentation (auto‑generated).
- `README_MCP_Architecture.md` – architecture diagram (kept for reference).

## 🎯 What MCP Solves
MCP provides a **standardized JSON‑based contract** between an LLM‑driven agent and external services:
1. **Request** – `{ "method": "calculate", "params": { "a": 2, "b": 3, "op": "+" } }`
2. **Response** – `{ "result": 5, "status": "ok" }`

This decouples the agent logic from the service implementation, making it easy to plug‑in new tools (e.g., weather, calculator, database) without changing the agent code.

## 🛠️ Typical MCP Flow (Mermaid Diagram)
```mermaid
flowchart TD
    A[LLM Agent] -->|Tool Call (JSON)| B[MCP Client (client.py)]
    B -->|HTTP POST| C[MCP Server]
    C -->|Dispatch to Service| D[Math / Weather Server]
    D -->|Result JSON| C
    C -->|JSON Response| B
    B -->|Tool Result| A
```

## 📄 Code Walk‑through
### `client.py`
```python
import requests
import json

def call_mcp(method: str, params: dict):
    payload = {"method": method, "params": params}
    response = requests.post("http://localhost:8000", json=payload)
    return response.json()

# Example usage
result = call_mcp("calculate", {"a": 4, "b": 2, "op": "*"})
print(result)  # → {"result": 8, "status": "ok"}
```
*The client serialises a request, posts it to the MCP server, and parses the JSON reply.*

### `math_server.py`
```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MathHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])) )
        method = data["method"]
        params = data["params"]
        if method == "calculate":
            a, b, op = params["a"], params["b"], params["op"]
            ops = {"+": a + b, "-": a - b, "*": a * b, "/": a / b}
            result = ops.get(op, None)
            response = {"result": result, "status": "ok"}
        else:
            response = {"error": "unknown method", "status": "error"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), MathHandler)
    print("MCP Math Server listening on :8000")
    server.serve_forever()
```
*The server receives the JSON payload, executes the requested operation, and returns a JSON result.*

### `weather_server.py`
```python
# Simplified mock weather server – returns a static forecast
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class WeatherHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])) )
        city = data["params"].get("city", "unknown")
        response = {"city": city, "forecast": "Sunny, 25°C", "status": "ok"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8001), WeatherHandler)
    print("MCP Weather Server listening on :8001")
    server.serve_forever()
```
*Provides a deterministic weather forecast for any city – useful for quick testing of LLM agents.*

## 📚 Study Tips
- **Run the servers** (`python math_server.py` & `python weather_server.py`) before invoking the client.
- **Inspect the JSON** – the exact format is what the LLM agent sees, so keep it stable.
- **Add new services** by defining a new handler and updating the client to use a new `method` name.
- **Combine with LangChain** – bind `client.call_mcp` as a LangChain tool to let the agent call any MCP‑exposed service.

---
*For a visual overview, see `README_MCP_Architecture.md` in this folder.*
