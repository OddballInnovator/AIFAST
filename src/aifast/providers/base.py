from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProvider(ABC):
    @abstractmethod
    def __init__(self, api_key: str, **kwargs):
        """Initialize the provider with API key and optional parameters."""
        pass

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """Generate completion for the given prompt."""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat response for the given messages."""
        pass

    @abstractmethod
    def validate_api_key(self) -> bool:
        """Validate the API key."""
        pass
