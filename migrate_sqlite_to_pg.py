import sqlite3, psycopg2, os
from dotenv import load_dotenv
load_dotenv()
PG_URL = os.getenv("DATABASE_URL")

sq = sqlite3.connect("jobs_data.db")
rows = sq.execute("""
  SELECT timestamp, linkedin, indeed, ziprecruiter, total, search, location, radius, remote
  FROM job_counts
  ORDER BY timestamp
""").fetchall()
sq.close()

pg = psycopg2.connect(PG_URL); cur = pg.cursor()
for r in rows:
    cur.execute("""
      INSERT INTO job_counts (timestamp, linkedin, indeed, ziprecruiter, total, search, location, radius, remote)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
      ON CONFLICT DO NOTHING
    """, r)
pg.commit(); cur.close(); pg.close()
print(f"Migrated {len(rows)} rows.")
