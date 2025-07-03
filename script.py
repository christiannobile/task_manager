import os

project_name = "task_manager"
backend_dir = os.path.join(project_name, "backend")
frontend_dir = os.path.join(project_name, "frontend")

files = {
    os.path.join(backend_dir, "app", "main.py"): """\
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.post("/tasks")
def create_task(task: dict, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.get("title"),
        description=task.get("description", ""),
        completed=task.get("completed", False),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.get("title", db_task.title)
    db_task.description = task.get("description", db_task.description)
    db_task.completed = task.get("completed", db_task.completed)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
""",

    os.path.join(backend_dir, "requirements.txt"): """\
fastapi
uvicorn[standard]
sqlalchemy
""",

    os.path.join(backend_dir, "Dockerfile"): """\
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
""",

    os.path.join(backend_dir, "README.md"): """\
# Task Manager Backend

This is the FastAPI backend for the Task Manager app with SQLite persistence.

## Run locally

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

## Docker

Build and run with:

docker build -t task-manager-backend .
docker run -p 8080:8080 task-manager-backend
""",

    os.path.join(project_name, ".gitignore"): """\
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.env.*
*.db
.vscode/
.DS_Store
""",

    os.path.join(frontend_dir, "README.md"): """\
# Task Manager Frontend

Flutter frontend scaffold for Task Manager.

## Run

flutter pub get
flutter run

Connect this frontend to backend by updating API URLs in your Dart code.
""",

    os.path.join(frontend_dir, "pubspec.yaml"): """\
name: task_manager_frontend
description: A simple Flutter frontend scaffold for the Task Manager app.
publish_to: 'none' 
version: 0.0.1
environment:
  sdk: ">=2.17.0 <3.0.0"
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.4
dev_dependencies:
  flutter_test:
    sdk: flutter
flutter:
  uses-material-design: true
""",

    os.path.join(frontend_dir, "lib", "main.dart"): """\
import 'package:flutter/material.dart';

void main() {
  runApp(const TaskManagerApp());
}

class TaskManagerApp extends StatelessWidget {
  const TaskManagerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Task Manager',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const Scaffold(
        body: Center(child: Text('Task Manager Frontend - Work in Progress')),
      ),
    );
  }
}
""",
}

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_files():
    for path, content in files.items():
        ensure_dir(path)
        with open(path, "w") as f:
            f.write(content)
    print(f"✅ Project '{project_name}' structure created successfully.")

if __name__ == "__main__":
    write_files()
