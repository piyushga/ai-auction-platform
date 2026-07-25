# AI Auction Intelligence Platform

## Run the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
uvicorn app.main:app --reload
```

Open `http://localhost:8000/health`.

## Run the frontend

```powershell
cd frontend
npm install
npm run dev
```
