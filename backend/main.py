from fastapi import FastAPI
from backend.schemas import ChatRequest, ChatResponse
from backend.llm import ask_gemini

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Welcome to Sapphire Codebase Assistant API"
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = ask_gemini(request.message)

    return ChatResponse(answer=answer)