from flask import Flask, jsonify, render_template
import sqlite3

from flask_cors import CORS
app = Flask(__name__)
CORS(app)


def fetch_rows(limit=100):
    conn = sqlite3.connect("jobs_data.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT timestamp, linkedin, indeed, ziprecruiter, total,
               search, location, radius, remote
        FROM job_counts
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/history")
def history():
    return jsonify(fetch_rows())

if __name__ == "__main__":
    app.run(debug=True)
