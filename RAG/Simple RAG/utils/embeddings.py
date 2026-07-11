from __future__ import annotations

from sentence_transformers import SentenceTransformer


class NomicEmbeddingModel:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name, trust_remote_code=True)
        return self._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        model = self._load_model()
        embeddings = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True).tolist()
        return [list(map(float, vector)) for vector in embeddings]

    def embed_query(self, text: str) -> list[float]:
        model = self._load_model()
        vector = model.encode([text], normalize_embeddings=True, convert_to_numpy=True)[0].tolist()
        return [float(value) for value in vector]
