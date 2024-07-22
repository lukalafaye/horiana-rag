# Horiana RAG

A Python project for Retrieval-Augmented Generation (RAG) for document processing and embedding.

## Installation

To install the package and its dependencies, follow these steps:

```bash
# Recreate the virtual environment
make venv

# Install core and development dependencies
make install
```

## Dev

Add a .vsvode/config.json and adapt:

```
{
    "pdf_path": "confidential/file.pdf",
    "doc_path": "confidential/file.docx",
    "output_path": "out.pkl",
    "tables_path": "tables.pkl"
}
```

Add .chroma_env with:

```
CHROMA_SERVER_AUTHN_CREDENTIALS="secret token"
CHROMA_SERVER_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider"
CHROMA_AUTH_TOKEN_TRANSPORT_HEADER="Authorization"

CHROMA_CLIENT_AUTHN_CREDENTIALS="secret token"
CHROMA_CLIENT_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthClientProvider"    
```

Run chroma server with docker: https://cookbook.chromadb.dev/security/auth/#token-authentication

Then run 1) preprocess, 2) embed