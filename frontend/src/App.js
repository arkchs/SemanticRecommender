import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Recommend from "./pages/Recommend";
import Analytics from "./pages/Analytics";

export default function App() {
  return (
    <div className="app-root">
      <nav className="topnav">
        <Link to="/">Recommend</Link>
        <Link to="/analytics">Analytics</Link>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Recommend />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
    </div>
  );
}
