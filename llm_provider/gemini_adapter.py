# llm_provider/gemini_adapter.py
import os
import numpy as np
import google.generativeai as genai

class GeminiAdapter:
    def __init__(self, model_name="gemini-1.5-flash", mock_embeddings=False):
        self.model_name = model_name
        self.embed_model = "models/embedding-001"
        self.mock_mode = os.environ.get("MOCK_MODE", "0") == "1"
        self.mock_embeddings = mock_embeddings  # NEW

    def chat(self, messages):
        if self.mock_mode:
            return f"[MOCK-{self.model_name}] " + " | ".join(messages)
        try:
            model = genai.GenerativeModel(self.model_name)
            out = model.generate_content("\n".join(messages))
            return getattr(out, "text", str(out))
        except Exception as e:
            return f"[ERROR Gemini API: {e}]"

    def embed(self, texts):
        if self.mock_mode or self.mock_embeddings:
            if isinstance(texts, str):
                texts = [texts]
            # deterministic fake embeddings
            return np.ones((len(texts), 768)).tolist()
        try:
            result = genai.embed_content(model=self.embed_model, content=texts)
            if isinstance(result, dict) and "embedding" in result:
                return result["embedding"]
            return result
        except Exception as e:
            return [0.0] * 768
