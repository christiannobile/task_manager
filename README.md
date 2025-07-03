# Task Manager Project

This project contains a **backend** written in Python FastAPI and a **frontend** written in Flutter.

## Backend

- REST API to manage tasks stored in a SQLite database.
- Run backend with: `uvicorn app.main:app --reload` inside the `backend` directory.

## Frontend

- Flutter app that consumes the backend API.
- Use `flutter run` inside the `frontend` directory.
- Change the backend API base URL in `frontend/lib/services/api_service.dart` if needed.

## Structure

- `backend/app/main.py`: FastAPI backend code.
- `frontend/lib`: Flutter app source code.

