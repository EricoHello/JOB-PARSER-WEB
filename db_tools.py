# db_tools.py
import sqlite3
from datetime import datetime

DB_PATH = "jobs_data.db"  # adjust if different

def view_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM job_counts ORDER BY timestamp DESC;")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

def delete_latest():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        DELETE FROM job_counts
        WHERE timestamp = (SELECT MAX(timestamp) FROM job_counts)
    """)
    conn.commit()
    conn.close()
    print("Deleted latest entry.")

def insert_manual(linkedin, indeed, ziprecruiter, total, search, location, radius, remote):
    ts = datetime.now().isoformat(timespec="seconds")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO job_counts
        (timestamp, linkedin, indeed, ziprecruiter, total, search, location, radius, remote)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, linkedin, indeed, ziprecruiter, total, search, location, radius, remote))
    conn.commit()
    conn.close()
    print(f"Inserted manual entry with timestamp {ts}")

if __name__ == "__main__":
    print("Options:")
    print("1) View all")
    print("2) Delete latest")
    print("3) Insert manual")
    choice = input("Select option: ")

    if choice == "1":
        view_all()
    elif choice == "2":
        delete_latest()
    elif choice == "3":
        linkedin = int(input("LinkedIn count: "))
        indeed = int(input("Indeed count: "))
        zipr = int(input("ZipRecruiter count: "))
        total = int(input("Total count: "))
        search = input("Search term: ")
        location = input("Location: ")
        radius = input("Radius: ")
        remote = input("Remote (On/Off): ")
        insert_manual(linkedin, indeed, zipr, total, search, location, radius, remote)
    else:
        print("Invalid option.")
