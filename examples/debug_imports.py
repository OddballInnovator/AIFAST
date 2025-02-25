import sys
print("Python path:", sys.path)

print("\nTrying to import aifast...")
import aifast
print("aifast.__file__:", aifast.__file__)
print("aifast.__all__:", getattr(aifast, '__all__', None))

print("\nTrying to import providers...")
from aifast.providers import anthropic_provider
print("anthropic_provider.__file__:", anthropic_provider.__file__)

print("\nTrying to import AnthropicProvider...")
from aifast.providers.anthropic_provider import AnthropicProvider
print("Successfully imported AnthropicProvider") 