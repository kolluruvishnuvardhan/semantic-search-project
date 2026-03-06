<<<<<<< HEAD
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from data_loader import load_news_data
from vector_store import VectorStore
from clustering import ClusterManager
from semantic_cache import SemanticCache

app = FastAPI(title="Cluster-Aware Semantic Search")

# Global State
store = VectorStore()
cluster_manager = ClusterManager(n_clusters=20)
cache = SemanticCache(threshold=0.85)
documents = []

@app.on_event("startup")
def initialize_system():
    global documents
    print("Loading data and building index...")
    documents = load_news_data()
    embeddings = store.encode(documents)
    store.build_index(embeddings)
    cluster_manager.fit(embeddings)
    print("System Ready.")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    query_vec = store.encode([request.query])[0]
    dom_cluster = int(cluster_manager.get_dominant_cluster(query_vec))
    
    # 1. Check Cache
    cache_result = cache.lookup(query_vec, dom_cluster)
    if cache_result:
        return {
            "cache_hit": True,
            "dominant_cluster": dom_cluster,
            "similarity_score": cache_result["similarity"],
            "results": cache_result["response"]
        }

    # 2. Vector Search if Cache Miss
    distances, indices = store.search(query_vec.reshape(1, -1), k=request.top_k)
    results = [documents[i] for i in indices[0]]
    
    # 3. Save to Cache
    cache.add(query_vec, dom_cluster, results)
    
    return {
        "cache_hit": False,
        "dominant_cluster": dom_cluster,
        "similarity_score": float(distances[0][0]),
        "results": results
    }

@app.get("/cache/stats")
async def get_stats():
    return cache.get_stats()

@app.delete("/cache")
async def clear_cache():
    cache.clear()
=======
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from data_loader import load_news_data
from vector_store import VectorStore
from clustering import ClusterManager
from semantic_cache import SemanticCache

app = FastAPI(title="Cluster-Aware Semantic Search")

# Global State
store = VectorStore()
cluster_manager = ClusterManager(n_clusters=20)
cache = SemanticCache(threshold=0.85)
documents = []

@app.on_event("startup")
def initialize_system():
    global documents
    print("Loading data and building index...")
    documents = load_news_data()
    embeddings = store.encode(documents)
    store.build_index(embeddings)
    cluster_manager.fit(embeddings)
    print("System Ready.")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    query_vec = store.encode([request.query])[0]
    dom_cluster = int(cluster_manager.get_dominant_cluster(query_vec))
    
    # 1. Check Cache
    cache_result = cache.lookup(query_vec, dom_cluster)
    if cache_result:
        return {
            "cache_hit": True,
            "dominant_cluster": dom_cluster,
            "similarity_score": cache_result["similarity"],
            "results": cache_result["response"]
        }

    # 2. Vector Search if Cache Miss
    distances, indices = store.search(query_vec.reshape(1, -1), k=request.top_k)
    results = [documents[i] for i in indices[0]]
    
    # 3. Save to Cache
    cache.add(query_vec, dom_cluster, results)
    
    return {
        "cache_hit": False,
        "dominant_cluster": dom_cluster,
        "similarity_score": float(distances[0][0]),
        "results": results
    }

@app.get("/cache/stats")
async def get_stats():
    return cache.get_stats()

@app.delete("/cache")
async def clear_cache():
    cache.clear()
>>>>>>> fd552f28aad4f45ea86cd8f3991a2913752c2073
    return {"message": "Cache cleared successfully"}