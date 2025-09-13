# Porter Saathi – A VOICE FIRST DRIVER ASSISTANT (by TEAM HackHers)

An AI-driven **voice-first assistant** for Porter driver-partners, developed by **Team HackHers** for **Chhalaang 4.0**.  
This project bridges the literacy gap by enabling conversational access to earnings, penalties, business insights and an accesible 'Guru' for Life skills.

---

## 🚀 Features
- 🎙 **Voice Input (Mic Support):** Drivers interact using speech instead of text.
- 📊 **Simplified Finance:** Query daily earnings like *“Aaj ka kharcha kaat ke kitna kamaya?”*.
- 🗂 **Service Layer Logic:** Matches spoken tokens to business data stored in the database. 
- 🌐 **Full-Stack Setup:** React (frontend) + FastAPI (backend).

---

## 🏗 Project Structure
```
hackHers-businessManager/
│
├── backend/               # FastAPI Backend
│   ├── main.py            # App entrypoint
│   ├── db.py              # Database connection
│   ├── models/            # DB Models (Driver, Earnings, etc.)
│   ├── routers/           # API Routers (saathi endpoints)
│   └── services/          # Business logic for voice queries
│
└── frontend/              # React Frontend
    └── vite-project/      # Vite + React setup
        ├── src/           # Components & Pages
        ├── package.json   # Frontend dependencies
        └── vite.config.js # Vite configuration
```

---

## ⚙️ Setup Instructions

### 1. Backend (FastAPI)
```bash
cd backend
# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r ../requirements.txt

# Run FastAPI server
uvicorn main:app --reload
```
Backend runs at: **http://127.0.0.1:8000**

---

### 2. Frontend (React + Vite)
```bash
cd frontend/vite-project

# Install dependencies
npm install

# Start dev server
npm run dev
```
Frontend runs at: **http://localhost:5173**

---

## 🧩 Tech Stack
- **Frontend:** React (Vite, JSX, Tailwind optional)
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite (dev) / PostgreSQL (future)
- **AI/NLP (Future Scope):** HuggingFace / OpenAI Whisper for STT

---

## 📌 Future Scope
- 📱 Extend to mobile app (React Native/Flutter).
- 🌍 Vernacular support with NLP for Regional languages.
- 🔐 Integration with DigiLocker, insurance & govt services.
- ⚡ Real-time safety alerts with GPS/voice.

---

## 👩‍💻 Team
**HackHers** – Innovating for Empowerment 🚀
