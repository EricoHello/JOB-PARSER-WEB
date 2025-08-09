import { useEffect, useState } from "react";

export default function App() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/history")
      .then(r => r.json())
      .then(setRows)
      .catch(console.error);
  }, []);

  if (!rows.length) return <div style={{ padding: 16 }}>Loading…</div>;

  const r = rows[0]; // latest
  return (
    <div style={{ padding: 16 }}>
      <h1>Job Counts (Latest)</h1>
      <p>LinkedIn: {r.linkedin} | Indeed: {r.indeed} | ZipRecruiter: {r.ziprecruiter} | Total: {r.total}</p>
      <p>Search: {r.search}, Location: {r.location} {r.radius}, Remote: {r.remote}</p>
    </div>
  );
}
