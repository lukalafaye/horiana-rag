from langchain_chroma import Chroma
from rag.embed import connect_to_chromadb, StellaEmbeddingFunction


def main():
    persistent_client = connect_to_chromadb()

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name="table",
        embedding_function=StellaEmbeddingFunction,
    )

    count = langchain_chroma._collection.count()
    print("There are", count, "in the collection")

    query = "Knees"
    docs = langchain_chroma.similarity_search(query)
    print(docs[0].page_content)


if __name__ == "__main__":
    main()
