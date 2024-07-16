from .pdf_extractor import (
    extract_metadata_pages,
    extract_title,
    extract_methods,
    extract_keyresults,
    extract_tables,
    extract_information
)

from .docx_extractor import (
    extract_tables_from_doc,
    fetch_relevant_tables
)

__all__ = [
    'extract_metadata_pages',
    'extract_title',
    'extract_methods',
    'extract_keyresults',
    'extract_tables',
    'extract_information',
    'extract_tables_from_doc',
    'fetch_relevant_tables'
]
