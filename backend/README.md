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
