import React, { useState } from "react";
import Webcam from "../components/Webcam";
import { recognizeFace } from "../api";

export default function Recognize() {
  const [capturedImage, setCapturedImage] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCapture = async (dataUrl) => {
    setCapturedImage(dataUrl);
    setResults(null);
    setError("");
    setLoading(true);

    try {
      const data = await recognizeFace(dataUrl);
      if (data.success) {
        setResults(data.faces);
      } else {
        setError(data.message || "Recognition failed.");
      }
    } catch (err) {
      setError("Request failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h3 className="mb-4">Recognize face</h3>

      <div className="row">
        <div className="col-md-6">
          <Webcam onCapture={handleCapture} />
        </div>

        <div className="col-md-6">
          {loading && <p>Analyzing...</p>}

          {error && <div className="alert alert-danger">{error}</div>}

          {results && results.length === 0 && (
            <div className="alert alert-warning">No face detected in the photo.</div>
          )}

          {results &&
            results.map((face, idx) => (
              <div
                key={idx}
                className={`card p-3 mb-2 ${
                  face.is_known ? "border-success" : "border-danger"
                }`}
              >
                <h5 className={face.is_known ? "text-success" : "text-danger"}>
                  {face.is_known ? "✅" : "❌"} {face.name}
                </h5>
                <p className="mb-0 text-muted">
                  Similarity: {(face.similarity * 100).toFixed(1)}%
                </p>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
