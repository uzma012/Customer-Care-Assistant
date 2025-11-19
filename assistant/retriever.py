from .embedder import Embedder
import faiss, json, os, numpy as np
from typing import List, Tuple

INDEX_PATH = os.path.join("output")    

class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.k = 5  
        self.index = faiss.read_index(os.path.join(INDEX_PATH, "index.faiss"))
        with open(os.path.join(INDEX_PATH, "passages.json"), "r", encoding="utf-8") as f:
            self.passages = json.load(f)   # list indexed in same order as embeddings


    def retrieve(self, query):
        embedding = self.embedder.embed_query(query)
        faiss.normalize_L2(embedding)
        distances, idxs = self.index.search(embedding, self.k)
        results = []
        for idx, dist in zip(idxs[0], distances[0]):
            results.append((self.passages[int(idx)], float(dist)))  # higher distance = more similar because of IP on normalized vectors

        return results
    
    def assemble_prompt(self,query: str, System_prompt:str ,  retrieved: List[Tuple[dict, float]], max_chars=2000) -> str:
        ctx = ""
        seen = set()
        for p, _ in retrieved:
            snippet = p["text"]
            if snippet in seen:
                continue
            seen.add(snippet)
            if len(ctx) + len(snippet) > max_chars:
                break
            source = p.get("meta", {}).get("title") or p.get("meta", {}).get("source_id") or p.get("source") or "Unknown"
            ctx += f"\nSource: {source}\n{snippet}\n"
        prompt = f"{System_prompt}\n\nContext:{ctx}\n\nQuestion: {query}\nAnswer:"
        return prompt
    
