# modules/search_pubmed.py
import os
import json
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import time

PAPER_DIR = "papers"
PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def search_pubmed(topic: str, max_results: int = 5) -> List[str]:
    """
    Execute PubMed API search query and persist results to local filesystem.

    Performs search against PubMed database using NCBI E-utilities API,
    extracts metadata from XML responses, and writes structured data
    to topic-specific JSON files in the papers directory.

    Args:
        topic (str): Query string for PubMed search API
        max_results (int): Maximum number of paper objects to process from API response

    Returns:
        List[str]: Collection of PubMed IDs (PMIDs) for successfully processed papers

    Side Effects:
        - Creates directory structure under PAPER_DIR
        - Writes/updates pubmed_papers_info.json files
        - Network I/O to PubMed API with rate limiting
    """
    # Step 1: Search for paper IDs
    search_url = f"{PUBMED_BASE_URL}esearch.fcgi"
    search_params = {
        'db': 'pubmed',
        'term': topic,
        'retmax': max_results,
        'retmode': 'json',
        'sort': 'relevance'
    }

    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        pmids = search_data.get('esearchresult', {}).get('idlist', [])

        if not pmids:
            return []

        # Rate limiting - PubMed allows 3 requests per second
        time.sleep(0.34)

        # Step 2: Fetch detailed information for each paper
        fetch_url = f"{PUBMED_BASE_URL}efetch.fcgi"
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml'
        }

        fetch_response = requests.get(fetch_url, params=fetch_params)
        fetch_response.raise_for_status()

        # Parse XML response
        papers_data = _parse_pubmed_xml(fetch_response.text)

        # Save to file
        path = os.path.join(PAPER_DIR, f"pubmed_{topic.lower().replace(' ', '_')}")
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, "pubmed_papers_info.json")

        try:
            with open(file_path, "r") as file:
                saved = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            saved = {}

        # Update saved data
        for pmid, paper_data in papers_data.items():
            saved[pmid] = paper_data

        with open(file_path, "w") as file:
            json.dump(saved, file, indent=2)

        return list(papers_data.keys())

    except requests.RequestException as e:
        print(f"Error fetching from PubMed: {e}")
        return []
    except Exception as e:
        print(f"Error processing PubMed data: {e}")
        return []


def _parse_pubmed_xml(xml_content: str) -> Dict[str, Dict[str, Any]]:
    """
    Parse PubMed XML response into structured paper data.

    Args:
        xml_content (str): Raw XML response from PubMed efetch API

    Returns:
        Dict[str, Dict[str, Any]]: Dictionary mapping PMIDs to paper metadata
    """
    papers = {}

    try:
        root = ET.fromstring(xml_content)

        for article in root.findall('.//PubmedArticle'):
            # Extract PMID
            pmid_elem = article.find('.//PMID')
            if pmid_elem is None:
                continue
            pmid = pmid_elem.text

            # Extract basic info
            medline_citation = article.find('.//MedlineCitation')
            if medline_citation is None:
                continue

            article_elem = medline_citation.find('.//Article')
            if article_elem is None:
                continue

            # Title
            title_elem = article_elem.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "No title available"

            # Abstract
            abstract_elem = article_elem.find('.//Abstract/AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"

            # Authors
            authors = []
            author_list = article_elem.find('.//AuthorList')
            if author_list is not None:
                for author in author_list.findall('.//Author'):
                    last_name = author.find('.//LastName')
                    first_name = author.find('.//ForeName')
                    if last_name is not None:
                        name = last_name.text
                        if first_name is not None:
                            name = f"{first_name.text} {name}"
                        authors.append(name)

            # Journal
            journal_elem = article_elem.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else "Unknown journal"

            # Publication date
            pub_date = article_elem.find('.//Journal/JournalIssue/PubDate')
            date_str = "Unknown date"
            if pub_date is not None:
                year = pub_date.find('.//Year')
                month = pub_date.find('.//Month')
                day = pub_date.find('.//Day')

                if year is not None:
                    date_str = year.text
                    if month is not None:
                        date_str = f"{month.text} {date_str}"
                        if day is not None:
                            date_str = f"{day.text} {date_str}"

            # DOI
            doi = None
            article_ids = article.findall('.//ArticleId')
            for article_id in article_ids:
                if article_id.get('IdType') == 'doi':
                    doi = article_id.text
                    break

            # PubMed URL
            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            papers[pmid] = {
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "journal": journal,
                "published": date_str,
                "pmid": pmid,
                "doi": doi,
                "pubmed_url": pubmed_url
            }

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

    return papers
