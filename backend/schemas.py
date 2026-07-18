from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str

from pydantic import BaseModel


class RepositoryFile(BaseModel):
    file_id: str
    path: str
    filename: str
    extension: str
    language: str
    content: str
    size: int

class EmbeddedChunk(CodeChunk):
    embedding: list[float]