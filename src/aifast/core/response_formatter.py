from typing import Any, Dict, List, Union
import json
import re
import yaml

class ResponseFormatter:
    def __init__(self, format_type: str = "text"):
        """
        Initialize formatter with format type.
        Supported formats: text, json, markdown, yaml, mermaid
        """
        self.format_type = format_type.lower()
        self._formatters = {
            "text": self._format_text,
            "json": self._format_json,
            "markdown": self._format_markdown,
            "yaml": self._format_yaml,
            "mermaid": self._format_mermaid
        }
    
    def format(self, response: str) -> Union[str, Dict, List]:
        """Format the response according to specified format type"""
        if self.format_type not in self._formatters:
            raise ValueError(f"Unsupported format type: {self.format_type}")
        
        return self._formatters[self.format_type](response)
    
    def _format_text(self, response: str) -> str:
        """Simple text formatting, strips whitespace"""
        return response.strip()
    
    def _format_json(self, response: str) -> Dict:
        """
        Attempts to parse response as JSON.
        If response isn't JSON, wraps it in a simple structure
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"text": response.strip()}
    
    def _format_markdown(self, response: str) -> str:
        """
        Formats response as markdown.
        - Detects and formats code blocks
        - Formats lists
        - Handles basic markdown syntax
        """
        # Add code block formatting if not present
        if "```" not in response and re.search(r'^\s*def\s+\w+|^\s*class\s+\w+', response, re.MULTILINE):
            response = f"```python\n{response}\n```"
        
        # Format lists if they look like lists but aren't formatted
        lines = response.split('\n')
        formatted_lines = []
        for line in lines:
            if re.match(r'^\s*[\d+]\.?\s+', line) and not line.strip().startswith("1."):
                line = re.sub(r'^\s*(\d+)\.?\s+', r'\1. ', line)
            elif re.match(r'^\s*[-*]\s+', line) and not line.strip().startswith("-"):
                line = re.sub(r'^\s*[-*]\s+', '- ', line)
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_yaml(self, response: str) -> Dict:
        """
        Attempts to parse response as YAML.
        If response isn't YAML, creates a simple YAML structure
        """
        try:
            return yaml.safe_load(response)
        except yaml.YAMLError:
            return {"content": response.strip()}
    
    def _format_mermaid(self, response: str) -> str:
        """
        Formats response as a Mermaid diagram.
        Wraps the diagram definition in mermaid code block.
        """
        # If response already contains mermaid block, just clean it
        if "```mermaid" in response:
            # Extract content between mermaid blocks
            match = re.search(r"```mermaid\n(.*?)\n```", response, re.DOTALL)
            if match:
                return f"```mermaid\n{match.group(1).strip()}\n```"
        
        # If it looks like a mermaid diagram but not properly formatted
        mermaid_indicators = [
            "graph ",
            "sequenceDiagram",
            "classDiagram",
            "erDiagram",
            "gantt",
            "pie",
            "flowchart",
            "stateDiagram"
        ]
        
        if any(indicator in response for indicator in mermaid_indicators):
            return f"```mermaid\n{response.strip()}\n```"
        
        # If it's not recognizable as a mermaid diagram,
        # attempt to convert simple text to a flowchart
        lines = response.strip().split('\n')
        if len(lines) > 0:
            # Create a simple top-down flowchart
            mermaid = ["graph TD"]
            for i, line in enumerate(lines):
                # Clean the line text for mermaid
                clean_text = re.sub(r'[^\w\s-]', '', line).strip()
                if clean_text:
                    node_id = f"A{i}"
                    mermaid.append(f"    {node_id}[{clean_text}]")
                    if i > 0:
                        prev_node = f"A{i-1}"
                        mermaid.append(f"    {prev_node} --> {node_id}")
            
            return "```mermaid\n" + "\n".join(mermaid) + "\n```"
        
        return response
    
    def set_format(self, format_type: str):
        """Change the format type"""
        if format_type.lower() not in self._formatters:
            raise ValueError(f"Unsupported format type: {format_type}")
        self.format_type = format_type.lower() 