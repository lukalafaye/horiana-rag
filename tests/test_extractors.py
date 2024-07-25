# tests/test_extractors.py

import pytest
import os
import pandas as pd

from rag.extractors.pdf_extractor import extract_metadata_pages, extract_information, extract_title, extract_methods, extract_keyresults, extract_tables
from rag.extractors.docx_extractor import extract_tables_from_doc, fetch_relevant_tables
from rag.extractors.abstracts_extractor import fetch_from_keywords

@pytest.fixture(scope='module')
def pdf_metadata_and_text():
    root_dir = os.path.join(os.path.dirname(__file__), '../redacted')
    studies_path = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file has the '-stat-report.pdf' suffix
            if filename.endswith('-stat-report.pdf'):
                # Extract the subfolder name from the directory path
                subfolder_name = os.path.basename(dirpath)
                # Construct the path to the file
                path = os.path.join(dirpath, filename)
                # Store the path in the dictionary
                studies_path[subfolder_name] = path

    documents = {}

    for study, path in studies_path.items():
        documents[study] = extract_metadata_pages(path)

    return documents


@pytest.fixture(scope='module')
def docx_tables():
    root_dir = os.path.join(os.path.dirname(__file__), '../redacted')
    studies_path = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file has the '-stat-report.pdf' suffix
            if filename.endswith('-stat-report.docx'):
                # Extract the subfolder name from the directory path
                subfolder_name = os.path.basename(dirpath)
                # Construct the path to the file
                path = os.path.join(dirpath, filename)
                # Store the path in the dictionary
                studies_path[subfolder_name] = path

    documents = {}

    for study, path in studies_path.items():
        documents[study] = extract_tables_from_doc(path) # list of dataframes

    return documents


@pytest.fixture(scope='module')
def extracted_tables(pdf_metadata_and_text):
    tables = {}
    for study, content in pdf_metadata_and_text.items():
        pages_content = content[1]
        tables[study] = extract_tables(pages_content)
    return tables


def test_extract_metadata_pages(pdf_metadata_and_text):
    for study, content in pdf_metadata_and_text.items():
        metadata = content[0]
        pages_content = content[1]

        assert isinstance(metadata, str)
        assert metadata

        assert isinstance(pages_content, list)
        assert pages_content
        assert len(pages_content) >= 4

def test_extract_information(pdf_metadata_and_text):
    for _, content in pdf_metadata_and_text.items():
        pages_content = content[1]
        information = extract_information(pages_content)

        assert isinstance(information, dict)
        assert information
        assert len(information.keys()) >= 3


def test_extract_title(pdf_metadata_and_text):
    for _, content in pdf_metadata_and_text.items():
        pages_content = content[1]
        title = extract_title(pages_content)

        assert isinstance(title, str)
        assert title
        assert len(title) <= 500

def test_extract_methods(pdf_metadata_and_text):
    for _, content in pdf_metadata_and_text.items():
        pages_content = content[1]
        methods = extract_methods(pages_content)

        assert isinstance(methods, dict)
        assert methods
        assert len(methods.keys()) >= 3


def test_extract_keyresults(pdf_metadata_and_text):
    for study, content in pdf_metadata_and_text.items():
        pages_content = content[1]
        keyresults = extract_keyresults(pages_content)

        assert isinstance(keyresults, str)
        assert keyresults
        assert len(keyresults) >= 500


def test_extract_tables(extracted_tables):
    for study, tables in extracted_tables.items():
        assert isinstance(tables, dict)
        assert tables
        assert len(tables.keys()) >= 6

def test_fetch_relevant_tables(docx_tables, extracted_tables):
    for study, table_list in docx_tables.items():
        relevant_doc_tables = fetch_relevant_tables(table_list)

        assert isinstance(relevant_doc_tables, dict)
        assert relevant_doc_tables

        assert len(relevant_doc_tables) == len(extracted_tables[study].keys())

def test_fetch_from_keywords():
    assert fetch_from_keywords([]) is None 
    assert fetch_from_keywords([""]) is None 
    assert fetch_from_keywords(["", ""]) is None 

    keywords_samples = [["medical", ""], ["medical", "disease"]]

    for sample in keywords_samples:
        abstractsdf = fetch_from_keywords(sample)
        assert isinstance(abstractsdf, pd.DataFrame)
        assert not abstractsdf.empty