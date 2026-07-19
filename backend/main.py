from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.chunker import chunk_repository
from backend.embeddings import embed_repository
from backend.llm import ask_gemini
from backend.parser import load_repository
from backend.schemas import ChatRequest
from backend.vector_store import index_chunks, search
from backend.vector_store import (
    index_chunks,
    search,
    clear_collection,
)
app = FastAPI(title="Sapphire Codebase Assistant")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Sapphire Codebase Assistant API is running."
    }


@app.post("/upload")
async def upload_repository(
    file: UploadFile = File(...)
):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    zip_path = upload_dir / file.filename

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    repository = load_repository(str(zip_path))

    chunks = chunk_repository(repository)

    embedded_chunks = embed_repository(chunks)

    clear_collection()
    index_chunks(embedded_chunks)

    return {
        "files": len(repository),
        "chunks": len(chunks),
        "message": "Repository indexed successfully."
    }


@app.post("/chat")
def chat(request: ChatRequest):

    results = search(request.message)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = ""

    for metadata, document in zip(metadatas, documents):
        context += (
            f"File: {metadata['path']}\n"
            f"Lines: {metadata['start_line']}-{metadata['end_line']}\n\n"
            f"{document}\n\n"
        )

    prompt = f"""
You are an expert software engineer.

Answer ONLY using the repository context provided below.

If the answer is not present in the repository context, say:
"I couldn't find that information in the uploaded repository."

Repository Context:

{context}

Question:

{request.message}
"""

    answer = ask_gemini(prompt)

    return {
        "answer": answer
    }