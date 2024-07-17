import pickle 
from pathlib import Path
import json 
from pprint import pprint 
from biobert_embedding.embedding import BiobertEmbedding
import torch 

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer


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


class BioMstralEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.biomistral = BiobertEmbedding()

    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = []
        for text in texts:
            tensor = self.biomistral.embed((str(text)))
            if isinstance(tensor, torch.Tensor):
                # Convert tensor to numpy array and then to a list
                embedding = tensor.detach().cpu().numpy().tolist()
            else:
                embedding = tensor  # Assuming it is already in the correct format
            embeddings.append(embedding)
        return embeddings
    


def load_text_chunks(pickle_file):
    # Refer to extract_tables_chunks
    """
    Displays first tables text chunk stored in pickle file.
    text_chunks = [(text, id), ...]
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
    config_path = Path('.vscode/config.json')

    # Lire le fichier de configuration JSON
    with open(config_path, 'r') as f:
        config = json.load(f)

    tables_path = config.get("tables_path")    
    text_chunks = load_text_chunks(tables_path)

    collection = create_chromadb("biobert", text_chunks)

    query = "Humerus et Glène vs Humérus (Ref)"
    print(search_chromadb("biobert", collection, query)["documents"])
    
if __name__ == "__main__":
    main()
