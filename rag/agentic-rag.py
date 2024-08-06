import warnings

warnings.filterwarnings("ignore")

from langchain_chroma import Chroma
from rag.embed import (
    connect_to_chromadb,
    StellaEmbeddingFunction,
    TestingEmbeddingFunction,
)
from pprint import pprint

cpu = True


def main():
    persistent_client = connect_to_chromadb()
    query = "The objective of this study was to investigate the differences in muscle activation and kinematic parameters between patients with unilateral knee osteoarthritis (OA) and healthy individuals"
    collection_name = "abstracts"

    fetch_context(query, persistent_client, collection_name)


def fetch_context(query, client, collection_name):
    """
    Query a Retrieval-Augmented Generation (RAG) system using Chroma database and OpenAI.
    Args:
    - query_text (str): The text to query the RAG system with.
    Returns:
    - formatted_response (str): Formatted response including the generated text and sources.
    - response_text (str): The generated response text.
    """
    # YOU MUST - Use same embedding function as before
    if cpu:
        embedding_function = TestingEmbeddingFunction()
    else:
        embedding_function = StellaEmbeddingFunction()

    chroma_db = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embedding_function,
        collection_metadata={"hnsw:space": "cosine"},
    )

    results = chroma_db.similarity_search_with_score(query=query, k=2)
    # Lower score represents more similarity.

    context_text = "\n\n".join([doc.page_content for doc, _score in results])
    print(context_text)

    return context_text


if __name__ == "__main__":
    main()
