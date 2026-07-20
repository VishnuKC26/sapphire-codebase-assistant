# 💎 Sapphire Codebase Assistant

A **Retrieval-Augmented Generation (RAG)** application that enables developers to chat with any GitHub repository or uploaded ZIP archive using natural language.

The application automatically downloads or extracts a codebase, chunks the source code, generates semantic embeddings using **BAAI/bge-small-en-v1.5**, stores them in **ChromaDB**, retrieves the most relevant code snippets for each query, and uses an LLM to generate context-aware, grounded answers.

---

## 🚀 Features

- 🧠 Retrieval-Augmented Generation (RAG) pipeline for source code
- 📂 Index public GitHub repositories
- 📦 Upload local project ZIP archives
- 🔍 Semantic code search using vector embeddings
- 💬 Natural language question answering over codebases
- 🗃️ ChromaDB vector database
- ⚡ FastAPI backend
- 🎨 Modern HTML/CSS/JavaScript frontend
- 📊 Repository statistics and indexing information

## 🧠 RAG Pipeline

The project follows a Retrieval-Augmented Generation (RAG) architecture.

1. **Ingestion**
   - Download a GitHub repository or upload a ZIP archive.
   - Extract and parse supported source files.

2. **Chunking**
   - Split source files into semantic code chunks while preserving metadata such as file paths and line numbers.

3. **Embedding**
   - Convert each chunk into dense vector embeddings using **BAAI/bge-small-en-v1.5**.

4. **Indexing**
   - Store embeddings in **ChromaDB** for efficient semantic retrieval.

5. **Retrieval**
   - Embed the user's query and retrieve the most relevant code chunks using vector similarity search.

6. **Generation**
   - Supply the retrieved context to the LLM, enabling grounded and context-aware answers about the repository.