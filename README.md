# Task Manager Project

This project consists of two main parts:

- **Backend:** A Flask API with GraphQL and SQLite database.
- **Frontend:** A React app that communicates with the backend via GraphQL.

---



## Running Locally

### Backend
```bash
cd task_manager/backend
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python app.py
```

### Running the Frontend Locally
```bash
cd task_manager/frontend
npm install
npm start
```

## Notes

- Update the backend GraphQL endpoint URL in `frontend/src/App.js` to point to your running backend (local or deployed).
- Use `npm run build` in the frontend folder to create a production build for deployment.
- The backend uses SQLite for easy local setup.
- When deploying, update frontend API URLs to the live backend URL.

