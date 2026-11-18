import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar navbar-dark bg-dark mb-4">
      <div className="container">
        <Link className="navbar-brand fw-bold" to="/">
          FaceVault
        </Link>
        <div>
          <Link className="btn btn-outline-light btn-sm me-2" to="/register">
            Register
          </Link>
          <Link className="btn btn-outline-light btn-sm me-2" to="/recognize">
            Recognize
          </Link>
          <Link className="btn btn-outline-light btn-sm" to="/history">
            History
          </Link>
        </div>
      </div>
    </nav>
  );
}
