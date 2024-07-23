import pickle 
from pathlib import Path
import json 
from pprint import pprint 
from biobert_embedding.embedding import BiobertEmbedding
import torch 
from chromadb.config import Settings
from dotenv import load_dotenv
import os
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

docker = True

class BioBertEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.biobert = BiobertEmbedding()

    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = []
        for text in texts:
            tensor = self.biobert.sentence_vector((str(text)))
            if isinstance(tensor, torch.Tensor):
                # Convert tensor to numpy array and then to a list
                embedding = tensor.detach().cpu().numpy().tolist()
            else:
                embedding = tensor  # Assuming it is already in the correct format
            embeddings.append(embedding)
        return embeddings

def connect_to_server():
    """"
    Connects to chroma db server already running...
    """

    chroma_env = '.chroma_env'
    if docker:
        chroma_env = '/app/' + chroma_env
    
    load_dotenv(chroma_env)
    chroma_client_auth_credentials= os.getenv("CHROMA_CLIENT_AUTHN_CREDENTIALS")
    chroma_client_auth_provider = os.getenv("CHROMA_CLIENT_AUTHN_PROVIDER")

    print(chroma_client_auth_provider, chroma_client_auth_credentials)

    client = chromadb.HttpClient(
        settings=Settings(
            chroma_client_auth_provider=chroma_client_auth_provider,
            chroma_client_auth_credentials=chroma_client_auth_credentials
        )
    )

    return client

def load_text_chunks(pickle_file):
    # Refer to extract_tables_chunks
    """
    Loads tables text chunks stored in pickle file.
    text_chunks = [(text, id), ...]
    """
    with open(pickle_file, "rb") as f:
        text_chunks = pickle.load(f)

    return text_chunks


def update_chromadb(text_chunks):
    """
    embedding_type can be biobert / biomistral / qwen7b
    text_chunks = [("document", "id"), ...]
    """

    client = connect_to_server()
    print("Client heartbeat: ", client.heartbeat())

    embedding_type = "biobert"
    if embedding_type=="biobert":
        existing_collections = client.list_collections()
        collection_name = "biobert-collection"
        
        if collection_name in existing_collections:
            client.delete_collection(collection_name)

        collection=client.create_collection(name=collection_name, embedding_function=BioBertEmbeddingFunction())

    ids = [text_chunk[1] for text_chunk in text_chunks]
    docs = [text_chunk[0] for text_chunk in text_chunks]

    assert len(ids) == len(docs)

    collection.add(documents=docs, ids=ids)
    return collection

def search_chromadb(embedding_type: str, collection, query, top_k=5):
    if embedding_type=="biobert":
        embedding_function=BioBertEmbeddingFunction()
    else:
        embedding_function=BioBertEmbeddingFunction()
    
    query_embedding = embedding_function([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results


def main():

    config_path = 'config.json'
    if docker:
        config_path = '/app/' + config_path
    
    # Lire le fichier de configuration JSON
    with open(config_path, 'r') as f:
        config = json.load(f)

    tables_path = config.get("tables_path")    
    text_chunks = load_text_chunks(tables_path)

    collection = update_chromadb(text_chunks)  # adds some text chunks to chromadb

    query = "Humerus et Glène vs Humérus (Ref)"
    pprint(search_chromadb("biobert", collection, query)["documents"])

if __name__ == "__main__":
    main()
