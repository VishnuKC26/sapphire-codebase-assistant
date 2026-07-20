# 💎 Sapphire Codebase Assistant

An AI-powered codebase assistant that lets you chat with any GitHub repository or uploaded ZIP archive. It indexes the source code using semantic embeddings and retrieves the most relevant code snippets to answer natural language questions about the project.

---

## ✨ Features

- 📂 Index GitHub repositories via URL
- 📦 Upload ZIP archives of local projects
- 💬 Chat with your codebase in natural language
- 🔍 Semantic code search using vector embeddings
- 🧠 Context-aware responses powered by an LLM
- ⚡ FastAPI backend with a modern HTML/CSS/JavaScript frontend
- 🗃️ ChromaDB vector database for efficient retrieval
- 📊 Repository statistics (files indexed, chunks created)

---

## Demo

### Home
<img src="assets/home.png" width="900">

### Repository Indexing
<img src="assets/index.png" width="900">

### Chat Interface
<img src="assets/chat.png" width="900">

> Replace the screenshots above with your own images.

---

## Tech Stack

### Backend

- FastAPI
- Python
- ChromaDB
- Sentence Transformers
- Hugging Face
- Requests

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Marked.js (Markdown Rendering)

### AI

- BAAI/bge-small-en-v1.5 Embedding Model
- Retrieval-Augmented Generation (RAG)

---

## Architecture

```
                 GitHub URL / ZIP Upload
                           │
                           ▼
                  Repository Downloader
                           │
                           ▼
                  Repository Parser
                           │
                           ▼
                     Code Chunking
                           │
                           ▼
                SentenceTransformer
                    Embeddings
                           │
                           ▼
                      ChromaDB
                           │
             Semantic Similarity Search
                           │
                           ▼
                      Retrieved Context
                           │
                           ▼
                           LLM
                           │
                           ▼
                     Formatted Answer
```

---

## Project Structure

```
Sapphire-Codebase-Assistant/
│
├── backend/
│   ├── main.py
│   ├── downloader.py
│   ├── repository_loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── chroma_db.py
│   ├── llm.py
│   ├── schemas.py
│   └── ...
│
├── templates/
│   └── index.html
│
├── uploads/
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<username>/Sapphire-Codebase-Assistant.git

cd Sapphire-Codebase-Assistant
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server

```bash
uvicorn backend.main:app --reload
```

Open

```
http://127.0.0.1:8000
```

---

## How It Works

### Step 1

Provide either

- a GitHub repository URL
- or upload a ZIP archive

### Step 2

The repository is

- downloaded/extracted
- parsed
- chunked into semantic code blocks

### Step 3

Each chunk is converted into embeddings using

```
BAAI/bge-small-en-v1.5
```

### Step 4

Embeddings are stored inside ChromaDB.

### Step 5

When a question is asked,

- relevant code chunks are retrieved
- passed as context to the LLM
- a grounded response is generated.

---

## Example Questions

- Explain the authentication flow.
- Where is the database connection created?
- How are API routes registered?
- Explain the payment service.
- Which files implement JWT authentication?
- What happens when a user logs in?
- Show me where WebSockets are used.
- Explain the project architecture.
- How does caching work?
- Find all Redis usage.

---

## Performance

Typical indexing workflow

| Stage | Time |
|--------|------|
| Download Repository | ~1–3 sec |
| Repository Parsing | <1 sec |
| Chunk Generation | <1 sec |
| Embedding | Depends on CPU |
| ChromaDB Indexing | <1 sec |

---

## Future Improvements

- Streaming LLM responses
- Multi-repository indexing
- Conversation history
- Repository summaries
- File-level citations
- Syntax highlighted code blocks
- Dark/Light themes
- Docker deployment
- Cloud deployment (Cloud Run / AWS)

---

## License

This project is licensed under the MIT License.

---

## Author

**Vishnu Kant Chaudhary**

GitHub: https://github.com/VishnuKC26