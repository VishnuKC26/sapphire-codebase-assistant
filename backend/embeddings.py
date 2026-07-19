from sentence_transformers import SentenceTransformer

from backend.schemas import CodeChunk, EmbeddedChunk

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def embed_repository(
    chunks: list[CodeChunk],
) -> list[EmbeddedChunk]:

    texts = [chunk.content for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            EmbeddedChunk(
                **chunk.model_dump(),
                embedding=embedding.tolist(),
            )
        )

    return embedded_chunks