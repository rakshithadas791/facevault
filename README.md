# FaceVault — AI-Powered Face Recognition Web App

Deep learning face recognition system: MTCNN (detection) + FaceNet (recognition)
+ Cosine Similarity (matching), served via Flask, with a React + Bootstrap frontend.

## Tech Stack

| Part | Technology |
|---|---|
| Frontend | React.js + Bootstrap |
| Backend | Python + Flask |
| Face Detection | MTCNN |
| Face Recognition | FaceNet (keras-facenet) |
| Deep Learning Framework | TensorFlow/Keras |
| Matching | Cosine Similarity |
| Database | SQLite |
| Image Processing | OpenCV + Pillow |

## Folder Structure

```
FaceVault/
├── backend/
│   ├── app.py                # Flask API (register/recognize/history/dashboard)
│   ├── database.py           # SQLite setup + queries
│   ├── face_detection.py     # MTCNN wrapper
│   ├── face_recognition.py   # FaceNet embeddings + cosine similarity
│   ├── test_pipeline.py      # Standalone Phase 2 test (no website needed)
│   └── requirements.txt
├── frontend/
│   ├── public/index.html
│   └── src/
│       ├── App.js
│       ├── api.js
│       ├── components/ (Navbar, Webcam)
│       └── pages/ (Home, Register, Recognize, History)
└── README.md
```

---

## PHASE 1 — Setup

**Install prerequisites:**
- Python 3.9 or 3.10 (best TensorFlow/MTCNN compatibility)
- Node.js (v18+) — https://nodejs.org
- VS Code (or any editor)
- Git (optional)

**Backend setup:**
```
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

**Frontend setup:**
```
cd frontend
npm install
```

By the end of Phase 1: environment ready, dependencies installed, folders in place.

---

## PHASE 2 — Face Detection + Deep Learning Model (test without the website)

Before touching the website, confirm MTCNN + FaceNet work on your machine:

```
cd backend
python test_pipeline.py path/to/person.jpg
```

Expected output:
```
Face detected ✓  (confidence: 0.998, box: [...])
Embedding generated ✓  (length: 512)
```

If this works, the core AI pipeline is confirmed before any web code runs.

---

## PHASE 3 — Registration System

Start the backend:
```
cd backend
python app.py
```
Flask runs on `http://localhost:5000`. This creates `facevault.db` (SQLite)
automatically on first run.

Registration flow: uploaded images → MTCNN detects face → FaceNet generates
embedding → embedding saved to SQLite under that person's name.

---

## PHASE 4 — Face Recognition

Handled by `/api/recognize` in `app.py`:
Image → MTCNN → face crop → FaceNet → embedding → Cosine Similarity vs. all
stored embeddings → best match returned if similarity ≥ 0.65, else "Unknown".

Every recognition attempt (known or unknown) is logged to the `history` table.

---

## PHASE 5 — Web Application (React + Flask)

Start the frontend (with backend already running from Phase 3):
```
cd frontend
npm start
```
Opens `http://localhost:3000` in your browser.

**4 pages:**
1. **Home** — dashboard stats + navigation
2. **Register** — webcam capture, multiple photos, name input
3. **Recognize** — webcam capture, live result with similarity %
4. **History** — table of all past recognition attempts

---

## PHASE 6 — Extra Features (already included)

- ✅ Multiple-face recognition — `/api/recognize` returns a result per detected face
- ✅ Webcam recognition — both Register and Recognize pages use live webcam capture
- ✅ Recognition history — logged automatically, viewable on the History page
- ✅ Dashboard — registered users / total recognitions / known / unknown counts

**Testing checklist before your demo:**
- [ ] Known face → correctly recognized
- [ ] Unknown face → correctly flagged "Unknown"
- [ ] Multiple faces in one frame
- [ ] Different lighting conditions
- [ ] Different face angles
- [ ] No face in frame (should not crash)
- [ ] Different expressions

---

## PHASE 7 — Results + Documentation

**Measure for your report:**
- Recognition accuracy (test known faces N times, record % correct)
- Recognition time (log timestamps around the `/api/recognize` call)
- False-unknown rate (known face wrongly marked Unknown)
- False-match rate (wrong person matched)

**Suggested report structure:**
1. Introduction
2. Problem statement
3. Objectives
4. Existing system
5. Proposed system
6. Methodology
7. System architecture (see diagram below)
8. Technologies used
9. Implementation
10. Results
11. Advantages
12. Limitations
13. Future scope
14. Conclusion

**System architecture:**
```
IMAGE
  ↓
MTCNN (face detection)
  ↓
FACE CROP (160x160)
  ↓
FaceNet (deep CNN → embedding)
  ↓
FACE EMBEDDING (512-d vector)
  ↓
COSINE SIMILARITY vs. stored embeddings
  ↓
MATCH?  ──yes──> KNOWN PERSON
  │
  no
  ↓
UNKNOWN
```

**Viva prep — be ready to explain:**
- What is a CNN, and why FaceNet uses one
- MTCNN's 3-stage detection pipeline (P-Net, R-Net, O-Net)
- What a face embedding represents geometrically
- Why cosine similarity (not Euclidean distance) was chosen here
- Difference between face detection and face recognition
- How "Unknown" is decided (threshold-based rejection)
- Role of Flask (API layer) vs React (UI layer)
- Why SQLite was sufficient here (no need for a full RDBMS at this scale)

---

## Notes

- `keras-facenet` downloads pretrained weights automatically on first run —
  make sure you have an internet connection the first time you run
  `test_pipeline.py` or `app.py`.
- Cosine similarity threshold is set in `face_recognition.py`
  (`SIMILARITY_THRESHOLD = 0.65`). Raise it for stricter matching, lower it
  if real matches are being marked "Unknown".
- Webcam access via `getUserMedia()` requires `localhost` or HTTPS — this is
  why both frontend (`localhost:3000`) and backend (`localhost:5000`) run
  locally during your demo.
