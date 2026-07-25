from fastembed import TextEmbedding

from backend.schemas import CodeChunk, EmbeddedChunk

model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5", threads=1)


def embed_repository(
    chunks: list[CodeChunk],
) -> list[EmbeddedChunk]:

    texts = [chunk.content for chunk in chunks]

    embeddings_generator = model.embed(
        texts,
        batch_size=32,
    )
    embeddings = list(embeddings_generator)

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            EmbeddedChunk(
                **chunk.model_dump(),
                embedding=embedding.tolist(),
            )
        )

    return embedded_chunks