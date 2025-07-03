from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import List, Optional
import sqlite3

app = FastAPI()

DB_PATH = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Task(BaseModel):
    id: Optional[str]
    title: str
    description: Optional[str] = ""
    due_date: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, due_date, completed, created_at FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return [Task(
        id=row[0], title=row[1], description=row[2],
        due_date=row[3], completed=bool(row[4]),
        created_at=row[5]
    ) for row in rows]

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task.id = str(uuid4())
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (id, title, description, due_date, completed) VALUES (?, ?, ?, ?, ?)",
                (task.id, task.title, task.description, task.due_date, int(task.completed)))
    conn.commit()
    conn.close()
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated: Task):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET title = ?, description = ?, due_date = ?, completed = ? WHERE id = ?",
                (updated.title, updated.description, updated.due_date, int(updated.completed), task_id))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    conn.commit()
    conn.close()
    updated.id = task_id
    return updated

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    conn.close()
    return {"detail": "Task deleted"}
