from langchain_chroma import Chroma
from rag.embed import connect_to_chromadb, StellaEmbeddingFunction, TestingEmbeddingFunction

cpu = True 

def main():
    persistent_client = connect_to_chromadb()

    if cpu:
        embedding_function = TestingEmbeddingFunction()
    else:
        embedding_function = StellaEmbeddingFunction()

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name="test",
        embedding_function=embedding_function,
    )

    count = langchain_chroma._collection.count()
    print("There are", count, "in the collection")

    query = "Knees"
    docs = langchain_chroma.similarity_search_with_relevance_scores(query, k=3)
    print(docs[0].page_content)


if __name__ == "__main__":
    main()
