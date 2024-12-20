import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_FILE =  os.path.join(os.getenv("USERPROFILE"),"Worklogger",os.getenv("DB_FILE"))

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_logs():
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM logs").fetchall()
    conn.close()
    return [dict(log) for log in logs]

def fetch_commits(session_id):
    conn = get_db_connection()
    commits = conn.execute("SELECT * FROM commits WHERE session_id = ?", (session_id,)).fetchall()
    conn.close()
    return [dict(commit) for commit in commits]

def fetch_log(log_id):
    conn = get_db_connection()
    log = conn.execute("SELECT * FROM logs WHERE id = ?", (log_id,)).fetchone()
    conn.close()
    return log
