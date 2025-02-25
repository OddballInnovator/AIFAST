from typing import List, Dict, Any
from .base import BaseProvider
from anthropic import Anthropic

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model
        self.client = Anthropic(api_key=api_key)
    
    def complete(self, prompt: str, **kwargs) -> str:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            # Extract system message if present
            system_message = None
            chat_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    chat_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Create message with system parameter if present
            response = self.client.messages.create(
                model=self.model,
                messages=chat_messages,
                system=system_message,  # Pass system message separately
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7)
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
            
    def validate_api_key(self) -> bool:
        try:
            # Simple validation by making a minimal API call
            self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return True
        except:
            return False
