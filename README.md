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
│   ├── datasets/
│   └── __init__.py
```

---

## 🚀 Getting Started (Docker)

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the Repository
```bash
git clone https://github.com/DheerajAluru/eda_bot.git
cd eda_bot
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
![image](https://drive.google.com/uc?export=view&id=1JXt5WNzridKwe35zsjq_v0eHbCNQrmVB)
![image](https://drive.google.com/uc?export=view&id=1SJztEe_WK7kNCvtgFAnGD-WKC7riIGrx)

---

## Future Improvements
- Prompts given from gemini api tend to return inaccurate summary about the dataset which can be improved further by more precise prompt engineering.
- Although executing the genrated code in E2B is secure, the output from the E2B execution results can be refined further to have more detailed infomration in the frontend.
- The current state of front end is very simple with a very basic layout. This can be enhanced more for a better look and feel
- There can be an option introduced to let users see the dataset information and then chose specific column wise plottings. This also includes adding more filters.
- The current fastapi implementation can be refactored more with more custom exception handling and adding more validations for edge cases.