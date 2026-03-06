import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticCache:
    def __init__(self, threshold=0.85):
        # Key: cluster_id, Value: List of dicts {query_vec, response, query_text}
        self.cache = {} 
        self.threshold = threshold
        self.stats = {"hit_count": 0, "miss_count": 0, "total_entries": 0}

    def lookup(self, query_vector: np.ndarray, cluster_id: int):
        """
        Cluster-Aware Lookup: Only searches within the predicted cluster.
        This reduces O(N) search to O(N/K).
        """
        if cluster_id not in self.cache:
            self.stats["miss_count"] += 1
            return None

        # Compare against all entries in this specific cluster
        cluster_entries = self.cache[cluster_id]
        
        best_score = -1
        best_result = None

        for entry in cluster_entries:
            # Reshape for sklearn similarity
            score = cosine_similarity(query_vector.reshape(1, -1), 
                                      entry['vector'].reshape(1, -1))[0][0]
            if score > best_score:
                best_score = score
                best_result = entry

        if best_score >= self.threshold:
            self.stats["hit_count"] += 1
            return {
                "response": best_result['response'],
                "similarity": float(best_score)
            }

        self.stats["miss_count"] += 1
        return None

    def add(self, query_vector: np.ndarray, cluster_id: int, response: list):
        if cluster_id not in self.cache:
            self.cache[cluster_id] = []
        
        self.cache[cluster_id].append({
            "vector": query_vector,
            "response": response
        })
        self.stats["total_entries"] += 1

    def clear(self):
        self.cache = {}
        self.stats = {"hit_count": 0, "miss_count": 0, "total_entries": 0}

    def get_stats(self):
        return self.stats