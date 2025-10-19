import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale);

export default function Analytics() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/analytics/stats")
      .then((r) => setStats(r.data))
      .catch(console.error);
  }, []);

  if (!stats)
    return (
      <div className="page">
        <p>Loading analytics...</p>
      </div>
    );

  const categories = stats.categories || {};
  const chartData = {
    labels: Object.keys(categories),
    datasets: [{ label: "Count", data: Object.values(categories) }],
  };

  return (
    <div className="page">
      <h2>Dataset Analytics</h2>
      <p>Total products: {stats.num_products}</p>
      <p>Average price: {stats.avg_price}</p>
      <div style={{ maxWidth: 600 }}>
        <Bar data={chartData} />
      </div>
    </div>
  );
}
