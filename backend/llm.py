from google import genai
from backend.config import GEMINI_API_KEY

client = None

def get_client() -> genai.Client:
    global client
    if client is None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set. Please configure it in your Render settings.")
        client = genai.Client(api_key=GEMINI_API_KEY)
    return client

def ask_gemini(prompt: str) -> str:
    try:
        api_client = get_client()
        response = api_client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"