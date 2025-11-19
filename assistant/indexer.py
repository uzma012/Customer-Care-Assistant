from sentence_transformers import SentenceTransformer
import faiss
import json
from pathlib import Path
from .embedder import Embedder
import os

embed_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))

class Indexer:
    def __init__(self):
        pass

    def chunk_text(self,text, chunk_size=500, chunk_overlap=50):
        tokens = text.split()
        chunks = []
        i = 0
        while i < len(tokens):
            chunk_tokens = tokens[i:i+chunk_size]
            chunks.append(" ".join(chunk_tokens))
            i += chunk_size - chunk_overlap
        return chunks


    def build_index_from_json(self,json_path: str):

        json_path = Path(json_path).resolve()
        if not json_path.exists():
            raise FileNotFoundError(json_path)

        output_dir = json_path.parent

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = json.dumps(data, indent=2)

        chunks = self.chunk_text(text, chunk_size=150, chunk_overlap=30)

        if not chunks:
            chunks = [text]

        passages = []
        for i, c in enumerate(chunks):
            passages.append({
                "id": f"chunk_{i}",
                "text": c,
                "meta": data
            })

        texts = [p["text"] for p in passages]
        embeddings = Embedder().embed_text(texts)
        faiss.normalize_L2(embeddings)

        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)

        faiss.write_index(index, str(output_dir / "index.faiss"))
        with open(output_dir / "passages.json", "w", encoding="utf-8") as f:
            json.dump(passages, f, ensure_ascii=False, indent=2)

        print(f"Indexed {len(passages)} chunks | dim={dim}")
        print(f"Saved index + metadata to: {output_dir}")


