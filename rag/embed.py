import pickle 
from pathlib import Path
import json 
from pprint import pprint 
from biobert_embedding.embedding import BiobertEmbedding
import numpy as np

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

# Define a custom embedding function for BioBert
class BioBertEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.biobert = BiobertEmbedding()

    def __call__(self, texts: Documents) -> Embeddings:
        return np.array(([[self.biobert.sentence_vector(chunk)] for chunk in texts])).tolist()
    

def load_text_chunks(pickle_file):
    """
    Displays first tables text chunk stored in pickle file.
    """
    with open(pickle_file, "rb") as f:
        text_chunks = pickle.load(f)

    return text_chunks


def create_chromadb(embedding_type: str, text_chunks):
    """
    embedding_type can be biobert / biomistral
    text_chunks = [("document", "id"), ...]
    """

    client = chromadb.PersistentClient(path=".")
    print("Client heartbeat: ", client.heartbeat())


    if embedding_type=="biobert":
        client.delete_collection("biobert-collection")
        collection=client.create_collection(name="biobert-collection",embedding_function=BioBertEmbeddingFunction())
    else:
        collection=client.create_collection(name="biomistral-collection",embedding_function=BioBertEmbeddingFunction())

    ids = [text_chunk[1] for text_chunk in text_chunks]
    docs = [text_chunk[0] for text_chunk in text_chunks]

    collection.add(documents=docs, ids=ids)
    collection.peek()


def main():
    config_path = Path('.vscode/config.json')

    # Lire le fichier de configuration JSON
    with open(config_path, 'r') as f:
        config = json.load(f)

    tables_path = config.get("tables_path")    
    text_chunks = load_text_chunks(tables_path)

    create_chromadb("biobert", text_chunks)
    
if __name__ == "__main__":
    main()
