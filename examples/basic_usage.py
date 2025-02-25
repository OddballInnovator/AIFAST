import os
from dotenv import load_dotenv
from aifast import AIInterface, OpenAIProvider, ContentProcessor

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI provider with API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY in .env file")
    
    provider = OpenAIProvider(api_key=api_key)
    ai = AIInterface(provider=provider)
    
    # Test completion
    print("\n=== Testing Completion ===")
    completion_prompt = "Translate 'Hello, how are you?' to French"
    print(f"Prompt: {completion_prompt}")
    response = ai.complete(completion_prompt)
    print(f"Response: {response}")
    
    # Test chat
    print("\n=== Testing Chat ===")
    messages = [
        {"role": "user", "content": "What's the capital of France?"}
    ]
    print(f"Messages: {messages}")
    chat_response = ai.chat(messages)
    print(f"Response: {chat_response}")
    
    # Test content processing
    print("\n=== Testing Content Processing ===")
    processor = ContentProcessor()
    text = "  This is a test   text with   extra spaces  "
    print(f"Original text: '{text}'")
    
    processed = processor.process(text, pipeline=["clean", "tokenize"])
    print(f"Processed text: {processed}")

if __name__ == "__main__":
    main()
