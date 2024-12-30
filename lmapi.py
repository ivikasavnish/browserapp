from abc import ABC, abstractmethod
import os
from typing import Dict, Any, Optional
import openai
from anthropic import Anthropic
import requests
from typing import Iterator
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def stream(self, prompt: str, **kwargs) -> iter:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content

    def stream(self, prompt: str, **kwargs) -> iter:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text

    def stream(self, prompt: str, **kwargs) -> iter:
        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs
        )
        for chunk in response:
            if chunk.content:
                yield chunk.content[0].text

class LLMFactory:
    @staticmethod
    def create_provider(provider_type: str, config: Dict[str, Any]) -> LLMProvider:
        providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider
        }
        
        if provider_type not in providers:
            raise ValueError(f"Unsupported provider: {provider_type}")
            
        return providers[provider_type](**config)
class OllamaProvider(LLMProvider):
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama2"):
        self.host = host
        self.model = model
        self.generate_url = f"{host}/api/generate"
        self.chat_url = f"{host}/api/chat"

    def generate(self, prompt: str, **kwargs) -> str:
        response = requests.post(
            self.generate_url,
            json={
                "model": self.model,
                "prompt": prompt,
                **kwargs
            }
        )
        return response.json()["response"]

    def stream(self, prompt: str, **kwargs) -> Iterator[str]:
        response = requests.post(
            self.generate_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                **kwargs
            },
            stream=True
        )
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "response" in chunk:
                    yield chunk["response"]
# Usage example
if __name__ == "__main__":
    config = {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-3.5-turbo"
    }
    
    llm = LLMFactory.create_provider("openai", config)
    response = llm.generate("Hello, how are you?")
    print(response)
    
    # Streaming example
    for chunk in llm.stream("Tell me a story"):
        print(chunk, end="", flush=True)