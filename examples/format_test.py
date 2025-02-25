import os
from dotenv import load_dotenv
from aifast import (
    AIInterface,
    OpenAIProvider,
    ResponseFormatter
)
import json

def test_json_response():
    """
    Test case 1: Get structured JSON data from OpenAI
    Asking for information about programming languages with specific fields
    """
    print("\n=== Testing JSON Response Format ===")
    
    # Create provider and formatter
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    ai = AIInterface(provider=provider)
    formatter = ResponseFormatter("json")
    
    # Prompt designed to elicit structured data
    prompt = """
    Compare Python and JavaScript. Return the response in JSON format with the following structure:
    {
        "languages": [
            {
                "name": "language name",
                "type": "programming paradigm",
                "strengths": ["strength1", "strength2"],
                "weaknesses": ["weakness1", "weakness2"],
                "best_used_for": ["use case1", "use case2"]
            }
        ]
    }
    """
    
    # Get and format response
    response = ai.complete(prompt)
    formatted = formatter.format(response)
    
    print("\nOriginal response:")
    print(response)
    print("\nFormatted as JSON:")
    print(json.dumps(formatted, indent=2))

def test_markdown_response():
    """
    Test case 2: Get markdown formatted documentation from OpenAI
    Asking for a technical explanation with code examples
    """
    print("\n=== Testing Markdown Response Format ===")
    
    # Create provider and formatter
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    ai = AIInterface(provider=provider)
    formatter = ResponseFormatter("markdown")
    
    # Prompt designed to elicit documentation-style response
    prompt = """
    Explain how to implement a decorator in Python that measures function execution time.
    Include:
    1. Explanation of the concept
    2. Code example
    3. Usage example
    4. Common pitfalls
    Format the response with proper markdown including code blocks and lists.
    """
    
    # Get and format response
    response = ai.complete(prompt)
    formatted = formatter.format(response)
    
    print("\nOriginal response:")
    print(response)
    print("\nFormatted as Markdown:")
    print(formatted)

def test_mermaid_response():
    """
    Test case 3: Get Mermaid diagram from OpenAI
    Asking for a flowchart representation
    """
    print("\n=== Testing Mermaid Response Format ===")
    
    # Create provider and formatter
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    ai = AIInterface(provider=provider)
    formatter = ResponseFormatter("mermaid")
    
    # Prompt designed to elicit a flowchart response
    prompt = """
    Create a mermaid flowchart showing the steps of a Git workflow.
    Include: clone, create branch, make changes, commit, push, pull request, merge.
    Use proper mermaid flowchart syntax.
    """
    
    # Get and format response
    response = ai.complete(prompt)
    formatted = formatter.format(response)
    
    print("\nOriginal response:")
    print(response)
    print("\nFormatted as Mermaid:")
    print(formatted)

def main():
    # Load environment variables
    load_dotenv()
    
    # Run test cases
    test_json_response()
    test_markdown_response()
    test_mermaid_response()

if __name__ == "__main__":
    main() 