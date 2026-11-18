import React, { useRef, useEffect } from "react";

export default function Webcam({ onCapture }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: { width: 480, height: 360 } })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => {
        console.error("Camera access denied:", err);
      });
  }, []);

  const capture = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = 480;
    canvas.height = 360;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, 480, 360);
    const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
    onCapture(dataUrl);
  };

  return (
    <div className="text-center">
      <video
        ref={videoRef}
        autoPlay
        muted
        width="480"
        height="360"
        className="rounded border mb-2"
      />
      <canvas ref={canvasRef} style={{ display: "none" }} />
      <div>
        <button className="btn btn-primary" onClick={capture}>
          Capture photo
        </button>
      </div>
    </div>
  );
}
