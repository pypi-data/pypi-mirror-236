from langchain import Anthropic, OpenAI
from langchain.chat_models import ChatOpenAI

from crland.models.guanaco import Guanaco

class ModelManager:
    def __init__(self, config):
        self.config = config
        #print(config.config)
        self.models = {}
        if "chatgpt" in  self.config.get("models"):
            chatgpt_config = self.config.get("models")["chatgpt"]
            self.register_model(
                "chatgpt", 
                ChatOpenAI(
                    temperature = 0, 
                    openai_api_key = chatgpt_config["token"], 
                    model_name = chatgpt_config["model_name"],
                    openai_api_base = chatgpt_config["api_base"],
                    max_tokens = chatgpt_config["max_tokens"] if "max_tokens" in chatgpt_config else 1024,
                    )
                )
        if "vicuna" in  self.config.get("models"):
            self.register_model(
                "vicuna", 
                OpenAI(
                    openai_api_key=self.config.get("models")["vicuna"]["token"], 
                    model_name="vicuna-13b",
                    openai_api_base="http://10.8.14.49:8007/v1",
                    max_tokens_to_sample = 1024,
                    temperature=0
                    )
                )
        if "qwen" in  self.config.get("models"):
            self.register_model(
                "qwen", 
                OpenAI(
                    openai_api_key=self.config.get("models")["qwen"]["token"], 
                    model_name="Qwen",
                    openai_api_base="http://10.8.14.49:7861/v1",
                    max_tokens_to_sample = 1024,
                    temperature=0
                    )
                )
        
        if "guanaco" in self.config.get("models"):
            self.register_model(
                "guanaco", Guanaco()
            )
            
    def register_model(self, model_name, model_class):
        self.models[model_name] = model_class
        
        if not self.config.get(model_name):
            self.config.set(model_name, {})
            
    def get_model(self, model_name):
        return self.models[model_name]

