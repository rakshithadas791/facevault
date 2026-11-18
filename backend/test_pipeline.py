"""
Phase 2 standalone test - run BEFORE building the website.
Confirms MTCNN detection + FaceNet embedding work on your machine.

Usage:
    python test_pipeline.py path/to/person.jpg
"""

import sys
import numpy as np
from PIL import Image

import face_detection
import face_recognition as fr


def test_pipeline(image_path):
    print(f"Loading image: {image_path}")
    image = np.array(Image.open(image_path).convert("RGB"))

    print("Running MTCNN face detection...")
    face = face_detection.detect_largest_face(image)

    if face is None:
        print("Face detected ✗  -- no face found in image.")
        return

    print(f"Face detected ✓  (confidence: {round(face['confidence'], 3)}, box: {face['box']})")

    print("Running FaceNet embedding...")
    embedding = fr.get_embedding(face["face_pixels"])

    print(f"Embedding generated ✓  (length: {len(embedding)})")
    print(f"First 5 values: {[round(v, 4) for v in embedding[:5]]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py path/to/person.jpg")
        sys.exit(1)

    test_pipeline(sys.argv[1])
