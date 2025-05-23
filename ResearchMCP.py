from mcp.server.fastmcp import FastMCP
from modules.search_arxiv import search_arxiv
from modules.extract_arxiv_info import extract_arxiv_info
from modules.search_pubmed import search_pubmed
from modules.extract_pubmed_info import extract_pubmed_info

mcp = FastMCP("research")


# ArXiv tools
@mcp.tool()
def search_arxiv_tool(topic: str, max_results: int = 5) -> list[str]:
    """
    Find and save research papers from arXiv on any topic you're interested in.

    Best for: Physics, Mathematics, Computer Science, and some Biology papers.
    Simply provide a research topic and get back a list of relevant paper IDs.

    Args:
        topic: What research area you want to explore
        max_results: How many papers to find (default is 5)

    Returns:
        List of arXiv paper IDs that you can use to get detailed information
    """
    return search_arxiv(topic, max_results)


@mcp.tool()
def extract_arxiv_info_tool(paper_id: str) -> str:
    """
    Get detailed information about a specific arXiv paper you've previously searched for.

    Use this to retrieve the full details (title, authors, summary, etc.) of any arXiv paper
    from your previous searches. Just provide the paper ID you got from searching.

    Args:
        paper_id: The paper ID from your arXiv search results (looks like "2405.12345v1")

    Returns:
        Complete paper information including title, authors, summary, and PDF link
    """
    return extract_arxiv_info(paper_id)


# PubMed tools
@mcp.tool()
def search_pubmed_tool(topic: str, max_results: int = 5) -> list[str]:
    """
    Find and save medical and biological research papers from PubMed.

    Best for: Medicine, Biology, Sports Science, Nutrition, Health, and Life Sciences.
    Perfect for topics like fitness, supplements, medical treatments, and biological research.

    Args:
        topic: What medical/biological research area you want to explore
        max_results: How many papers to find (default is 5)

    Returns:
        List of PubMed IDs (PMIDs) that you can use to get detailed information
    """
    return search_pubmed(topic, max_results)


@mcp.tool()
def extract_pubmed_info_tool(pmid: str) -> dict:
    """
    Get detailed information about a specific PubMed paper you've previously searched for.

    Use this to retrieve the full details (title, authors, abstract, journal, etc.) of any
    PubMed paper from your previous searches. Just provide the PMID you got from searching.

    Args:
        pmid: The PubMed ID from your search results (looks like "12345678")

    Returns:
        Complete paper information including title, authors, abstract, journal, and PubMed link
    """
    return extract_pubmed_info(pmid)


if __name__ == "__main__":
    mcp.run(transport="stdio")