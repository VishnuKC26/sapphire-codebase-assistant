from fastembed import TextEmbedding

def main():
    print("Pre-downloading FastEmbed model: BAAI/bge-small-en-v1.5...")
    model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print("Model loaded and cached successfully!")

if __name__ == "__main__":
    main()
