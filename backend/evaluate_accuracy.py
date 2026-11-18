"""
FaceVault accuracy evaluation. Run from the backend folder (venv active):
    python evaluate_accuracy.py

Folder layout (create it inside backend/):
    eval_data/
        register/<PersonName>/*.jpg    3-5 photos per person (enrolment)
        test/<PersonName>/*.jpg        NEW photos of the same people (not used in register)
        unknown/*.jpg                  photos of people who are NOT registered

Uses the same MTCNN + FaceNet + cosine similarity code as the app,
but keeps everything in memory (your SQLite database is not touched).
"""

import os
import time
import csv
import numpy as np
from PIL import Image

import face_detection
import face_recognition as fr

ROOT = "eval_data"
THRESHOLDS = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
EXTS = (".jpg", ".jpeg", ".png")


def images_in(folder):
    return [os.path.join(folder, f) for f in sorted(os.listdir(folder))
            if f.lower().endswith(EXTS)]


def embed(path):
    """Returns (embedding, seconds) or (None, seconds) if no face is found."""
    start = time.time()
    img = np.array(Image.open(path).convert("RGB"))
    face = face_detection.detect_largest_face(img)
    if face is None:
        return None, time.time() - start
    return fr.get_embedding(face["face_pixels"]), time.time() - start


def best_match(emb, known):
    best_name, best_score = "Unknown", -1.0
    for entry in known:
        score = fr.cosine_similarity(emb, entry["embedding"])
        if score > best_score:
            best_name, best_score = entry["name"], score
    return best_name, best_score


def main():
    # 1. Enrol people in memory
    known = []
    reg_root = os.path.join(ROOT, "register")
    for person in sorted(os.listdir(reg_root)):
        for path in images_in(os.path.join(reg_root, person)):
            emb, _ = embed(path)
            if emb is not None:
                known.append({"name": person, "embedding": emb})
    print(f"Registered {len(set(k['name'] for k in known))} people, "
          f"{len(known)} embeddings\n")

    # 2. Score every test image once: (true_label, best_name, best_score)
    results, times, no_face = [], [], 0
    test_root = os.path.join(ROOT, "test")
    for person in sorted(os.listdir(test_root)):
        for path in images_in(os.path.join(test_root, person)):
            emb, t = embed(path)
            times.append(t)
            if emb is None:
                no_face += 1
                continue
            name, score = best_match(emb, known)
            results.append((person, name, score))

    unknown_root = os.path.join(ROOT, "unknown")
    for path in images_in(unknown_root):
        emb, t = embed(path)
        times.append(t)
        if emb is None:
            no_face += 1
            continue
        name, score = best_match(emb, known)
        results.append(("Unknown", name, score))

    # 3. Metrics at each threshold
    rows = []
    for th in THRESHOLDS:
        correct_known = wrong_person = false_reject = 0
        correct_unknown = false_accept = 0
        for true, name, score in results:
            predicted = name if score >= th else "Unknown"
            if true == "Unknown":
                if predicted == "Unknown":
                    correct_unknown += 1
                else:
                    false_accept += 1
            else:
                if predicted == true:
                    correct_known += 1
                elif predicted == "Unknown":
                    false_reject += 1
                else:
                    wrong_person += 1
        total = len(results)
        accuracy = (correct_known + correct_unknown) / total * 100 if total else 0
        rows.append([th, total, correct_known, false_reject, wrong_person,
                     correct_unknown, false_accept, round(accuracy, 2)])

    header = ["Threshold", "Images", "Known correct", "False reject",
              "Wrong person", "Unknown correct", "False accept", "Accuracy %"]
    print(" | ".join(f"{h:>15}" for h in header))
    for r in rows:
        print(" | ".join(f"{str(v):>15}" for v in r))

    print(f"\nImages with no face detected (skipped): {no_face}")
    if times:
        print(f"Average time per image (detect + embed): {np.mean(times):.2f} s")

    with open("accuracy_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print("Saved table to accuracy_results.csv")


if __name__ == "__main__":
    main()