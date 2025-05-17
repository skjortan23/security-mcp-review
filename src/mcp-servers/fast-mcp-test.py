from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtracts two integer numbers."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplies two integer numbers."""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divides two integer numbers."""
    return a / b

if __name__ == "__main__":
    mcp.run()