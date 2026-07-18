from uuid import uuid4

from backend.schemas import RepositoryFile, CodeChunk

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def chunk_text(text: str):
    """
    Splits text into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunks.append((start, min(end, len(text))))

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def chunk_repository(
    repository: list[RepositoryFile],
) -> list[CodeChunk]:

    all_chunks = []

    for file in repository:

        line_offsets = []
        current = 0

        for line in file.content.splitlines(True):
            line_offsets.append(current)
            current += len(line)

        ranges = chunk_text(file.content)

        for start_char, end_char in ranges:

            chunk_content = file.content[start_char:end_char]

            start_line = 1
            end_line = len(line_offsets)

            for i, offset in enumerate(line_offsets):
                if offset <= start_char:
                    start_line = i + 1
                if offset <= end_char:
                    end_line = i + 1

            all_chunks.append(
                CodeChunk(
                    chunk_id=str(uuid4()),
                    file_id=file.file_id,
                    repository=file.repository,
                    path=file.path,
                    filename=file.filename,
                    extension=file.extension,
                    language=file.language,
                    start_line=start_line,
                    end_line=end_line,
                    content=chunk_content,
                )
            )

    return all_chunks