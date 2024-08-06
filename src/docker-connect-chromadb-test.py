import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os

# Load environment variables from .chroma_env file
chroma_env = ".chroma_env"
load_dotenv(chroma_env)

# Retrieve the environment variables
chroma_client_auth_provider = os.getenv("CHROMA_CLIENT_AUTHN_PROVIDER")
chroma_client_auth_credentials = os.getenv("CHROMA_CLIENT_AUTHN_CREDENTIALS")

# Print the retrieved values for debugging purposes
print("Auth Provider:", chroma_client_auth_provider)
print("Auth Credentials:", chroma_client_auth_credentials)

# Ensure that both variables are not None and correctly formatted
if not chroma_client_auth_provider or not chroma_client_auth_credentials:
    raise ValueError(
        "Environment variables for ChromaDB authentication are not set correctly."
    )
if "." not in chroma_client_auth_provider:
    raise ValueError(
        "The 'CHROMA_CLIENT_AUTHN_PROVIDER' should be a fully qualified class name."
    )

# Create ChromaDB HttpClient with the settings
try:
    client = chromadb.HttpClient(
        settings=Settings(
            chroma_client_auth_provider=chroma_client_auth_provider,
            chroma_client_auth_credentials=chroma_client_auth_credentials,
        )
    )

    print(client.list_collections())
    print("ChromaDB client initialized successfully.")
except Exception as e:
    print(f"Error initializing ChromaDB client: {e}")
