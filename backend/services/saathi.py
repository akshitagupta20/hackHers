from db import SessionLocal
from models.earnings import Earnings
from datetime import date
from sqlalchemy import cast, Date

def handle_transcript(transcript: str) -> str:
    transcript = transcript.lower().strip()
    print("📥 Received transcript:", transcript)

    if any(phrase in transcript for phrase in ["kamaya", "kamai", "पैसा", "कमाई", "कितना कमाई"]):
        return get_today_earnings(driver_id=1)

    elif "penalty" in transcript or "jurmana" in transcript:
        return explain_penalty(driver_id=1)

    elif "behtar hai ya nahi" in transcript or "business" in transcript:
        return compare_business(driver_id=1)

    return "Maaf kijiye, main abhi is sawaal ka jawaab dene mein saksham nahi hoon."

def get_today_earnings(driver_id: int) -> str:
    db = SessionLocal()
    today = date.today()
    record = db.query(Earnings).filter(
        Earnings.driver_id == driver_id,
        cast(Earnings.date, Date) == today
    ).first()
    db.close()

    if record:
        net = record.amount - record.expenses
        return f"Aapne ₹{net} kamaye aaj, kharche ke baad."
    return "Aaj ka earnings data nahi mila."

def explain_penalty(driver_id: int) -> str:
    db = SessionLocal()
    record = db.query(Earnings).filter(
        Earnings.driver_id == driver_id
    ).order_by(Earnings.date.desc()).first()
    db.close()

    if record and record.penalty_code:
        code = record.penalty_code
        if code == "LATE30":
            return "Aapko ₹30 ka jurmana laga kyunki delivery 30 minute late thi."
        return f"Penalty code '{code}' ke liye abhi koi explanation nahi hai."
    return "Aapke record mein koi jurmana nahi mila."

def compare_business(driver_id: int) -> str:
    return "Pichle hafte ke mukable aapka business 10% behtar hai."  # Stub for now
