"""Local-only embedding interfaces and deterministic test embedding."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Protocol, Sequence


class LocalEmbeddingModel(Protocol):
    model_id: str
    dimension: int

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...

    def fingerprint(self) -> str: ...


class LocalHashEmbeddingModel:
    """Dependency-free deterministic embedding for tests and offline smoke runs.

    This is a reproducible feature-vector baseline, not a language model. Production
    semantic quality should use the local sentence-transformer adapter below.
    """

    def __init__(self, dimension: int = 256, model_id: str = "local-hash-v1") -> None:
        if dimension <= 0:
            raise ValueError("dimension must be > 0")
        self.dimension = dimension
        self.model_id = model_id

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_one(text)

    def fingerprint(self) -> str:
        payload = json.dumps({"model_id": self.model_id, "dimension": self.dimension}, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _embed_one(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        tokens = [token for token in text.lower().split() if token]
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimension
            vector[index] += 1.0 if digest[4] % 2 else -1.0
        norm = sum(value * value for value in vector) ** 0.5
        return [value / norm for value in vector] if norm else vector


class LocalSentenceTransformerEmbedding:
    """Optional local sentence-transformer adapter with network access disabled."""

    def __init__(self, model_path: Path, *, device: str = "cpu") -> None:
        if not model_path.exists():
            raise FileNotFoundError(f"local embedding model not found: {model_path}")
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError("sentence-transformers is required for a local model adapter") from exc
        self.model_path = model_path.resolve()
        self.model_id = self.model_path.name
        self._model = SentenceTransformer(str(self.model_path), device=device, local_files_only=True)
        self.dimension = int(self._model.get_sentence_embedding_dimension())

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        vectors = self._model.encode(list(texts), normalize_embeddings=True, show_progress_bar=False)
        return [list(map(float, vector)) for vector in vectors]

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]

    def fingerprint(self) -> str:
        digest = hashlib.sha256()
        for path in sorted(self.model_path.rglob("*")):
            if path.is_file():
                digest.update(path.relative_to(self.model_path).as_posix().encode("utf-8"))
                digest.update(path.read_bytes())
        return digest.hexdigest()
