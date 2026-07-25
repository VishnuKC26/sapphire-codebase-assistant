from fastembed import TextEmbedding

from backend.schemas import CodeChunk, EmbeddedChunk

# Using FastEmbed for local-first, free-of-cost, fast embedding generation using ONNX Runtime
model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def embed_repository(
    chunks: list[CodeChunk],
) -> list[EmbeddedChunk]:

    texts = [chunk.content for chunk in chunks]

    embeddings = list(model.embed(texts))

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            EmbeddedChunk(
                **chunk.model_dump(),
                embedding=embedding.tolist(),
            )
        )

    return embedded_chunks