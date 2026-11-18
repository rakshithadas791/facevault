"""
Phase 3/4/5: Flask Backend
Endpoints:
  POST /api/register    -> register a new person from uploaded image(s)
  POST /api/recognize    -> recognize face(s) in an uploaded image
  GET  /api/history       -> recognition history
  GET  /api/dashboard    -> stats for dashboard
  GET  /api/persons       -> list all registered persons
"""

import io
import base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

import database
import face_detection
import face_recognition as fr

app = Flask(__name__)
CORS(app)

database.init_db()


def decode_image(base64_string):
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    return np.array(img)


@app.route("/api/register", methods=["POST"])
def register():
    payload = request.get_json()
    name = payload.get("name", "").strip()
    images = payload.get("images", [])  # list of base64 strings

    if not name or not images:
        return jsonify({"success": False, "message": "Name and at least one image are required."}), 400

    person_id = database.add_person(name)
    saved_count = 0

    for img_b64 in images:
        try:
            image_array = decode_image(img_b64)
            face = face_detection.detect_largest_face(image_array)

            if face is None:
                continue

            embedding = fr.get_embedding(face["face_pixels"])
            database.add_embedding(person_id, embedding)
            saved_count += 1

        except Exception as e:
            print(f"Error processing image for {name}: {e}")

    if saved_count == 0:
        return jsonify({"success": False, "message": "No face detected in any uploaded image."}), 400

    return jsonify({
        "success": True,
        "message": f"Registered {name} with {saved_count} face sample(s).",
        "person_id": person_id
    })


@app.route("/api/recognize", methods=["POST"])
def recognize():
    payload = request.get_json()
    image_b64 = payload.get("image")

    if not image_b64:
        return jsonify({"success": False, "message": "No image provided."}), 400

    try:
        image_array = decode_image(image_b64)
        faces = face_detection.detect_faces(image_array)
        known_embeddings = database.get_all_embeddings()

        results = []
        for face in faces:
            embedding = fr.get_embedding(face["face_pixels"])
            name, similarity, is_known = fr.find_best_match(embedding, known_embeddings)

            database.add_history(name, similarity, is_known)

            results.append({
                "name": name,
                "similarity": similarity,
                "is_known": is_known,
                "box": face["box"]
            })

        return jsonify({"success": True, "faces": results})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def history():
    limit = request.args.get("limit", 50, type=int)
    rows = database.get_history(limit)
    return jsonify({"success": True, "history": rows})


@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    stats = database.get_dashboard_stats()
    return jsonify({"success": True, "stats": stats})


@app.route("/api/persons", methods=["GET"])
def persons():
    rows = database.get_all_persons()
    return jsonify({"success": True, "persons": rows})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
