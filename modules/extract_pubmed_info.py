import os
import json
from typing import Dict, Any

PAPER_DIR = "papers"


def extract_pubmed_info(pmid: str) -> Dict[str, Any]:
    """
    Retrieve cached PubMed paper metadata by PMID from local JSON storage.

    Performs filesystem traversal across topic subdirectories to locate paper data
    previously cached by PubMed search operations. Returns paper metadata dict on
    successful lookup or error dict on failure.

    Args:
        pmid (str): PubMed identifier (e.g., "12345678")

    Returns:
        Dict[str, Any]: Paper metadata dict if found, error dict otherwise

    Side Effects:
        - Filesystem I/O across papers directory structure
        - JSON deserialization of potentially large files
    """
    for topic_dir in os.listdir(PAPER_DIR):
        if not topic_dir.startswith('pubmed_'):
            continue

        file_path = os.path.join(PAPER_DIR, topic_dir, "pubmed_papers_info.json")
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r") as f:
                    papers = json.load(f)
                    if pmid in papers:
                        return papers[pmid]
            except (json.JSONDecodeError, FileNotFoundError) as e:
                continue

    return {"error": f"No information found for PMID '{pmid}'."}