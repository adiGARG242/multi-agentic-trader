# llm_provider/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    def chat(self, messages: List[str]) -> str:
        pass

    @abstractmethod
    def embed(self, texts: List[str]) -> List[float]:
        pass

    @abstractmethod
    def structured_output(self, prompt: List[str], json_schema: Dict[str, Any]) -> Dict[str, Any]:
        pass
