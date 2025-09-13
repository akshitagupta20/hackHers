from fastapi import APIRouter, Request
from db import SessionLocal
from models.driver import Driver
from services.saathi import handle_transcript

router = APIRouter()

@router.post("/saathi/login")
async def login(request: Request):
    data = await request.json()
    name = data.get("name", "").strip()
    language = data.get("language", "en").strip()

    db = SessionLocal()
    driver = db.query(Driver).filter(Driver.name == name).first()

    if not driver:
        driver = Driver(name=name, language=language)
        db.add(driver)
        db.commit()
        db.refresh(driver)

    db.close()
    return {"driver_id": driver.id, "language": driver.language}

@router.post("/saathi/respond")
async def respond(request: Request):
    data = await request.json()
    transcript = data.get("transcript", "")
    driver_id = data.get("driver_id")

    if not driver_id:
        return {"message": "Driver ID missing. Please login first."}

    return {"message": handle_transcript(transcript, driver_id)}
