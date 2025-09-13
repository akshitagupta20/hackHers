from fastapi import APIRouter, Request
from services.saathi import handle_transcript

router = APIRouter()

@router.post("/saathi/respond")
async def respond(request: Request):
    data = await request.json()
    transcript = data.get("transcript", "")
    return {"message": handle_transcript(transcript)}
