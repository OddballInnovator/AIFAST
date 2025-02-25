import os
import json
from dotenv import load_dotenv
from aifast import (
    AIInterface,
    OpenAIProvider,
    AnthropicProvider,
    CohereProvider,
    ContentProcessor
)

def test_content_processor():
    print("\n=== Testing Content Processor ===")
    processor = ContentProcessor()
    
    # Test text with multiple issues
    text = """
    This is a   MESSY text with
    multiple     spaces,    \n\n UPPERCASE letters,
    and special ch@r&cters!!!
    
    It has multiple paragraphs   with irregular     spacing.
    """
    
    print("Original text:")
    print(f"'{text}'\n")
    
    # Test individual processors
    print("1. Clean (remove extra whitespace):")
    cleaned = processor.clean(text)
    print(f"'{cleaned}'\n")
    
    print("2. Lowercase:")
    lowercased = processor.lowercase(cleaned)
    print(f"'{lowercased}'\n")
    
    print("3. Remove special characters:")
    no_special = processor.remove_special_chars(lowercased)
    print(f"'{no_special}'\n")
    
    print("4. Tokenize:")
    tokens = processor.tokenize(no_special)
    print(f"Tokens: {tokens}\n")
    
    print("5. Summarize (max 10 words):")
    summary = processor.summarize(cleaned, max_length=10)
    print(f"'{summary}'\n")
    
    # Test pipeline processing
    print("6. Pipeline processing (clean -> lowercase -> remove_special_chars):")
    pipeline_result = processor.process(
        text,
        pipeline=["clean", "lowercase", "remove_special_chars"]
    )
    print(f"'{pipeline_result}'")

def test_provider(name: str, provider, prompt: str):
    print(f"\n=== Testing {name} Provider ===")
    ai = AIInterface(provider=provider)
    
    print("Completion test:")
    response = ai.complete(prompt)
    print(f"Response: {response}\n")
    
    print("Chat test:")
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What's your name and who created you?"}
    ]
    chat_response = ai.chat(messages)
    print(f"Response: {chat_response}")

def test_response_formatter():
    print("\n=== Testing Response Formatter ===")
    from aifast.core.response_formatter import ResponseFormatter

    # Test cases with different types of content
    test_cases = {
        "Code": """
        def fibonacci(n):
            if n <= 1:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        """,
        
        "Lists": """
        Benefits of Python:
        1) Easy to learn
        2) Large ecosystem
        * Great community
        * Extensive libraries
        """,
        
        "JSON-like": """
        {
            "name": "Python",
            "type": "Programming Language",
            "features": ["easy", "powerful", "flexible"]
        }
        """,
        
        "Mixed Content": """
        # Data Processing in Python
        
        Here's a simple data processor:
        
        def process_data(data):
            results = []
            for item in data:
                results.append(item * 2)
            return results
        
        Key features:
        1) Handles lists
        2) Simple multiplication
        * Returns new list
        * Preserves order
        """
    }

    formats = ["text", "json", "markdown", "yaml"]
    
    for test_name, content in test_cases.items():
        print(f"\n{'-'*20} Testing {test_name} {'-'*20}")
        print("Original content:")
        print(content)
        
        for fmt in formats:
            print(f"\n{fmt.upper()} Format:")
            formatter = ResponseFormatter(fmt)
            try:
                formatted = formatter.format(content)
                print(f"Result type: {type(formatted)}")
                if isinstance(formatted, (dict, list)):
                    print(f"Formatted output:\n{json.dumps(formatted, indent=2)}")
                else:
                    print(f"Formatted output:\n{formatted}")
            except Exception as e:
                print(f"Error formatting as {fmt}: {str(e)}")

def main():
    # Load environment variables
    load_dotenv()
    
    # Test the response formatter first
    test_response_formatter()
    
    # Test the content processor
    test_content_processor()
    
    # Then test the providers
    prompt = "Explain what a decorator is in Python, keep it brief."
    
    # Test OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        provider = OpenAIProvider(api_key=openai_key)
        test_provider("OpenAI", provider, prompt)
    
    # Test Claude
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    print(f"Found Anthropic key: {'Yes' if anthropic_key else 'No'}")  # Don't print the actual key
    if anthropic_key:
        provider = AnthropicProvider(api_key=anthropic_key)
        test_provider("Claude", provider, prompt)
    
    # # Test Cohere
    # cohere_key = os.getenv("COHERE_API_KEY")
    # if cohere_key:
    #     provider = CohereProvider(api_key=cohere_key)
    #     test_provider("Cohere", provider, prompt)

if __name__ == "__main__":
    main() 