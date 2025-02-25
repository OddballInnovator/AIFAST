from typing import List, Any
import re

class ContentProcessor:
    def __init__(self):
        self.pipeline = []
    
    def add_processor(self, processor_func):
        self.pipeline.append(processor_func)
    
    def process(self, content: str, pipeline: List[str] = None) -> Any:
        if pipeline:
            for step in pipeline:
                if hasattr(self, step):
                    content = getattr(self, step)(content)
        return content
    
    def clean(self, text: str) -> str:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        # Basic word tokenization
        return text.split()
    
    def remove_special_chars(self, text: str) -> str:
        # Remove special characters
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    def lowercase(self, text: str) -> str:
        return text.lower()
    
    def summarize(self, text: str, max_length: int = 100) -> str:
        # Basic summarization (truncation)
        words = text.split()
        if len(words) <= max_length:
            return text
        return ' '.join(words[:max_length]) + '...'
