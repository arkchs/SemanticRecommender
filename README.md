# Product Recommendation / Analytics Web App

This repository contains a minimal end-to-end demonstration of a Product Recommendation Web App using FastAPI (backend) and React (frontend). It includes starter notebooks for data analytics and model training.

Structure

- backend/: FastAPI app
- frontend/: React app (create-react-app style)
- notebooks/: Model training and analytics notebooks (starter)

Quick start (development)

1. Create a Python virtual environment and install backend dependencies:

   python -m venv .venv
   source .venv/Scripts/activate # on Windows (bash)
   pip install -r backend/requirements.txt

2. Run the backend:

   uvicorn backend.main:app --reload --port 8000

3. Start the frontend (requires Node.js):

   cd frontend
   npm install
   npm start

Notes

- This is a starter scaffold. You will need to provide Pinecone API key or configure FAISS for local vector DB.
- Notebooks in `notebooks/` are templates with comments to guide model training and analytics.
