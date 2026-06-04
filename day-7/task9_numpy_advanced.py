# Task 9: Boolean masking, broadcasting, and cosine similarity with NumPy.
# In this code, we demonstrate three advanced NumPy techniques: boolean masking to filter elements of an array based on a condition, broadcasting to apply operations across arrays of different shapes without explicit loops, and a function to compute cosine similarity between two vectors.    
# We create a NumPy array of scores and use boolean masking to extract scores greater than 60. We then apply a 10% penalty to all scores using broadcasting. Finally, we define a function to compute cosine similarity between two vectors and test it with different pairs of vectors to illustrate the concept of similarity in high-dimensional space.  
# The outputs are printed in a clear format to show the results of each technique and the expected outcomes based on the mathematical properties of cosine similarity.
import numpy as np

scores = np.array([45, 78, 92, 33, 61, 88, 55, 70, 40, 95])

mask = scores > 60
passing = scores[mask]
print("=== Boolean Masking ===")
print(f"  All scores  : {scores}")
print(f"  Mask (>60)  : {mask}")
print(f"  Passing     : {passing}")

penalised = np.round(scores * 0.9, 1)
print("\n=== Broadcasting — 10% penalty applied ===")
print(f"  Original  : {scores}")
print(f"  Penalised : {penalised}")

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    Formula: (v1 · v2) / (||v1|| * ||v2||)
    Returns a value in [-1, 1]; 1 = identical direction, 0 = orthogonal.
    """
    dot_product = np.dot(v1, v2)
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    if norm == 0:
        return 0.0
    return float(dot_product / norm)


print("\n=== Cosine Similarity ===")

v1 = np.array([1.0, 2.0, 3.0])
v2 = np.array([2.0, 4.0, 6.0])   
sim1 = cosine_similarity(v1, v2)
print(f"  v1={v1}, v2={v2}")
print(f"  Similarity: {sim1:.4f}  (expected ≈ 1.0 — same direction)")

v3 = np.array([1.0, 0.0, 0.0])
v4 = np.array([0.0, 1.0, 0.0])
sim2 = cosine_similarity(v3, v4)
print(f"\n  v3={v3}, v4={v4}")
print(f"  Similarity: {sim2:.4f}  (expected = 0.0 — perpendicular vectors)")

v5 = np.array([0.8, 0.3, 0.5, 0.1])
v6 = np.array([0.7, 0.4, 0.6, 0.2])
sim3 = cosine_similarity(v5, v6)
print(f"\n  v5={v5}, v6={v6}")
print(f"  Similarity: {sim3:.4f}  (high similarity — vectors point in similar directions)")
