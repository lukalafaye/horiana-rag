import pickle
import json
from chromadb.config import Settings
from dotenv import load_dotenv
import os
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer
import pandas as pd
from pprint import pprint

from rag.utils import validate_params
import torch

docker = False

if torch.cuda.is_available():
    stella = SentenceTransformer(
        "infgrad/stella_en_400M_v5", trust_remote_code=True
    ).cuda()
else:
    stella = SentenceTransformer("infgrad/stella_en_400M_v5", trust_remote_code=True)


@validate_params
def load_tables_chunks(pickle_file):
    # Refer to extract_tables_chunks
    """
    Loads tables text chunks stored in pickle file.
    text_chunks = [(text, id), ...]
    """
    with open(pickle_file, "rb") as f:
        text_chunks = pickle.load(f)

    return text_chunks


@validate_params
def load_abstracts_chunks(csv_file):
    # returns dataframe
    # pubmed_id,title,keywords,journal,abstract,conclusions,methods,results,copyrights,doi,publication_date,authors
    """
    Loads abstracts text chunks stored in pickle file.
    text_chunks = [(text, id), ...]
    """
    df = pd.read_csv(csv_file)
    
    if 'pubmed_id' not in df.columns or 'abstract' not in df.columns:
        raise ValueError("CSV file must contain 'pubmed_id' and 'abstract' columns")
    
    # Convert the pubmed_id to string and create the list of tuples
    text_chunks = [(row['abstract'], str(row['pubmed_id'])) for _, row in df.iterrows()]
    
    return text_chunks


class StellaEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.stella = stella

    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = []
        for text in texts:
            embedding_array = self.stella.encode((str(text)))
            embeddings.append(embedding_array.tolist())
        return embeddings


@validate_params
def connect_to_chromadb():
    """ "
    Connects to chroma db server already running...
    """

    chroma_env = ".chroma_env"
    if docker:
        chroma_env = "/app/" + chroma_env

    load_dotenv(chroma_env)
    chroma_client_auth_credentials = os.getenv("CHROMA_CLIENT_AUTHN_CREDENTIALS")
    chroma_client_auth_provider = os.getenv("CHROMA_CLIENT_AUTHN_PROVIDER")

    print(chroma_client_auth_provider, chroma_client_auth_credentials)
    # https://cookbook.chromadb.dev/core/collections/#collection-utilities
    client = chromadb.HttpClient(
        settings=Settings(
            chroma_client_auth_provider=chroma_client_auth_provider,
            chroma_client_auth_credentials=chroma_client_auth_credentials,
        )
    )

    return client


@validate_params
def update_collection(collection_name, tables_chunks):
    """
    tables_chunks = [("table text", "id"), ...]
    """

    client = connect_to_chromadb()
    print("Client heartbeat: ", client.heartbeat())

    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=StellaEmbeddingFunction()
    )

    ids = [table[1] for table in tables_chunks]
    docs = [table[0] for table in tables_chunks]

    assert len(ids) == len(docs)

    collection.add(documents=docs, ids=ids)

    return collection


@validate_params
def update_abstracts_collection(abstracts_chunks):
    # Complete with abstacts chunks

    client = connect_to_chromadb()
    print("Client heartbeat: ", client.heartbeat())

    collection_name = "abstracts"
    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=StellaEmbeddingFunction()
    )

    ids = abstracts_chunks["doi"].tolist()
    docs = abstracts_chunks["abstract"].tolist()

    assert len(ids) == len(docs)

    collection.add(documents=docs, ids=ids)

    return collection


def main():
    config_path = "config.json"
    if docker:
        config_path = "/app/" + config_path

    # Lire le fichier de configuration JSON
    with open(config_path, "r") as f:
        config = json.load(f)

    tables_path = config.get("tables_output_path")
    tables_chunks = load_tables_chunks(tables_path)

    tables_collection = update_collection(
        "tables", tables_chunks
    )  # adds some text chunks to chromadb

    abstracts_path = config.get("abstracts_output_path")
    abstracts_chunks = load_abstracts_chunks(abstracts_path)

    pprint(abstracts_chunks)
    abstracts_collection = update_collection("abstracts", abstracts_chunks)
    # Exécuter la fonction read pour afficher le contenu du fichier pickle

    print(tables_collection.peek())
    print(abstracts_collection.peek())


if __name__ == "__main__":
    main()
