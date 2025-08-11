from flask import Flask, jsonify, render_template
import os, psycopg2
from dotenv import load_dotenv

load_dotenv()
PG_URL = os.getenv("DATABASE_URL")


from flask_cors import CORS
app = Flask(__name__)
CORS(app)


def fetch_rows(limit=100):
    conn = psycopg2.connect(PG_URL)
    cur = conn.cursor()
    cur.execute("""
      SELECT timestamp, linkedin, indeed, ziprecruiter, total,
             search, location, radius, remote
      FROM job_counts
      ORDER BY timestamp DESC
      LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    keys = ["timestamp","linkedin","indeed","ziprecruiter","total","search","location","radius","remote"]
    return [dict(zip(keys, r)) for r in rows]

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/history")
def history():
    return jsonify(fetch_rows())

if __name__ == "__main__":
    app.run(debug=True)
