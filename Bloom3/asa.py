import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Set random seed for reproducibility
np.random.seed(42)

# Generate 3 random clusters
n_samples = 300
n_clusters = 3
n_features = 2

# Generate synthetic data with 3 distinct clusters
X, y_true = make_blobs(n_samples=n_samples, centers=n_clusters, 
                       n_features=n_features, random_state=42, 
                       cluster_std=1.5)

# Apply K-means clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
y_pred = kmeans.fit_predict(X)

# Get cluster centers
centers = kmeans.cluster_centers_

# Create the plot
plt.figure(figsize=(12, 5))

# Plot 1: Original data with true labels
plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], c=y_true, cmap='viridis', 
            s=50, alpha=0.7, edgecolors='k', linewidth=0.5)
plt.title('Original Data (True Clusters)', fontsize=14, fontweight='bold')
plt.xlabel('Feature 1', fontsize=12)
plt.ylabel('Feature 2', fontsize=12)
plt.grid(True, alpha=0.3)

# Plot 2: K-means clustering results
plt.subplot(1, 2, 2)
plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='viridis', 
            s=50, alpha=0.7, edgecolors='k', linewidth=0.5)
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x', 
            s=200, linewidths=3, label='Centroids', zorder=10)
plt.title('K-means Clustering Results', fontsize=14, fontweight='bold')
plt.xlabel('Feature 1', fontsize=12)
plt.ylabel('Feature 2', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print some statistics
print(f"Number of clusters: {n_clusters}")
print(f"Number of samples: {n_samples}")
print(f"\nCluster centers:")
for i, center in enumerate(centers):
    print(f"  Cluster {i+1}: ({center[0]:.2f}, {center[1]:.2f})")
print(f"\nInertia (within-cluster sum of squares): {kmeans.inertia_:.2f}")
