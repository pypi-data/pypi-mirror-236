from langchain.embeddings.openai import OpenAIEmbeddings

def Openai_embedding(conf):
    chatgpt_config = conf.get("models")["chatgpt"]
    openai_embedding = OpenAIEmbeddings(
        openai_api_key=chatgpt_config['token'],
    )
    return openai_embedding