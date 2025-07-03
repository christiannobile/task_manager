# Task Manager Project

This project consists of two main parts:

- **Backend:** A Flask API with GraphQL and SQLite database.
- **Frontend:** A React app that communicates with the backend via GraphQL.

---

## To Do List for Deployment

### Backend (Google Cloud Free Tier)
- [ ] Create a Google Cloud account if you don't have one.
- [ ] Install and configure Google Cloud SDK (`gcloud` CLI).
- [ ] Prepare a Docker image for the backend.
- [ ] Push the Docker image to Google Container Registry (GCR).
- [ ] Deploy the backend using Google Cloud Run (serverless container hosting).
- [ ] Configure environment variables and CORS if needed.
- [ ] Ensure backend URL is accessible and update frontend to use this URL.

### Frontend (GitHub Pages)

✅ Build the React frontend (`npm run build`).  
✅ Commit and push the build output to GitHub repository.  
✅ Enable GitHub Pages in the repository settings (serve from `gh-pages` branch or `/docs` folder).  
- [ ] Ensure frontend communicates with the deployed backend URL.  
- [ ] Test frontend live on GitHub Pages.

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

