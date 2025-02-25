# AIFAST

AIFAST is a flexible and extensible Python library that provides a unified interface for working with multiple Large Language Models (LLMs) like OpenAI's GPT and Anthropic's Claude. It simplifies LLM integration with features for content processing, response formatting, and structured outputs.

## Features

### 1. Multi-Provider Support
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Extensible architecture for adding new providers

### 2. Response Formatting
Multiple output formats supported:
- Plain text
- JSON (structured data)
- Markdown (with code blocks and lists)
- YAML
- Mermaid (diagrams and flowcharts)

### 3. Content Processing
Built-in content processing capabilities:
- Text cleaning
- Tokenization
- Special character handling
- Case conversion
- Text summarization
- Pipeline processing

## Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
# or
.\venv\Scripts\activate  # On Windows

# Install from wheel
pip install aifast-0.1.0-py3-none-any.whl
```

## Quick Start

### Basic Usage
```python
from aifast import AIInterface, OpenAIProvider
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize provider and interface
provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
ai = AIInterface(provider=provider)

# Simple completion
response = ai.complete("What is Python?")
print(response)
```

### Response Formatting Example
```python
from aifast import ResponseFormatter

# Get response in JSON format
formatter = ResponseFormatter("json")
structured_response = formatter.format(response)

# Get response in Markdown
formatter.set_format("markdown")
markdown_response = formatter.format(response)

# Generate Mermaid diagram
formatter.set_format("mermaid")
diagram = formatter.format("Create a flowchart for user authentication")
```

### Content Processing Example
```python
from aifast import ContentProcessor

processor = ContentProcessor()

# Clean and process text
text = """
   This is a   MESSY text with
multiple     spaces and CAPS!
"""

cleaned = processor.clean(text)
lowercased = processor.lowercase(cleaned)
no_special = processor.remove_special_chars(lowercased)

# Use processing pipeline
result = processor.process(
    text,
    pipeline=["clean", "lowercase", "remove_special_chars"]
)
```

## Configuration

### Environment Variables
Create a `.env` file:
```plaintext
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here
```

### Provider Configuration
```python
# OpenAI Provider
openai_provider = OpenAIProvider(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo"  # or "gpt-4"
)

# Anthropic Provider
claude_provider = AnthropicProvider(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-opus-20240229"
)
```

## Architecture

AIFAST is built with a modular architecture:

1. **Core Components**
   - `AIInterface`: Main interface for interacting with LLMs
   - `ContentProcessor`: Text processing utilities
   - `ResponseFormatter`: Output formatting system
   - `PromptManager`: Prompt template management
   - `LLMConnector`: Base connection handling

2. **Providers**
   - `BaseProvider`: Abstract base class for providers
   - `OpenAIProvider`: OpenAI GPT integration
   - `AnthropicProvider`: Anthropic Claude integration

3. **Formatters**
   - Text
   - JSON
   - Markdown
   - YAML
   - Mermaid

## Examples

Check the `examples/` directory for more detailed examples:
- `format_test.py`: Response formatting examples
- `multi_provider_usage.py`: Using multiple LLM providers
- `debug_imports.py`: Package import verification

## Development

### Building the Package
To build a new distribution of the package:
```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build new distribution files
python setup.py sdist bdist_wheel
```

### Installation from Source
For development installation:
```bash
# Clone the repository
git clone https://github.com/OddballInnovator/AIFAST.git
cd AIFAST

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
# or
.\venv\Scripts\activate  # On Windows

# Install development dependencies
pip install -r requirements.txt

# Install package in editable mode
pip install -e .
```

### Running Tests
```bash
pytest
```

## License

MIT License

## Project Status

Current version: 0.1.0
Status: Alpha - Basic functionality implemented, actively developing new features
