from langchain_mcp_adapters.client import MultiServerMCPClient 
from langchain.agents import create_agent
from langchain_groq import ChatGroq 
from dotenv import load_dotenv 
import asyncio 
import os 


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [os.path.abspath("MCP/math_server.py")],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable-http"
            }
        }
    )

    tools = await client.get_tools()

    model = ChatGroq(model = "qwen/qwen3-32b")

    agent = create_agent(
        model = model,
        tools = tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

