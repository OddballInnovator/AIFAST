from typing import List, Dict, Any
from .base import BaseProvider
from openai import OpenAI

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def complete(self, prompt: str, **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get('max_tokens', 150),
                temperature=kwargs.get('temperature', 0.7)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 150)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
            
    def validate_api_key(self) -> bool:
        try:
            # Simple validation by making a minimal API call
            self.client.models.list()
            return True
        except:
            return False
