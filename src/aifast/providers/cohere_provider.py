from typing import List, Dict, Any
from .base import BaseProvider
import cohere

class CohereProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "command"):
        self.api_key = api_key
        self.model = model
        self.client = cohere.Client(api_key)
    
    def complete(self, prompt: str, **kwargs) -> str:
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                max_tokens=kwargs.get('max_tokens', 150),
                temperature=kwargs.get('temperature', 0.7)
            )
            return response.generations[0].text.strip()
        except Exception as e:
            raise Exception(f"Cohere API error: {str(e)}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            # Convert standard messages to Cohere chat format
            chat_history = []
            for msg in messages:
                role = msg["role"]
                if role == "system":
                    # Add system message as a preamble
                    chat_history.append({"role": "CHATBOT", "message": msg["content"]})
                else:
                    chat_history.append({
                        "role": "USER" if role == "user" else "CHATBOT",
                        "message": msg["content"]
                    })
            
            response = self.client.chat(
                model=self.model,
                message=messages[-1]["content"],  # Current message
                chat_history=chat_history[:-1],   # Previous messages
                temperature=kwargs.get('temperature', 0.7)
            )
            return response.text
        except Exception as e:
            raise Exception(f"Cohere API error: {str(e)}")
            
    def validate_api_key(self) -> bool:
        try:
            # Simple validation
            self.client.generate(prompt="test", max_tokens=1)
            return True
        except:
            return False 