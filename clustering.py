from sklearn.mixture import GaussianMixture
import numpy as np

class ClusterManager:
    def __init__(self, n_clusters=20):
        # K=20 matches the natural structure of the 20 Newsgroups dataset
        self.gmm = GaussianMixture(n_components=n_clusters, covariance_type='diag', random_state=42)
        
    def fit(self, embeddings: np.ndarray):
        self.gmm.fit(embeddings)
        
    def predict_proba(self, embeddings: np.ndarray):
        # Soft clustering: returns probabilities for all clusters
        return self.gmm.predict_proba(embeddings)
    
    def get_dominant_cluster(self, embedding: np.ndarray):
        # For cache routing, we pick the most likely cluster
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        return self.gmm.predict(embedding)[0]