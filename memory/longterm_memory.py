# memory/longterm_memory.py
from memory.chroma_setup import get_chroma_client
from llm_provider.gemini_adapter import GeminiAdapter
from typing import List

class AgentMemory:
    def __init__(self, collection_name: str = "agent_memory", mock_embeddings=False):
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = GeminiAdapter(mock_embeddings=mock_embeddings)
  # used for embeddings

    def add_memory(self, doc_id: str, text: str):
        emb = self.embedder.embed(text)
        self.collection.add(ids=[doc_id], documents=[text], embeddings=[emb])

    # def get_memories(self, query: str, n_results: int = 3) -> List[dict]:
    #     emb = self.embedder.embed(query)
    #     res = self.collection.query(query_embeddings=[emb], n_results=n_results)
    #     # res format varies; return list of dicts: {"id":..., "document":...}
    #     docs = []
    #     if isinstance(res, dict):
    #         hits = res.get("documents", [])
    #         for d in hits:
    #             docs.append({"document": d})
    #     else:
    #         # best-effort
    #         docs = [{"document": x} for x in res]
    #     return docs

    # memory/longterm_memory.py

    def get_memories(self, query: str, n_results: int = 3) -> List[dict]:
        emb = self.embedder.embed(query)
        res = self.collection.query(query_embeddings=[emb], n_results=n_results)
        docs = []
        if isinstance(res, dict):
            hits = res.get("documents", [])
            for d in hits:
                # d is usually a list of strings, take the first string
                if isinstance(d, list) and d:
                    docs.append({"document": d[0]})
                elif isinstance(d, str):
                    docs.append({"document": d})
        else:
            docs = [{"document": str(x)} for x in res]
        return docs

