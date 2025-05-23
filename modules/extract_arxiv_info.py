import os
import json

PAPER_DIR = "papers"


def extract_arxiv_info(paper_id: str) -> str:
    """
    Retrieve cached paper metadata by arXiv identifier from local JSON storage.

    Performs filesystem traversal across topic subdirectories to locate paper data
    previously cached by search operations. Returns serialized JSON on successful
    lookup or error message on failure.

    Args:
        paper_id (str): arXiv paper identifier in short format (e.g., "2405.12345v1")

    Returns:
        str: JSON-serialized paper metadata dict if found, error string otherwise

    Side Effects:
        - Filesystem I/O across papers directory structure
        - JSON deserialization of potentially large files
    """
    for topic_dir in os.listdir(PAPER_DIR):
        file_path = os.path.join(PAPER_DIR, topic_dir, "papers_info.json")
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r") as f:
                    papers = json.load(f)
                    if paper_id in papers:
                        return json.dumps(papers[paper_id], indent=2)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                continue

    return f"No information found for paper ID '{paper_id}'."