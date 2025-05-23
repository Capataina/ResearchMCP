from mcp.server.fastmcp import FastMCP
from modules.search_arxiv import search_arxiv
from modules.extract_arxiv_info  import extract_arxiv_info

mcp = FastMCP("research")

mcp.register(search_arxiv)
mcp.register(extract_arxiv_info)

if __name__ == "__main__":
    mcp.run(transport="stdio")
