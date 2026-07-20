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
from backend.parser import load_repository_from_zip
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


from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()


# @app.post("/upload")
# async def upload_repository(
#     file: UploadFile = File(...)
# ):
#     upload_dir = Path("uploads")
#     upload_dir.mkdir(exist_ok=True)

#     zip_path = upload_dir / file.filename

#     with open(zip_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     repository = load_repository(str(zip_path))

#     chunks = chunk_repository(repository)

#     embedded_chunks = embed_repository(chunks)

#     clear_collection()
#     index_chunks(embedded_chunks)

#     return {
#         "files": len(repository),
#         "chunks": len(chunks),
#         "message": "Repository indexed successfully."
#     }
from fastapi import HTTPException
import traceback

@app.post("/upload")
async def upload_repository(file: UploadFile = File(...)):
    try:
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        zip_path = upload_dir / file.filename

        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("ZIP saved")

        repository = load_repository_from_zip(str(zip_path))
        print("Repository loaded:", len(repository))

        chunks = chunk_repository(repository)
        print("Chunks:", len(chunks))

        embedded_chunks = embed_repository(chunks)
        print("Embeddings created")

        clear_collection()
        print("Collection cleared")

        index_chunks(embedded_chunks)
        print("Indexed")

        return {
            "files": len(repository),
            "chunks": len(chunks),
            "message": "Repository indexed successfully."
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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


import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("sapphire")
logger.setLevel(logging.INFO)
@app.post("/github")
async def github_upload(request: GitHubRequest):
    temp_dir = None

    try:
        t = time.perf_counter()
        clear_collection()
        logger.info(f"Clear collection: {time.perf_counter()-t:.2f}s")

        t = time.perf_counter()
        zip_path, temp_dir = download_repository_zip(request.url)
        logger.info(f"Download: {time.perf_counter()-t:.2f}s")

        t = time.perf_counter()
        files = load_repository_from_zip(zip_path)
        logger.info(f"Load: {time.perf_counter()-t:.2f}s")

        t = time.perf_counter()
        chunks = chunk_repository(files)
        logger.info(f"Chunk: {time.perf_counter()-t:.2f}s")

        t = time.perf_counter()
        embedded_chunks = embed_repository(chunks)
        logger.info(f"Embed: {time.perf_counter()-t:.2f}s")

        t = time.perf_counter()
        index_chunks(embedded_chunks)
        logger.info(f"Index: {time.perf_counter()-t:.2f}s")

        return {
            "message": "Repository indexed successfully.",
            "files": len(files),
            "chunks": len(chunks),
        }

    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)