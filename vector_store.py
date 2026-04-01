# vector_store.py

from langchain_core.vectorstores import InMemoryVectorStore
from embeddings import embeddings
from chunks import get_chunks

# --- Lazy singleton pattern ---
# This prevents chunks from being loaded & embedded on every import.
_vector_store = None


def get_vector_store() -> InMemoryVectorStore:
    """Build and cache the vector store (runs only once per process)."""
    global _vector_store
    if _vector_store is None:
        all_splits = get_chunks()
        _vector_store = InMemoryVectorStore(embeddings)
        document_ids = _vector_store.add_documents(documents=all_splits)
        print(f"✅ Added {len(document_ids)} documents to vector store.")
        print("First 3 IDs:", document_ids[:3])
    return _vector_store


# Convenience alias — still works as `from vector_store import vector_store`
# but now defers loading until first access.
vector_store = get_vector_store()
