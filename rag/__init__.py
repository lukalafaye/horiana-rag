# Import core modules or functions for easy access from the package level
from .preprocess import process_files

# from .embed import embed_documents
# from .query import query_database

# Define the public API of the package
__all__ = [
    "process_files",
    #    'embed_documents',
    #    'query_database'
]

# Optionally, include package metadata
__version__ = "0.1"
__description__ = """
RAG (Retrieval-Augmented Generation) for document
processing and querying
"""
