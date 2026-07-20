from pathlib import Path
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from backend.github import download_repository_zip
from backend.chunker import chunk_repository
from backend.embeddings import embed_repository
from backend.vector_store import clear_collection, index_chunks
from backend.chunker import chunk_repository
from backend.embeddings import embed_repository
from backend.llm import ask_gemini
from backend.parser import load_repository, load_repository_from_zip
from backend.schemas import ChatRequest, GitHubRequest
from backend.vector_store import index_chunks, search
from backend.vector_store import (
    index_chunks,
    search,
    clear_collection,
)

import shutil



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



@app.post("/github")
async def github_upload(request: GitHubRequest):
    """
    Download a public GitHub repository as a ZIP,
    extract it, index it and store embeddings.
    """

    temp_dir = None

    try:
        clear_collection()

        zip_path, temp_dir = download_repository_zip(request.url)

        files = load_repository_from_zip(zip_path)

        chunks = chunk_repository(files)

        embedded_chunks = embed_repository(chunks)

        index_chunks(embedded_chunks)

        return {
            "message": "Repository indexed successfully.",
            "files": len(files),
            "chunks": len(chunks),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)