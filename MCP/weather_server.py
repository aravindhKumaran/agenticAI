from mcp.server.fastmcp import FastMCP 

# Server initialization
mcp = FastMCP("weather")


# tools creation

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for a location"""
    return f"The weather in {location} is sunny."


if __name__ == "__main__":
    # Runs the MCP server
    # The transport="streamable-http" argument tells the server to
    # Use streamable-http to receive and respond to tool function calls.
    mcp.run(transport = "streamable-http")

