"""
Phase 2/4: Face Recognition using FaceNet
Input: cropped face pixels (160x160 RGB, from face_detection.py)
Output: 128-d (or 512-d depending on model) embedding vector

Matching uses Cosine Similarity between embeddings.
"""

import numpy as np
from keras_facenet import FaceNet

# Loads a pretrained FaceNet model (downloaded automatically on first run)
embedder = FaceNet()

SIMILARITY_THRESHOLD = 0.65  # cosine similarity above this = match


def get_embedding(face_pixels):
    """
    face_pixels: numpy array, shape (160, 160, 3)
    Returns: 512-d embedding as a plain Python list (for JSON/SQLite storage)
    """
    face_pixels = np.expand_dims(face_pixels, axis=0)
    embedding = embedder.embeddings(face_pixels)[0]
    return embedding.tolist()


def get_embeddings_batch(list_of_face_pixels):
    """Batch version - faster when processing multiple faces from one image."""
    batch = np.array(list_of_face_pixels)
    embeddings = embedder.embeddings(batch)
    return [e.tolist() for e in embeddings]


def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def find_best_match(query_embedding, known_embeddings):
    """
    known_embeddings: list of {"person_id", "name", "embedding"}
    Returns: (name, similarity, is_known)
    """
    if not known_embeddings:
        return "Unknown", 0.0, False

    best_name = "Unknown"
    best_score = -1.0

    for entry in known_embeddings:
        score = cosine_similarity(query_embedding, entry["embedding"])
        if score > best_score:
            best_score = score
            best_name = entry["name"]

    is_known = best_score >= SIMILARITY_THRESHOLD
    final_name = best_name if is_known else "Unknown"

    return final_name, round(best_score, 4), is_known
