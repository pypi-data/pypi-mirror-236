from langchain.embeddings import HuggingFaceHubEmbeddings

def Huggingface_embedding(conf=None):
    repo_id = "sentence-transformers/all-MiniLM-L12-v2"
    huggingface_embedding = HuggingFaceHubEmbeddings(
        repo_id=repo_id,
        task="feature-extraction",
        huggingfacehub_api_token="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",
    )
    return huggingface_embedding