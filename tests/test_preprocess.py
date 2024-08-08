# tests/test_preprocess.py

import pytest
import os
import pickle
import pandas as pd

from src.healthdraft.preprocess import preprocess, extract_tables_chunks, fetch_abstracts
from src.config import get_absolute_path


@pytest.fixture(scope="module")
def pdf_paths():
    root_dir = get_absolute_path("../data/redacted")
    studies_pdf_paths = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file has the '-stat-report.pdf' suffix
            if filename.endswith("-stat-report.pdf"):
                # Extract the subfolder name from the directory path
                subfolder_name = os.path.basename(dirpath)
                # Construct the path to the file
                path = os.path.join(dirpath, filename)
                # Store the path in the dictionary
                studies_pdf_paths[subfolder_name] = path

    return studies_pdf_paths


@pytest.fixture(scope="module")
def docx_paths():
    root_dir = get_absolute_path("../data/redacted")
    studies_docx_path = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file has the '-stat-report.pdf' suffix
            if filename.endswith("-stat-report.docx"):
                # Extract the subfolder name from the directory path
                subfolder_name = os.path.basename(dirpath)
                # Construct the path to the file
                path = os.path.join(dirpath, filename)
                # Store the path in the dictionary
                studies_docx_path[subfolder_name] = path

    return studies_docx_path


@pytest.fixture(scope="module")
def synopsis_paths():
    root_dir = get_absolute_path("../data/redacted")
    studies_synopsis_paths = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file has the '-stat-report.pdf' suffix
            if filename.endswith("-synopsis.docx"):
                # Extract the subfolder name from the directory path
                subfolder_name = os.path.basename(dirpath)
                # Construct the path to the file
                path = os.path.join(dirpath, filename)
                # Store the path in the dictionary
                studies_synopsis_paths[subfolder_name] = path

    return studies_synopsis_paths


def remove_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def test_preprocess(pdf_paths, docx_paths, synopsis_paths):
    output_path = get_absolute_path("../data/test-output/out.pkl")
    remove_file_if_exists(output_path)

    print(synopsis_paths)

    for study, path in pdf_paths.items():
        pdf_path = path
        docx_path = docx_paths[study]
        synopsis_path = synopsis_paths[study]

        preprocess(pdf_path, docx_path, synopsis_path, output_path)

        assert os.path.exists(output_path)

        with open(output_path, "rb") as f:
            data = pickle.load(f)

        assert isinstance(data, dict)
        assert data

        os.remove(output_path)


def test_extract_tables_chunks(pdf_paths, docx_paths, synopsis_paths):
    output_path = get_absolute_path("../data/test-output/out.pkl")
    tables_path = get_absolute_path("../data/test-output/tables.pkl")

    remove_file_if_exists(output_path)
    remove_file_if_exists(tables_path)

    for study, path in pdf_paths.items():
        pdf_path = path
        docx_path = docx_paths[study]
        synopsis_path = synopsis_paths[study]

        preprocess(pdf_path, docx_path, synopsis_path, output_path)
        extract_tables_chunks(output_path, tables_path)

        assert os.path.exists(tables_path)
        with open(tables_path, "rb") as f:
            text_chunks = pickle.load(f)
        assert isinstance(text_chunks, list)
        assert text_chunks

        os.remove(output_path)
        os.remove(tables_path)


def test_fetch_abstracts():
    keywords = ["knee", "bucket"]
    abstracts_path = get_absolute_path("../data/test-output/out.csv")

    remove_file_if_exists(abstracts_path)
    print(abstracts_path)

    fetch_abstracts(keywords, abstracts_path)

    # Check that the CSV file was created
    assert os.path.exists(abstracts_path)

    # Validate the contents of the CSV file
    loaded_df = pd.read_csv(abstracts_path)
    assert isinstance(loaded_df, pd.DataFrame)
    assert not loaded_df.empty
    assert "doi" in loaded_df.columns
    assert "abstract" in loaded_df.columns

    os.remove(abstracts_path)
