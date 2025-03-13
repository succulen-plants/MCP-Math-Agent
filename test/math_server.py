from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MathService")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Execute arithmetic addition operation"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Execute arithmetic multiplication operation""" 
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")  # 启动标准输入输出传输层