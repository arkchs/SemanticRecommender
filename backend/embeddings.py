from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL = None


def _load_model():
    global _MODEL
    if _MODEL is None:
        # use a small model for speed in demo; can be replaced with larger models
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def get_text_embedding(text: str):
    model = _load_model()
    emb = model.encode([text], convert_to_numpy=True)
    return emb[0].astype(np.float32)
