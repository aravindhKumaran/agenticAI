from mcp.server.fastmcp import FastMCP 

# server initialization
mcp = FastMCP("Math") 


# tools creation
@mcp.tool()
def add(a:int, b:int) -> int:
    """Add two numbers"""
    return a + b 

@mcp.tool()
def sub(a:int, b:int) -> int:
    """Subtract two numbers"""
    return a - b 

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """Multiply two numbers"""
    return a * b 

@mcp.tool()
def divide(a:int, b:int) -> int:
    """Divide two numbers"""
    return a / b 



if __name__ == "__main__":
    # Runs the MCP server
    # The transport="stdio" argument tells the server to
    # Use standard input/output (stdin and stdout) to receive and respond to tool function calls.
    mcp.run(transport = "stdio") 