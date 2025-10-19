import React, { useState } from "react";
import axios from "axios";
const SERVER_ENDPOINT = process.env.SERVER_ENDPOINT;
export default function Recommend() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleSearch(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.get(
        `${SERVER_ENDPOINT}/recommend?q=${encodeURIComponent(q)}`
      );
      setResults(res.data.results || []);
    } catch (err) {
      console.error(err);
      alert("Error fetching recommendations");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <h2>Product Recommendations</h2>
      <form onSubmit={handleSearch} className="search-form">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Describe what you're looking for (e.g., cozy grey sofa)"
        />
        <button type="submit">Search</button>
      </form>

      {loading && <p>Loading...</p>}

      <div className="results">
        {results.map((r, i) => (
          <div key={i} className="card">
            <h3>{r.metadata?.title || r.metadata?.uniq_id || r.id}</h3>
            <p className="brand">{r.metadata?.brand}</p>
            <p>{r.metadata?.description}</p>
            <div className="generated">
              Generated description (placeholder): A beautiful, handcrafted
              piece designed for modern homes.
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
