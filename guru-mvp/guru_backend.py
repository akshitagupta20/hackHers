from fastapi import FastAPI, File, UploadFile, Request, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
from pydub import AudioSegment
import os
import base64
from io import BytesIO

app = FastAPI(title="Guru MVP — Voice-Enabled Backend")

# ---------------------
# CORS Middleware
# ---------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for dev
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Guides
# ---------------------
guides = {
    "contest_challan": {
        "title": "How to contest a traffic challan online",
        "steps": [
            "Open the Parivahan website (parivahan.gov.in).",
            "Go to the traffic challan section and click 'Contest Challan'.",
            "Enter vehicle number and challan ID.",
            "Upload supporting documents.",
            "Submit and note the reference ID."
        ]
    },
    "upload_digilocker": {
        "title": "How to upload documents to DigiLocker",
        "steps": [
            "Install the DigiLocker app or visit digilocker.gov.in.",
            "Sign in using Aadhaar or mobile number.",
            "Tap 'Upload Document' and choose the document type.",
            "Select the file and confirm upload.",
            "Check confirmation and viewable link."
        ]
    }
}

# ---------------------
# Lessons
# ---------------------
lessons = {
    "vehicle_insurance": {
        "title": "Basics of Vehicle Insurance",
        "short_summary": "Insurance protects you from financial loss due to accidents or theft.",
        "detailed_summary": "Vehicle insurance protects against financial loss due to accidents, theft, or damage."
    },
    "customer_service": {
        "title": "Customer Service Tips",
        "short_summary": "Small gestures improve customer experience.",
        "detailed_summary": "Greet customers politely, keep your vehicle clean, be punctual, communicate delays, help with loading."
    }
}

# ---------------------
# FAQ
# ---------------------
faq = {
    "insurance": {
        "question": "Renew or buy new policy?",
        "options": {
            "renew": "Visit insurer's site, login, choose renew, pay online, and keep receipts.",
            "new": "Compare plans online, choose, enter details, pay and keep policy document."
        }
    }
}

class FAQAnswer(BaseModel):
    topic: str
    choice: str

# ---------------------
# Search helper
# ---------------------
def search_topics(query: str):
    query = query.lower()
    results = {"guides": [], "lessons": []}
    for key, val in guides.items():
        if query in key.lower() or any(query in step.lower() for step in val["steps"]):
            results["guides"].append(key)
    for key, val in lessons.items():
        if query in key.lower() or query in val["title"].lower() or query in val["short_summary"].lower() or query in val["detailed_summary"].lower():
            results["lessons"].append(key)
    return results

# ---------------------
# REST Endpoints
# ---------------------
@app.get("/")
def home(request: Request):
    base_url = str(request.base_url)
    return {"message": "Welcome to Guru MVP 👋", "resources": {
        "guides": f"{base_url}guides",
        "lessons": f"{base_url}lessons",
        "faq": f"{base_url}faq",
        "search": f"{base_url}search?q=",
        "voice_search": f"{base_url}voice_search",
        "ws_voice": f"{base_url}ws/voice"
    }}

@app.get("/guides")
def list_guides(request: Request):
    base_url = str(request.base_url)
    return [{"topic": k, "title": guides[k]["title"], "link": f"{base_url}guide/{k}"} for k in guides]

@app.get("/guide/{topic}")
def get_guide(topic: str):
    return guides.get(topic, {"title": "Not found", "steps": ["No guide found"]})

@app.get("/lessons")
def list_lessons(request: Request):
    base_url = str(request.base_url)
    return [{"topic": k, "title": lessons[k]["title"], "link": f"{base_url}lesson/{k}"} for k in lessons]

@app.get("/lesson/{topic}")
def get_lesson(topic: str):
    return lessons.get(topic, {"title": "Not found", "short_summary":"", "detailed_summary":""})

@app.get("/faq")
def list_faq():
    return [{"topic": k, "question": v["question"]} for k,v in faq.items()]

@app.get("/faq/{topic}")
def get_faq(topic: str):
    return faq.get(topic, {"question":"No FAQ found", "options":{}})

@app.post("/faq/answer")
def answer_faq(data: FAQAnswer):
    topic_data = faq.get(data.topic)
    if not topic_data: return {"answer":"Invalid topic"}
    return {"answer": topic_data["options"].get(data.choice, "No answer found")}

@app.get("/search")
def search(q: str):
    return {"query": q, "results": search_topics(q)}

# ---------------------
# Voice Search (upload)
# ---------------------
@app.post("/voice_search")
async def voice_search(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    wav_file = temp_file
    if file.filename.lower().endswith(".mp3"):
        sound = AudioSegment.from_mp3(temp_file)
        wav_file = temp_file.rsplit(".",1)[0]+".wav"
        sound.export(wav_file, format="wav")

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_file) as source:
            audio = recognizer.record(source)
            query = recognizer.recognize_google(audio, language="en-IN")
    except Exception as e:
        os.remove(temp_file)
        if wav_file != temp_file: os.remove(wav_file)
        return {"error": str(e)}

    os.remove(temp_file)
    if wav_file != temp_file: os.remove(wav_file)

    results = search_topics(query)
    return {"transcribed_text": query, "results": results}

# ---------------------
# WebSocket real-time voice
# ---------------------
@app.websocket("/ws/voice")
async def websocket_voice(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected! Send audio Base64.")

    recognizer = sr.Recognizer()
    while True:
        try:
            data = await websocket.receive_text()
            audio_bytes = base64.b64decode(data)
            audio_file = BytesIO(audio_bytes)

            try:
                sound = AudioSegment.from_file(audio_file)
                audio_file = BytesIO()
                sound.export(audio_file, format="wav")
                audio_file.seek(0)
            except:
                audio_file.seek(0)

            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                query = recognizer.recognize_google(audio, language="en-IN")

            results = search_topics(query)
            await websocket.send_json({"transcribed_text": query, "results": results})
        except Exception as e:
            await websocket.send_json({"error": str(e)})
