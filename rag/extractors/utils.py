from rag.extractors.pdf_extractor import (
    extract_metadata_pages,
    extract_information,
    extract_title,
    extract_methods,
    extract_keyresults,
    extract_tables,
)

from rag.extractors.docx_extractor import extract_tables_from_doc, fetch_relevant_tables


def process_files(pdf_path, docx_path):
    # Extract information from the PDF
    metadata, pages_text = extract_metadata_pages(pdf_path)
    information = extract_information(pages_text)
    title = extract_title(pages_text)
    methods = extract_methods(pages_text)
    keyresults = extract_keyresults(pages_text)
    tables = extract_tables(pages_text)

    # Extract information from the DOCX
    doc_tables = extract_tables_from_doc(docx_path)
    relevant_doc_tables = fetch_relevant_tables(doc_tables)

    # Create the document dictionary
    document = {
        "metadata": metadata,
        "information": information,
        "title": title,
        "methods": methods,
        "tables": tables,
        "keyresults": keyresults,
        "tables": tables,
    }
    
    assert document["tables"].keys() == relevant_doc_tables.keys()

    # Add the relevant DOCX tables to the PDF tables
    for id, table in relevant_doc_tables.items():
        document["tables"][id].append(table)

    return document
