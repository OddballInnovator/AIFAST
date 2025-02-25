import yaml
from typing import Dict, Any

class PromptManager:
    def __init__(self, prompt_file: str):
        self.prompts = self._load_prompts(prompt_file)
    
    def _load_prompts(self, file_path: str) -> Dict[str, str]:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_prompt(self, key: str) -> str:
        """Get a prompt template by key."""
        return self.prompts.get(key, "")
    
    def format_prompt(self, key: str, **kwargs) -> str:
        """Format a prompt template with provided variables."""
        template = self.get_prompt(key)
        return template.format(**kwargs)
    
    def add_prompt(self, key: str, template: str):
        """Add a new prompt template."""
        self.prompts[key] = template
    
    def save_prompts(self, file_path: str):
        """Save prompts to a YAML file."""
        with open(file_path, 'w') as f:
            yaml.dump(self.prompts, f)
