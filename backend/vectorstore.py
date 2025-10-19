import os
import numpy as np
from typing import List, Dict

_USE_PINECONE = bool(os.environ.get("PINECONE_API_KEY"))

if _USE_PINECONE:
    import pinecone
    # init handled lazily
else:   
    import faiss
    _index = None
    _metadatas: List[Dict] = []


def ingest_documents(docs: List[Dict], embed_fn=None):
    """docs: list of dicts. Each dict must have 'uniq_id' and text fields."""
    global _index, _metadatas
    texts = []
    ids = []

    def _to_text(val):
        # handle None and NaN floats
        if val is None:
            return ""
        # NaN check for floats
        try:
            import math
            if isinstance(val, float) and math.isnan(val):
                return ""
        except Exception:
            pass
        return str(val)

    for d in docs:
        ids.append(d.get("uniq_id") or str(len(_metadatas)))
        title = _to_text(d.get("title", ""))
        desc = _to_text(d.get("description", ""))
        texts.append((title + " \n " + desc).strip())
    if embed_fn is None:
        raise ValueError("embed_fn must be provided")
    embeddings = [embed_fn(t) for t in texts]
    dim = len(embeddings[0])
    if _USE_PINECONE:
        api_key = os.environ["PINECONE_API_KEY"]
        env = os.environ.get("PINECONE_ENV")
        pinecone.init(api_key=api_key, environment=env)
        idx_name = os.environ.get("PINECONE_INDEX", "products")
        if idx_name not in pinecone.list_indexes():
            pinecone.create_index(idx_name, dimension=dim)
        idx = pinecone.Index(idx_name)
        to_upsert = [(ids[i], embeddings[i].tolist(), docs[i]) for i in range(len(ids))]
        idx.upsert(vectors=to_upsert)
    else:
        if _index is None:
            _index = faiss.IndexFlatL2(dim)
        arr = np.array(embeddings).astype('float32')
        _index.add(arr)
        for d in docs:
            _metadatas.append(d)


def semantic_search(query_embedding, top_k: int = 6):
    """Return list of metadata dicts with score"""
    if _USE_PINECONE:
        api_key = os.environ["PINECONE_API_KEY"]
        env = os.environ.get("PINECONE_ENV")
        pinecone.init(api_key=api_key, environment=env)
        idx_name = os.environ.get("PINECONE_INDEX", "products")
        idx = pinecone.Index(idx_name)
        res = idx.query(vector=query_embedding.tolist(), top_k=top_k, include_metadata=True, include_values=False)
        out = []
        for match in res.get('matches', []):
            out.append({"id": match['id'], "score": match['score'], "metadata": match.get('metadata')})
        return out
    else:
        global _index, _metadatas
        if _index is None or _index.ntotal == 0:
            return []
        import numpy as np
        q = np.array([query_embedding]).astype('float32')
        D, I = _index.search(q, top_k)
        out = []
        for dist, idx in zip(D[0], I[0]):
            meta = _metadatas[idx] if idx < len(_metadatas) else {}
            out.append({"id": meta.get('uniq_id'), "score": float(dist), "metadata": meta})
        return out
