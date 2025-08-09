# parse_email.py
import os, re, imaplib, email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("GMAIL_USER")
PASS = os.getenv("GMAIL_APP_PASSWORD")
IMAP_HOST = "imap.gmail.com"
SENDER = "alert@distill.io"
LIMIT = 200  # how many recent emails to scan

PATS = [
    re.compile(r"([\d,]+)\+?\s*(results|jobs)\b", re.I),       # "25+ jobs", "335 results", "7 jobs"
    re.compile(r"([\d,]+)\s+\w+\s+jobs\s+in\b", re.I),         # "146 It jobs in Seattle, WA"
]

def decode_subject(raw_subj):
    if not raw_subj: return ""
    parts = decode_header(raw_subj)
    out = []
    for text, enc in parts:
        out.append(text.decode(enc or "utf-8", errors="ignore") if isinstance(text, bytes) else text)
    return " ".join(out)

def get_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                return re.sub(r"<[^>]+>", " ", part.get_payload(decode=True).decode(errors="ignore"))
    payload = msg.get_payload(decode=True)
    return payload.decode(errors="ignore") if payload else ""

def extract_count(text):
    if not text: return None
    for p in PATS:
        m = p.search(text)
        if m: return int(m.group(1).replace(",", ""))
    return None

def detect_source(subject):
    s = subject.lower()
    if "linkedin" in s: return "LinkedIn"
    if "indeed" in s: return "Indeed"
    if "zip" in s: return "ZipRecruiter"
    return None

def main():
    if not USER or not PASS:
        print("Missing GMAIL_USER or GMAIL_APP_PASSWORD"); return

    with imaplib.IMAP4_SSL(IMAP_HOST) as M:
        M.login(USER, PASS)
        M.select("INBOX")
        typ, data = M.search(None, f'(FROM "{SENDER}")')
        ids = data[0].split()
        if not ids:
            print("No Distill emails found."); return

        # Look from newest to oldest, keep first hit per source
        results = {}  # source -> count
        for msg_id in reversed(ids[-LIMIT:]):
            typ, msgdata = M.fetch(msg_id, "(RFC822)")
            msg = email.message_from_bytes(msgdata[0][1])

            subject = decode_subject(msg.get("Subject", ""))
            source = detect_source(subject)
            if not source or source in results:
                continue

            body = get_text(msg)
            count = extract_count(subject) or extract_count(body)
            if count is not None:
                results[source] = count

            if len(results) == 3:  # got LinkedIn, Indeed, ZipRecruiter
                break

        # Print whatever we found, consistently ordered
        for src in ["LinkedIn", "Indeed", "ZipRecruiter"]:
            if src in results:
                print(f"{src}: {results[src]}")

        print(f"Total: {sum(results.values())}")
        print("Search: IT, Location: Seattle, WA 25 miles, Remote: On")

        import sqlite3
        from datetime import datetime

        conn = sqlite3.connect("jobs_data.db")
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS job_counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            linkedin INTEGER,
            indeed INTEGER,
            ziprecruiter INTEGER,
            total INTEGER,
            search TEXT,
            location TEXT,
            radius TEXT,
            remote TEXT
        )
        """)

        current = (
            results.get("LinkedIn"),
            results.get("Indeed"),
            results.get("ZipRecruiter"),
            sum(results.values()),
            "IT",
            "Seattle, WA",
            "25 miles",
            "On"
        )

        # Select last full row to detect duplicates
        c.execute("""
        SELECT linkedin, indeed, ziprecruiter, total, search, location, radius, remote
        FROM job_counts
        ORDER BY timestamp DESC
        LIMIT 1
        """)
        last = c.fetchone()

        if last == current:
            print("No change; skipping DB insert.")
        else:
            c.execute("""
            INSERT INTO job_counts (timestamp, linkedin, indeed, ziprecruiter, total, search, location, radius, remote)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(timespec="seconds"), *current))
            conn.commit()

        conn.close()



if __name__ == "__main__":
    main()

import sqlite3

def read_history():
    conn = sqlite3.connect("jobs_data.db")
    c = conn.cursor()
    for row in c.execute("SELECT timestamp, linkedin, indeed, ziprecruiter, total, search, location, radius, remote FROM job_counts ORDER BY timestamp DESC"):
        print(row)
    conn.close()

if __name__ == "__main__":
    read_history()
