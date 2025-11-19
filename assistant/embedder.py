from sentence_transformers import SentenceTransformer
import os


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))

    def embed_text(self, text: str):
        return self.model.encode(
        text,
        batch_size=32,
        convert_to_numpy=True,
        show_progress_bar=True
        ).astype("float32")
    
    def embed_query(self, query: str):
        return self.model.encode([query], convert_to_numpy=True).astype("float32")