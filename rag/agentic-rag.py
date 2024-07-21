import chromadb


def main():
    langchain_chroma = Chroma(
    client=persistent_client,
    collection_name="collection_name",
    embedding_function=embedding_function,
    )

if __name__ == "__main__":
    main()
