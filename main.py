import json
from fastapi import FastAPI, HTTPException
import uvicorn
from db import fetch_log, fetch_logs, fetch_commits
from sync import sync_commits
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://localhost:8645"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"message": "WorkLogger Backend is running!"}

@app.get("/logs")
def get_logs():
    logs = fetch_logs()
    return logs

@app.get("/logs/{log_id}")
def get_logs(log_id:str):
    log = fetch_log(log_id)
    return log

@app.get("/commits/{session_id}")
def get_commits(session_id: str):
    commits = fetch_commits(session_id)
    if not commits:
        raise HTTPException(status_code=404, detail="Commits not found.")
    return commits

@app.post("/sync/{session_id}")
def sync(session_id: str):
    result = sync_commits(session_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5453, reload=True)
