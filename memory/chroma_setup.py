# memory/chroma_setup.py
import chromadb

def get_chroma_client(path="./chroma_db"):
    # PersistentClient path will create local chroma DB
    try:
        client = chromadb.PersistentClient(path=path)
        return client
    except Exception:
        # fallback to in-memory
        return chromadb.Client()
