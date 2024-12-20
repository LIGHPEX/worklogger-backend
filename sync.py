import os
import requests
from dotenv import load_dotenv
from db import fetch_commits

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def sync_commits(session_id):
    commits = fetch_commits(session_id)
    if not commits:
        return {"message": "No commits to sync."}

    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{SUPABASE_URL}/rest/v1/commits"

    for commit in commits:
        response = requests.post(url, json=commit, headers=headers)
        if response.status_code != 201:
            return {"error": f"Failed to sync commit {commit['commit_hash']}."}

    return {"message": "Commits synced successfully."}

