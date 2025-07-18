# math_server.py
import os
from mcp.server.fastmcp import FastMCP
from datetime import datetime
mcp = FastMCP("Math")

#file system tool
@mcp.tool()
def read_file(path: str) -> str:
    """Read a file"""
    with open(path, "r") as file:
        return file.read()

#write file tool
@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write to a file"""
    with open(path, "w") as file:
        file.write(content)

#make file tool
@mcp.tool()
def make_file(path: str) -> str:
    """Make a file"""
    with open(path, "w") as file:
        pass

#list files in current directory tool
@mcp.tool()
def list_files() -> str:
    """List files in the current directory"""
    return "\n".join(os.listdir(os.getcwd()))

if __name__ == "__main__":
    print("Starting file mcp server")
    mcp.run(transport="stdio")