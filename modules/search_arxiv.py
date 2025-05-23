import os
import json
import arxiv
from typing import List

PAPER_DIR = "papers"


def search_arxiv(topic: str, max_results: int = 5) -> List[str]:
    """
    Execute arXiv API search query and persist results to local filesystem.

    Performs relevance-sorted search against arXiv database, extracts metadata
    from response objects, and writes structured data to topic-specific JSON files
    in the papers directory hierarchy. Maintains existing data through merge operations.

    Args:
        topic (str): Query string for arXiv search API
        max_results (int): Maximum number of paper objects to process from API response

    Returns:
        List[str]: Collection of arXiv short IDs for successfully processed papers

    Side Effects:
        - Creates directory structure under PAPER_DIR
        - Writes/updates papers_info.json files
        - Network I/O to arXiv API
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = client.results(search)

    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "papers_info.json")

    try:
        with open(file_path, "r") as file:
            saved = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        saved = {}

    paper_ids = []
    for paper in results:
        pid = paper.get_short_id()
        saved[pid] = {
            "title": paper.title,
            "summary": paper.summary,
            "authors": [a.name for a in paper.authors],
            "pdf_url": paper.pdf_url,
            "published": str(paper.published.date())
        }
        paper_ids.append(pid)

    with open(file_path, "w") as file:
        json.dump(saved, file, indent=2)

    return paper_ids