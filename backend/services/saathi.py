from db import SessionLocal
from models.earnings import Earnings
from models.driver import Driver
from datetime import date, timedelta
from sqlalchemy import cast, Date, func

def handle_transcript(transcript: str, driver_id: int) -> str:
    db = SessionLocal()
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    lang = driver.language if driver else "en"
    db.close()

    transcript = transcript.lower().strip()
    print(f"📥 Transcript: {transcript} | Language: {lang}")

    if lang == "hi":
        return handle_hindi(transcript, driver_id)
    elif lang == "kn":
        return handle_kannada(transcript, driver_id)
    else:
        return handle_english(transcript, driver_id)

# -------------------- Hindi --------------------

def handle_hindi(transcript: str, driver_id: int) -> str:
    if any(phrase in transcript for phrase in ["कमाया", "कमाई", "पैसा", "कितना कमाया"]):
        return get_today_earnings(driver_id)

    elif any(phrase in transcript for phrase in ["जुर्माना", "penalty"]):
        return explain_penalty(driver_id)

    elif any(phrase in transcript for phrase in ["बेहतर", "बिजनेस", "व्यापार", "business"]):
        return compare_business(driver_id)

    elif "डिजीलॉकर" in transcript or "digilocker" in transcript:
        return handle_digilocker(transcript, lang="hi")

    return "Maaf kijiye, main abhi is sawaal ka jawaab dene mein saksham nahi hoon."

# -------------------- English --------------------

def handle_english(transcript: str, driver_id: int) -> str:
    if any(phrase in transcript for phrase in ["earnings", "how much did i earn", "today's income"]):
        return get_today_earnings(driver_id)

    elif any(phrase in transcript for phrase in ["penalty", "fine", "charge"]):
        return explain_penalty(driver_id)

    elif any(phrase in transcript for phrase in ["business", "growth", "better than last week"]):
        return compare_business(driver_id)

    elif "digilocker" in transcript:
        return handle_digilocker(transcript, lang="en")

    return "Sorry, I couldn't understand your question yet."

# -------------------- Kannada --------------------

def handle_kannada(transcript: str, driver_id: int) -> str:
    if any(phrase in transcript for phrase in ["ಎಷ್ಟು ಸಂಪಾದನೆ", "ಹಣ", "ಇಂದು ಎಷ್ಟು", "ಸಂಪಾದನೆ"]):
        return get_today_earnings(driver_id)

    elif any(phrase in transcript for phrase in ["ದಂಡ", "penalty", "ಜುರ್ಮಾನಾ"]):
        return explain_penalty(driver_id)

    elif any(phrase in transcript for phrase in ["ವ್ಯಾಪಾರ", "ಬೆಳೆದಿದೆ", "business"]):
        return compare_business(driver_id)

    elif "ಡಿಜಿಲೋಕರ್" in transcript or "digilocker" in transcript:
        return handle_digilocker(transcript, lang="kn")

    return "ಕ್ಷಮಿಸಿ, ನಾನು ಈ ಪ್ರಶ್ನೆಯನ್ನು ಇನ್ನೂ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಾಗಿಲ್ಲ."

# -------------------- Shared Logic --------------------

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
    db = SessionLocal()
    today = date.today()
    start_this_week = today - timedelta(days=today.weekday())
    start_last_week = start_this_week - timedelta(days=7)
    end_last_week = start_this_week - timedelta(days=1)

    last_week_total = db.query(func.sum(Earnings.amount)).filter(
        Earnings.driver_id == driver_id,
        cast(Earnings.date, Date) >= start_last_week,
        cast(Earnings.date, Date) <= end_last_week
    ).scalar() or 0

    this_week_total = db.query(func.sum(Earnings.amount)).filter(
        Earnings.driver_id == driver_id,
        cast(Earnings.date, Date) >= start_this_week,
        cast(Earnings.date, Date) <= today
    ).scalar() or 0

    db.close()

    if last_week_total == 0 and this_week_total == 0:
        return "Pichle do hafton ka business data uplabdh nahi hai."

    if last_week_total == 0:
        return f"Is hafte ₹{this_week_total} kamaye, lekin pichle hafte ka data nahi mila."

    change = this_week_total - last_week_total
    percent = round((change / last_week_total) * 100, 2)

    if change > 0:
        return f"Shubh samachar! Aapka business is hafte {percent}% behtar hai pichle hafte ke mukable."
    elif change < 0:
        return f"Is hafte business {abs(percent)}% kam raha pichle hafte ke mukable."
    else:
        return "Business is hafte bilkul pichle hafte jaisa hi raha."

def handle_digilocker(transcript: str, lang: str) -> str:
    if lang == "hi":
        if any(word in transcript for word in ["upload", "अपलोड", "डालना"]):
            return "DigiLocker par document upload karne ke liye app kholen, login karein, aur 'Upload Documents' section mein jaakar file choose karein."
        elif any(word in transcript for word in ["delete", "हटाना", "डिलीट", "remove"]):
            return "Document delete karne ke liye DigiLocker app mein 'My Documents' section kholen, document select karein, aur delete option dabayein."
        elif any(word in transcript for word in ["verify", "सत्यापन", "check", "confirm"]):
            return "DigiLocker mein document verify karne ke liye 'Issued Documents' section mein jaakar QR code ya reference number ka use karein."
        return "DigiLocker se sambandhit sawaal ke liye main uplabdh hoon."

    elif lang == "en":
        if "upload" in transcript:
            return "To upload a document in DigiLocker, open the app, log in, and go to 'Upload Documents'."
        elif "delete" in transcript:
            return "To delete a document, go to 'My Documents', select the file, and tap delete."
        elif "verify" in transcript:
            return "To verify a document, use the QR code or reference number in the 'Issued Documents' section."
        return "I can help with DigiLocker. Please specify upload, delete, or verify."

    elif lang == "kn":
        if any(word in transcript for word in ["ಅಪ್‌ಲೋಡ್", "upload"]):
            return "ಡಿಜಿಲೋಕರ್‌ನಲ್ಲಿ ಡಾಕ್ಯುಮೆಂಟ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಲು, ಅಪ್‌ ತೆರೆಯಿರಿ, ಲಾಗಿನ್ ಮಾಡಿ ಮತ್ತು 'Upload Documents' ವಿಭಾಗಕ್ಕೆ ಹೋಗಿ."
        elif any(word in transcript for word in ["delete", "ಅಳಿಸು", "remove"]):
            return "ಡಾಕ್ಯುಮೆಂಟ್ ಅಳಿಸಲು 'My Documents' ವಿಭಾಗದಲ್ಲಿ ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತು delete ಒತ್ತಿರಿ."
        elif any(word in transcript for word in ["verify", "ಪರಿಶೀಲನೆ", "check"]):
            return "ಡಾಕ್ಯುಮೆಂಟ್ ಪರಿಶೀಲಿಸಲು 'Issued Documents' ವಿಭಾಗದಲ್ಲಿ QR ಕೋಡ್ ಅಥವಾ reference number ಬಳಸಿ."
        return "ಡಿಜಿಲೋಕರ್ ಸಹಾಯಕ್ಕಾಗಿ upload, delete ಅಥವಾ verify ಅನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಹೇಳಿ."

    return "DigiLocker query samajh nahi aaya. Kripya upload/delete/verify batayein."
