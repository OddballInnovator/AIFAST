class AIInterface:
    def __init__(self, provider):
        self.provider = provider
    
    def complete(self, prompt: str) -> str:
        return self.provider.complete(prompt)
    
    def chat(self, messages: list) -> str:
        return self.provider.chat(messages)
