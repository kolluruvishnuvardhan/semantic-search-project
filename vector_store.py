<<<<<<< HEAD
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # MiniLM is chosen for its low latency and small memory footprint
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.dimension = 384 # Dimension for MiniLM-L6-v2

    def encode(self, texts: list):
        return self.model.encode(texts, convert_to_numpy=True)

    def build_index(self, embeddings: np.ndarray):
        self.index = faiss.IndexFlatIP(self.dimension) # Inner Product for Cosine Similarity
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def search(self, query_vector: np.ndarray, k=5):
        faiss.normalize_L2(query_vector)
        distances, indices = self.index.search(query_vector, k)
=======
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # MiniLM is chosen for its low latency and small memory footprint
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.dimension = 384 # Dimension for MiniLM-L6-v2

    def encode(self, texts: list):
        return self.model.encode(texts, convert_to_numpy=True)

    def build_index(self, embeddings: np.ndarray):
        self.index = faiss.IndexFlatIP(self.dimension) # Inner Product for Cosine Similarity
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def search(self, query_vector: np.ndarray, k=5):
        faiss.normalize_L2(query_vector)
        distances, indices = self.index.search(query_vector, k)
>>>>>>> fd552f28aad4f45ea86cd8f3991a2913752c2073
        return distances, indices