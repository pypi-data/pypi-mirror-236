import json
from typing import Any, Dict, List
from crland.tools.embeddings.sentence_transformers import RemoteEmbeddings
from crland.tools.embeddings.huggingface_embedding import Huggingface_embedding
from crland.tools.embeddings.openai_embedding import Openai_embedding

class EmbeddingManager:
    @classmethod
    def get_embedding(self, config):
        try:
            if RemoteEmbeddings.__name__ == config.get("embedding"):
                return RemoteEmbeddings()
            if Huggingface_embedding.__name__ == config.get("embedding"):
                return Huggingface_embedding()
            if Openai_embedding.__name__ == config.get("embedding"):
                return Openai_embedding(config)                
        except:
            pass    
        return RemoteEmbeddings()