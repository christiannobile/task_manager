# Task Manager

A full-stack Task Manager application with:

- **Backend**: FastAPI + SQLite  
- **Frontend**: Flutter (mobile and web)

---

## 📁 Project Structure

```
task_manager/
├── backend/           # FastAPI backend
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend/          # Flutter frontend
│   ├── lib/
│   │   └── main.dart
│   ├── pubspec.yaml
│   └── README.md
└── .gitignore
```

---

## 🚀 Backend - FastAPI

### ✅ Features

- REST API to manage tasks (`GET`, `POST`, `PUT`, `DELETE`)
- SQLite database with SQLAlchemy ORM
- Docker support

### 🔧 Setup (Local)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 🐳 Docker

```bash
cd backend
docker build -t task-manager-backend .
docker run -p 8080:8080 task-manager-backend
```

---

## 📱 Frontend - Flutter

### ✅ Features

- Mobile/web-friendly UI
- HTTP support via `http` package
- Scaffolded structure for backend integration

### 🔧 Setup

```bash
cd frontend
flutter pub get
flutter run
```

> 🔗 Make sure to configure the API base URL in your Dart code.

---

## 🌐 API Endpoints

```
GET     /tasks             - List all tasks  
POST    /tasks             - Create a new task  
PUT     /tasks/{id}        - Update a task  
DELETE  /tasks/{id}        - Delete a task
```

---

## 📦 Environment

- Python 3.11+  
- Flutter SDK  
- Docker (optional)  
- Git

---

## 📌 TODO

- [ ] Connect Flutter frontend to backend API  
- [ ] Add authentication (optional)  
- [ ] Deploy frontend (e.g., Firebase Hosting)  
- [ ] Deploy backend (e.g., Google Cloud Run)

---

## 🧑‍💻 Author

**Christian Nobile**  
GitHub: [@christiannobile](https://github.com/christiannobile)
