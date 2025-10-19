from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from . import vectorstore, embeddings, data_loader

app = FastAPI(title="Product Recommendation API")


class Product(BaseModel):
    uniq_id: str
    title: str
    brand: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    categories: Optional[List[str]] = None
    images: Optional[List[str]] = None


@app.post("/ingest")
def ingest_products(products: List[Product]):
    """Ingest products into vector store (embeddings)."""
    docs = [p.dict() for p in products]
    try:
        # pass embedding function
        vectorstore.ingest_documents(docs, embed_fn=embeddings.get_text_embedding)
        return {"status": "ok", "ingested": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



import math

def _sanitize_json(obj):
    # Recursively replace NaN/Inf with None in dicts/lists
    if isinstance(obj, dict):
        return {k: _sanitize_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_json(x) for x in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    else:
        return obj

@app.get("/recommend")
def recommend(q: str, top_k: int = 6):
    """Recommend products for a query string using semantic search."""
    try:
        emb = embeddings.get_text_embedding(q)
        results = vectorstore.semantic_search(emb, top_k=top_k)
        results = _sanitize_json(results)
        return {"query": q, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/stats")
def analytics_stats():
    df = data_loader.load_sample_dataframe()
    stats = {
        "num_products": len(df),
        "avg_price": float(df["price"].dropna().mean()) if "price" in df.columns else None,
        "categories": df["categories"].explode().value_counts().to_dict() if "categories" in df.columns else {},
    }
    return stats


@app.post('/demo/load_sample')
def load_sample():
    """Load the sample dataset into vectorstore for demo purposes."""
    df = data_loader.load_sample_dataframe()
    docs = df.to_dict(orient='records')
    vectorstore.ingest_documents(docs, embed_fn=embeddings.get_text_embedding)
    return {"loaded": len(docs)}
