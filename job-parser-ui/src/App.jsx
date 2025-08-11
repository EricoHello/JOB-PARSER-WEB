// src/App.jsx
import { useEffect, useState } from "react";
import { Pie, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale, PointElement, LineElement
} from "chart.js";

ChartJS.register(
  ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale, PointElement, LineElement
);

const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:5000") + "/api/history";

export default function App() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(API_URL)
      .then(r => r.json())
      .then(data => setRows(Array.isArray(data) ? data : []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 16 }}>Loading…</div>;
  if (!rows.length) return <div style={{ padding: 16 }}>No data yet.</div>;

  const latest = rows[0]; // API returns newest first
  const chronological = [...rows].reverse(); // oldest → newest for line chart

  const pieData = {
    labels: ["LinkedIn", "Indeed", "ZipRecruiter"],
    datasets: [{
      data: [
        latest.linkedin || 0,
        latest.indeed || 0,
        latest.ziprecruiter || 0
      ],
      backgroundColor: [
        "rgba(54, 162, 235, 0.7)",   // LinkedIn
        "rgba(255, 99, 132, 0.7)",   // Indeed
        "rgba(255, 206, 86, 0.7)"    // ZipRecruiter
      ],
      borderColor: [
        "rgba(54, 162, 235, 1)",
        "rgba(255, 99, 132, 1)",
        "rgba(255, 206, 86, 1)"
      ],
      borderWidth: 1
    }]
  };

  const lineData = {
    labels: chronological.map(r => {
      const d = new Date(r.timestamp);
      return `${d.getMonth() + 1}-${d.getDate()}-${String(d.getFullYear()).slice(-2)}`;
    }),
    datasets: [{
      label: "Total jobs",
      data: chronological.map(r => r.total),
      tension: 0.25,
      borderColor: "rgba(75, 192, 192, 1)",   // teal-ish line
      backgroundColor: "rgba(75, 192, 192, 0.2)", // fill under line
      fill: true,
      pointBackgroundColor: "rgba(75, 192, 192, 1)"
    }]
  };


  return (
    <div style={{ margin: "0 auto", maxWidth: 900, padding: 16 }}>
      {/* Header */}
      <header style={{ marginBottom: 12 }}>
        <h1 style={{ margin: 0, fontSize: 22 }}>Job Watch</h1>
        <p style={{ margin: "6px 0", color: "#999" }}>
          Latest snapshot & trend for your tracked roles.
        </p>
      </header>

      {/* Summary */}
      <section
        style={{
          // background: "rgba(75, 192, 192, 0.2)",
          border: "1px solid #eee",
          borderRadius: 10,
          padding: 16,
          marginBottom: 16
        }}
      >
        <div style={{ fontSize: 16, marginBottom: 6 }}>
          <strong>Latest:</strong> LinkedIn {latest.linkedin} · Indeed {latest.indeed} ·
          {" "}ZipRecruiter {latest.ziprecruiter} · <strong>Total {latest.total}</strong>
        </div>
        <div style={{ color: "#999" }}>
          Search: {latest.search}, Location: {latest.location} {latest.radius}, Remote: {latest.remote}
        </div>
      </section>

      {/* Charts (mobile-first stacked) */}
      <div
        style={{
          display: "grid",
          gap: 16,
          gridTemplateColumns: "1fr"
        }}
      >
        {/* Pie */}
        <div
          style={{
            height: 260,
            padding: 35,
            border: "1px solid #eee",
            borderRadius: 10
          }}
        >
          <h3 style={{ fontSize: 16, margin: "0 0 8px 0" }}>Latest breakdown</h3>
          <Pie data={pieData} options={{ maintainAspectRatio: false, plugins: { legend: { labels: { color: "#eee" } } } }} />
        </div>

        {/* Line */}
        <div
          style={{
            height: 300,
            padding: 12,
            border: "1px solid #eee",
            borderRadius: 10
          }}
        >
          <h3 style={{ fontSize: 16, margin: "0 0 8px 0" }}>Totals over time</h3>
          <Line data={lineData} options={{
            maintainAspectRatio: false, plugins: { legend: { labels: { color: "#eee" } } }, scales: {
              x: {
                ticks: {
                  color: "#eee"
                }
              },
              y: {
                ticks: {
                  color: "#eee"
                }
              }
            }
          }} />
        </div>
      </div>

      {/* Footer */}
      <footer style={{ textAlign: "center", color: "#888", marginTop: 18 }}>
        <small>© {new Date().getFullYear()} Job Watch • Prototype</small>
      </footer>
    </div>
  );
}
