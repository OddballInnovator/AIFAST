import sys
import os

print("Python Path:", sys.path)
print("Current Directory:", os.getcwd())

# Try to import the module first
import aifast.core.ai_interface as ai_module
print("Module contents:", dir(ai_module))

# Then try to import the class
from aifast.core.ai_interface import AIInterface
print("Successfully imported AIInterface")