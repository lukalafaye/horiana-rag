import pytest
import pickle
import json 
import pandas as pd 

from rag.embed import load_tables_chunks, load_abstracts_chunks
# GPU only
# from rag.embed import StellaEmbeddingFunction connect_to_chromadb, update_collection, update_abstracts_collection

from rag.preprocess import preprocess, extract_tables_chunks, fetch_abstracts

@pytest.fixture(scope='module')
def setup_data():
    config_path = 'config.json'
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    pdf_path = config["test_pdf_path"]
    docx_path = config["test_docx_path"]
    output_path = config["test_output_path"]
    tables_path = config["test_tables_path"]
    abstracts_path = config["test_abstracts_path"]

    keywords = ["knee", "bucket"]
    
    preprocess(pdf_path, docx_path, output_path) # create document.pkl (dict)
    extract_tables_chunks(output_path, tables_path) # create tables.pkl  [(table text, table id), ...]
    fetch_abstracts(keywords, abstracts_path) # create csv for abstracts (dataframe)
    
    return {
        "output_path": output_path,
        "tables_path": tables_path,
        "abstracts_path": abstracts_path
    }

def test_load_tables_chunks(setup_data):
    text_chunks = load_tables_chunks(setup_data["tables_path"])
    
    assert isinstance(text_chunks, list)
    assert len(text_chunks) > 0
    assert isinstance(text_chunks[0], tuple)
    assert len(text_chunks[0]) == 2 # (table text, id)

def test_load_abstracts_chunks(setup_data):
    abstracts_df = load_abstracts_chunks(setup_data["abstracts_path"])
    
    assert isinstance(abstracts_df, pd.DataFrame)
    assert not abstracts_df.empty
    # pubmed_id,title,keywords,journal,abstract,conclusions,methods,results,copyrights,doi,publication_date,authors
    assert 'doi' in abstracts_df.columns
    assert 'abstract' in abstracts_df.columns

"""
GPU tests

def test_stella_embedding_function(setup_data):
    stella_embedding_func = StellaEmbeddingFunction()
    
    with open(setup_data["tables_path"], "rb") as f:
        text_chunks = pickle.load(f)
    
    texts = [chunk[0] for chunk in text_chunks]
    embeddings = stella_embedding_func(texts)
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(text_chunks)
    assert isinstance(embeddings[0], list)

def test_connect_to_chromadb():
    client = connect_to_chromadb()
    
    # Add additional checks if needed, e.g., verifying client connection
    assert client is not None

def test_update_collection(setup_data):
    with open(setup_data["tables_path"], "rb") as f:
        tables_chunks = pickle.load(f)
    
    collection = update_collection("tables", tables_chunks)
    
    # Add checks for the collection if needed
    assert collection is not None

def test_update_abstracts_collection(setup_data):
    abstracts_df = load_abstracts_chunks(setup_data["abstracts_path"])
    collection = update_abstracts_collection(abstracts_df)
    
    # Add checks for the collection if needed
    assert collection is not None
"""