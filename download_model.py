import os
from sentence_transformers import SentenceTransformer

def main():
    print("Pre-downloading SentenceTransformer model: BAAI/bge-small-en-v1.5...")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    print("Model loaded and cached successfully!")

if __name__ == "__main__":
    main()
