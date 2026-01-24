# chat/utils/fetch_pubmed.py
"""
Fetch research abstracts from PubMed
"""

from Bio import Entrez
import pandas as pd

Entrez.email = "kellyegorman@gmail.com"

def search_pubmed(query, max_results=50):
    """Search PubMed for research papers"""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

if __name__ == "__main__":
    print("Fetch research abstracts to expand knowledge base")