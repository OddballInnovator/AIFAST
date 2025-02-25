import os
from dotenv import load_dotenv
from aifast import (
    AIInterface, 
    OpenAIProvider, 
    ContentProcessor, 
    PromptManager,
    LLMConnector
)

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY in .env file")
    
    # Initialize connector with rate limiting
    connector = LLMConnector(api_key)
    connector.set_rate_limits(requests_per_min=30, tokens_per_min=45000)
    
    # Initialize provider with custom settings
    provider = OpenAIProvider(
        api_key=api_key,
        model="gpt-4"  # Using GPT-4 for this example
    )
    
    # Initialize AI interface
    ai = AIInterface(provider=provider)
    
    # Test advanced chat with system message
    print("\n=== Testing Advanced Chat ===")
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant specializing in Python programming."},
        {"role": "user", "content": "Write a simple decorator to measure function execution time."}
    ]
    
    # Check rate limits before making request
    if connector.check_rate_limit():
        chat_response = ai.chat(messages)
        print(f"Response: {chat_response}")
    else:
        print("Rate limit exceeded, please wait...")
    
    # Test content processing pipeline
    print("\n=== Testing Advanced Content Processing ===")
    processor = ContentProcessor()
    
    text = """This is a TEST document with multiple     spaces and special @#$ characters.
    It spans multiple lines   with irregular spacing."""
    
    print(f"Original text: '{text}'")
    
    # Process with multiple steps
    processed = processor.process(
        text, 
        pipeline=["clean", "remove_special_chars", "lowercase"]
    )
    print(f"Processed text: '{processed}'")
    
    # Get current rate limits
    limits = connector.get_rate_limits()
    print("\n=== Rate Limits ===")
    print(f"Requests per minute: {limits['requests_per_min']}")
    print(f"Tokens per minute: {limits['tokens_per_min']}")

if __name__ == "__main__":
    main()
