import React, { useEffect, useState } from "react";
import { getHistory } from "../api";

export default function History() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getHistory()
      .then((data) => setHistory(data.history))
      .catch(() => setError("Could not reach backend. Is Flask running on port 5000?"));
  }, []);

  return (
    <div className="container">
      <h3 className="mb-4">Recognition history</h3>

      {error && <div className="alert alert-warning">{error}</div>}

      {history.length === 0 && !error && (
        <p className="text-muted">No recognition attempts yet.</p>
      )}

      {history.length > 0 && (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Person</th>
              <th>Result</th>
              <th>Similarity</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {history.map((row) => (
              <tr key={row.id}>
                <td>{row.result_name}</td>
                <td>
                  {row.is_known ? (
                    <span className="badge bg-success">Recognized</span>
                  ) : (
                    <span className="badge bg-danger">Unknown</span>
                  )}
                </td>
                <td>{(row.similarity * 100).toFixed(1)}%</td>
                <td>{new Date(row.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
