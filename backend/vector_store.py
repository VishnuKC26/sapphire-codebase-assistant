try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import chromadb

from backend.schemas import EmbeddedChunk

from google import genai

from backend.config import GEMINI_API_KEY

from backend.embeddings import model

from backend.schemas import  EmbeddedChunk


client_gemini = genai.Client(api_key=GEMINI_API_KEY)


client = chromadb.PersistentClient(path="database")

collection = client.get_or_create_collection(
    name="repositories"
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

    query_embedding = model.encode(
    query,
    normalize_embeddings=True,
).tolist()

    
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
        name="repositories"
    )