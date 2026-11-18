"""
Phase 2: Face Detection using MTCNN
Input: raw image (numpy array, RGB)
Output: cropped, aligned face(s) resized to 160x160 (FaceNet's expected input size)
"""

import numpy as np
from mtcnn import MTCNN
from PIL import Image

detector = MTCNN()


def detect_faces(image_array):
    """
    Detect all faces in an image.
    Returns list of dicts: {box: [x, y, w, h], confidence: float, face_pixels: np.array}
    face_pixels is the cropped face resized to 160x160, ready for FaceNet.
    """
    results = detector.detect_faces(image_array)
    faces = []

    for result in results:
        x, y, w, h = result["box"]
        x, y = max(0, x), max(0, y)

        face = image_array[y:y + h, x:x + w]
        if face.size == 0:
            continue

        face_image = Image.fromarray(face).resize((160, 160))
        face_pixels = np.asarray(face_image)

        faces.append({
            "box": [int(x), int(y), int(w), int(h)],
            "confidence": float(result["confidence"]),
            "face_pixels": face_pixels
        })

    return faces


def detect_largest_face(image_array):
    """Convenience function for registration: returns the single largest detected face, or None."""
    faces = detect_faces(image_array)
    if not faces:
        return None
    faces.sort(key=lambda f: f["box"][2] * f["box"][3], reverse=True)
    return faces[0]
