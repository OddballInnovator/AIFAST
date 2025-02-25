import os
import pathlib

def create_core_files():
    # Create ai_interface.py
    with open('src/aifast/core/ai_interface.py', 'w') as f:
        f.write('''class AIInterface:
    def __init__(self, provider):
        self.provider = provider
    
    def complete(self, prompt: str) -> str:
        return self.provider.complete(prompt)
    
    def chat(self, messages: list) -> str:
        return self.provider.chat(messages)
''')

    # Create llm_connector.py
    with open('src/aifast/core/llm_connector.py', 'w') as f:
        f.write('''from typing import Dict, Optional
import time
from datetime import datetime, timedelta

class LLMConnector:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.api_key = api_key
        self.last_request_time = None
        self.request_count = 0
        self.rate_limit = {
            "requests_per_min": 60,
            "tokens_per_min": 90000
        }
    
    def validate_connection(self) -> bool:
        """Validate the connection and API key."""
        try:
            # Implement actual validation logic here
            return True
        except Exception as e:
            return False
    
    def check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        current_time = datetime.now()
        
        if self.last_request_time:
            time_diff = current_time - self.last_request_time
            if time_diff < timedelta(minutes=1):
                if self.request_count >= self.rate_limit["requests_per_min"]:
                    return False
        else:
            self.request_count = 0
            
        self.last_request_time = current_time
        self.request_count += 1
        return True
    
    def get_rate_limits(self) -> Dict[str, int]:
        """Get current rate limits."""
        return self.rate_limit
    
    def set_rate_limits(self, requests_per_min: int, tokens_per_min: int):
        """Update rate limits."""
        self.rate_limit = {
            "requests_per_min": requests_per_min,
            "tokens_per_min": tokens_per_min
        }
''')

    # Create base.py in providers
    with open('src/aifast/providers/base.py', 'w') as f:
        f.write('''from abc import ABC, abstractmethod
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
''')

    # Create openai_provider.py
    with open('src/aifast/providers/openai_provider.py', 'w') as f:
        f.write('''from typing import List, Dict, Any
from .base import BaseProvider
import openai

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
    
    def complete(self, prompt: str, **kwargs) -> str:
        try:
            response = openai.Completion.create(
                model=self.model if "gpt" not in self.model else "text-davinci-003",
                prompt=prompt,
                max_tokens=kwargs.get('max_tokens', 150),
                temperature=kwargs.get('temperature', 0.7)
            )
            return response.choices[0].text.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 150)
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
            
    def validate_api_key(self) -> bool:
        try:
            # Simple validation by making a minimal API call
            openai.Model.list()
            return True
        except:
            return False
''')

def create_init_files():
    # Main package __init__.py
    with open('src/aifast/__init__.py', 'w') as f:
        f.write('''"""AIFAST package."""
from aifast.core.ai_interface import AIInterface
from aifast.providers.openai_provider import OpenAIProvider
from aifast.core.content_processor import ContentProcessor
from aifast.core.prompt_manager import PromptManager
from aifast.core.llm_connector import LLMConnector

__all__ = [
    'AIInterface',
    'OpenAIProvider',
    'ContentProcessor',
    'PromptManager',
    'LLMConnector'
]
''')

    # Core __init__.py
    with open('src/aifast/core/__init__.py', 'w') as f:
        f.write('''"""AIFAST core modules."""
from .ai_interface import AIInterface
from .content_processor import ContentProcessor
from .prompt_manager import PromptManager
from .llm_connector import LLMConnector

__all__ = [
    'AIInterface',
    'ContentProcessor',
    'PromptManager',
    'LLMConnector'
]
''')

    # Providers __init__.py
    with open('src/aifast/providers/__init__.py', 'w') as f:
        f.write('''"""AIFAST provider modules."""
from .base import BaseProvider
from .openai_provider import OpenAIProvider

__all__ = [
    'BaseProvider',
    'OpenAIProvider'
]
''')

def create_directory_structure():
    # Define the base directory structure
    directories = [
        'src/aifast/core',
        'src/aifast/providers',
        'src/aifast/utils',
        'src/aifast/config',
        'tests',
        'examples'
    ]
    
    # Create directories
    for dir_path in directories:
        pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files with content
    create_init_files()
    
    # Create core files with content
    create_core_files()
    
    # Create empty files for core modules
    core_files = [
        'src/aifast/core/config.py',
        'src/aifast/core/llm_connector.py',
        'src/aifast/core/prompt_manager.py',
        'src/aifast/core/content_processor.py'
    ]
    
    for file_path in core_files:
        pathlib.Path(file_path).touch()
    
    # Create provider files
    provider_files = [
        'src/aifast/providers/base.py',
        'src/aifast/providers/openai_provider.py',
        'src/aifast/providers/anthropic_provider.py'
    ]
    
    for file_path in provider_files:
        pathlib.Path(file_path).touch()
    
    # Create config files
    with open('src/aifast/config/config.yaml', 'w') as f:
        f.write('# Default AIFAST configuration\n')
    
    with open('src/aifast/config/prompts.yaml', 'w') as f:
        f.write('# AIFAST prompt templates\n')
    
    # Create example files
    example_files = [
        'examples/basic_usage.py',
        'examples/advanced_usage.py'
    ]
    
    for file_path in example_files:
        pathlib.Path(file_path).touch()
    
    # Create test files
    test_files = [
        'tests/test_ai_interface.py',
        'tests/test_llm_connector.py',
        'tests/test_prompt_manager.py'
    ]
    
    for file_path in test_files:
        pathlib.Path(file_path).touch()

    # Create README.md
    with open('README.md', 'w') as f:
        f.write('''# AIFAST

A fast and efficient AI integration framework.

## Installation

```bash
pip install -e .
```

## Usage

See examples directory for usage examples.
''')

    # Create LICENSE file
    with open('LICENSE', 'w') as f:
        f.write('''MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge...''')  # Add full MIT license text

    # Create .gitignore
    with open('.gitignore', 'w') as f:
        f.write('''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
venv/
''')

if __name__ == '__main__':
    create_directory_structure()
