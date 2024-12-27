from langchain_community.embeddings.ollama import OllamaEmbeddings
def local_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    #embeddings = OllamaEmbeddings(model="llama2:latest")
    return embeddings
