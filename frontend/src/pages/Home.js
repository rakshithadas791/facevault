import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getDashboardStats } from "../api";

export default function Home() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getDashboardStats()
      .then((data) => setStats(data.stats))
      .catch(() => setError("Could not reach backend. Is Flask running on port 5000?"));
  }, []);

  return (
    <div className="container">
      <div className="text-center mb-5">
        <h1 className="display-5 fw-bold">FaceVault</h1>
        <p className="text-muted">AI-powered face recognition</p>
        <div className="mt-3">
          <Link to="/register" className="btn btn-primary me-2">
            Register person
          </Link>
          <Link to="/recognize" className="btn btn-success me-2">
            Recognize face
          </Link>
          <Link to="/history" className="btn btn-secondary">
            History
          </Link>
        </div>
      </div>

      {error && <div className="alert alert-warning">{error}</div>}

      {stats && (
        <div className="row text-center">
          <div className="col-md-3 mb-3">
            <div className="card p-3">
              <h6 className="text-muted">Registered users</h6>
              <h3>{stats.registered_users}</h3>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card p-3">
              <h6 className="text-muted">Total recognitions</h6>
              <h3>{stats.total_recognitions}</h3>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card p-3">
              <h6 className="text-muted">Known</h6>
              <h3 className="text-success">{stats.known}</h3>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card p-3">
              <h6 className="text-muted">Unknown</h6>
              <h3 className="text-danger">{stats.unknown}</h3>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
