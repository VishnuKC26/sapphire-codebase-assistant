try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import chromadb

from backend.schemas import EmbeddedChunk
from backend.embeddings import model

from chromadb import EmbeddingFunction

class DummyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        pass
    def __call__(self, input):
        return []

client = chromadb.PersistentClient(path="database")

try:
    collection = client.get_or_create_collection(
        name="repositories",
        embedding_function=DummyEmbeddingFunction()
    )
except ValueError:
    try:
        client.delete_collection("repositories")
    except Exception:
        pass
    collection = client.get_or_create_collection(
        name="repositories",
        embedding_function=DummyEmbeddingFunction()
    )


def index_chunks(chunks: list[EmbeddedChunk]) -> None:
    

    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],

        embeddings=[
            chunk.embedding
            for chunk in chunks
        ],

        documents=[
            chunk.content
            for chunk in chunks
        ],

        metadatas=[
            {
                "file_id": chunk.file_id,
                "path": chunk.path,
                "filename": chunk.filename,
                "extension": chunk.extension,
                "language": chunk.language,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
            }
            for chunk in chunks
        ],
    )

def search(
    query: str,
    top_k: int = 5,
):

    query_embeddings = list(model.query_embed(query))
    query_embedding = query_embeddings[0].tolist()

    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


def clear_collection() -> None:
    """
    Remove all indexed chunks.
    """

    client.delete_collection("repositories")

    global collection

    collection = client.get_or_create_collection(
        name="repositories",
        embedding_function=DummyEmbeddingFunction()
    )