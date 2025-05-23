import os
import json

PAPER_DIR = "papers"

def extract_arxiv_info(paper_id: str) -> str:
    """
    Retrieve saved paper info by ID from local JSON files.

    Args:
        paper_id: The unique arXiv ID of the paper (e.g., "2405.12345v1")

    Returns:
        A formatted JSON string with paper details, or an error message if not found.
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
