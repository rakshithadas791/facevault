import React, { useState } from "react";
import Webcam from "../components/Webcam";
import { registerPerson } from "../api";

export default function Register() {
  const [name, setName] = useState("");
  const [images, setImages] = useState([]);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCapture = (dataUrl) => {
    setImages((prev) => [...prev, dataUrl]);
  };

  const handleSubmit = async () => {
    if (!name.trim()) {
      setMessage({ type: "danger", text: "Enter a name first." });
      return;
    }
    if (images.length === 0) {
      setMessage({ type: "danger", text: "Capture at least one photo first." });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const result = await registerPerson(name.trim(), images);
      setMessage({
        type: result.success ? "success" : "danger",
        text: result.message,
      });
      if (result.success) {
        setName("");
        setImages([]);
      }
    } catch (err) {
      setMessage({ type: "danger", text: "Request failed. Is the backend running?" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h3 className="mb-4">Register person</h3>

      <div className="row">
        <div className="col-md-6">
          <Webcam onCapture={handleCapture} />
        </div>

        <div className="col-md-6">
          <div className="mb-3">
            <label className="form-label">Name</label>
            <input
              type="text"
              className="form-control"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Rakshitha"
            />
          </div>

          <p className="text-muted">
            Captured photos: <strong>{images.length}</strong> (capture 3-5 for
            best accuracy)
          </p>

          <div className="d-flex flex-wrap gap-2 mb-3">
            {images.map((img, idx) => (
              <img
                key={idx}
                src={img}
                alt={`capture-${idx}`}
                width="70"
                height="52"
                className="rounded border"
              />
            ))}
          </div>

          <button
            className="btn btn-primary w-100"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? "Registering..." : "Register"}
          </button>

          {message && (
            <div className={`alert alert-${message.type} mt-3`}>
              {message.text}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
