# Horiana RAG

A Python project for Retrieval-Augmented Generation (RAG) for document processing and embedding.
Development in progress.

## Installation

1) Change config.json with files path:

```
{
    "pdf_path": "confidential/file.pdf",
    "doc_path": "confidential/file.docx",
    "output_path": "out.pkl",
    "tables_path": "tables.pkl"
}
```

2) Update credentials in .chroma_env:

```
CHROMA_SERVER_AUTHN_CREDENTIALS="secret token"
CHROMA_SERVER_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider"
CHROMA_AUTH_TOKEN_TRANSPORT_HEADER="Authorization"

CHROMA_CLIENT_AUTHN_CREDENTIALS="secret token"
CHROMA_CLIENT_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthClientProvider"    
```

3) Run chroma server with docker: https://cookbook.chromadb.dev/security/auth/#token-authentication
docker run --rm -e CHROMA_SERVER_AUTHN_CREDENTIALS="chr0ma-t0k3n"  -e CHROMA_SERVER_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider"  -e CHROMA_AUTH_TOKEN_TRANSPORT_HEADER="Authorization"  -p 8000:8000  chromadb/chroma:latest

chr0ma-t0k3n needs to be the same token in config.json!

4) docker build -t my-python-app .
docker run -it --network="host" --rm -v $(pwd):/app my-python-app bash
