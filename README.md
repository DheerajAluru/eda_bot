# eda_bot# React + FastAPI CSV/XLSX Data Analyzer

This is a full-stack web application that allows users to upload `.csv` or `.xlsx` files, select a plot type, and receive dynamically generated plots and analysis output from a FastAPI backend powered by Gemini and E2B sandbox execution.

---

## 🔧 Features

- 📊 Upload CSV/XLSX and generate plots (Line, Bar, Scatter)
- ⚙️ Secure sandboxed Python code execution via E2B
- 🔁 Real-time status updates via WebSocket
- 📦 Auto-cleanup of uploaded files and plots
- 💡 Gemini API for auto-generating analysis logic
- 🐳 Dockerized frontend (React) and backend (FastAPI)

---

## 📁 Folder Structure

```
your-project/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   └── Spinner.jsx
│   │   └── index.js
│   └── package.json
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── agent.py
│   ├── utils.py
│   ├── Plots/
│   ├── UploadedFiles/
│   └── __init__.py
```

---

## 🚀 Getting Started (Docker)

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-project.git
cd your-project
```

### 2. Run via Docker Compose
```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

---

## 🛠 Development (Locally)

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

---

## ⚙️ Environment Configuration
If using Gemini API or E2B, create a `.env` in `backend/`:
```env
GEMINI_API_KEY=your_key_here
E2B_API_KEY=your_key_here
```

---

## 🧪 Sample Files
Include test `.csv` and `.xlsx` files in `UploadedFiles/` or via the UI.

---

## 📸 Screenshots
> Add screenshots here to showcase UI and generated plots.

---

## 📄 License
MIT © [Your Name](https://github.com/yourusername)
