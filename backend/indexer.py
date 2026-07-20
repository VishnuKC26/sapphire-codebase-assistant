
from backend.parser import load_repository
from backend.chunker import chunk_repository
from backend.embeddings import embed_repository
from backend.vector_store import (
    clear_collection,
    index_chunks,
)
def index_repository(repo_path: str):
    """
    Complete indexing pipeline.
    """

    clear_collection()

    files = load_repository(repo_path)

    chunks = chunk_repository(files)

    embedded_chunks = embed_repository(chunks)

    index_chunks(embedded_chunks)

    return {
        "files": len(files),
        "chunks": len(chunks),
    }