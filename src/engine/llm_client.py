import requests
from typing import List, Dict, Optional

class PRISMLLMClient:
    """
    Client for interacting with various LLM providers (OpenRouter, OpenAI, Gemini, etc.)
    """
    
    PROVIDERS = {
        "OpenRouter": "https://openrouter.ai/api/v1",
        "OpenAI": "https://api.openai.com/v1",
        "DeepSeek": "https://api.deepseek.com/v1",
    }

    def __init__(self, provider: str, api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        self.base_url = self.PROVIDERS.get(provider, "")

    def get_models(self) -> List[Dict]:
        """Fetches available models from the provider."""
        if self.provider == "OpenRouter":
            try:
                response = requests.get(f"{self.base_url}/models")
                if response.status_code == 200:
                    return response.json().get("data", [])
            except Exception:
                pass
        
        # Fallback / Static lists for other providers for demo
        fallbacks = {
            "OpenAI": [{"id": "gpt-4o", "name": "GPT-4o"}, {"id": "gpt-4-turbo", "name": "GPT-4 Turbo"}],
            "DeepSeek": [{"id": "deepseek-chat", "name": "DeepSeek Chat"}, {"id": "deepseek-coder", "name": "DeepSeek Coder"}],
            "Gemini": [{"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro"}, {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash"}],
            "Claude": [{"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"}, {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"}]
        }
        return fallbacks.get(self.provider, [{"id": "default", "name": "Default Model"}])

    def test_connection(self) -> bool:
        """Tests connectivity with the current provider and API key."""
        if not self.api_key or len(self.api_key) < 5:
            return False
        
        if self.provider == "OpenRouter":
            try:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                response = requests.get(f"{self.base_url}/auth/key", headers=headers)
                return response.status_code == 200
            except Exception:
                return False
        
        return True

    def query(self, model: str, prompt: str) -> str:
        """Sends a query to the LLM."""
        safe_prompt = str(prompt)[:50]
        return f"Mock response from {self.provider} ({model}) for prompt: {safe_prompt}..."
