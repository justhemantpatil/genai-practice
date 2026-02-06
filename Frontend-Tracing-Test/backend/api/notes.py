from fastapi import APIRouter
from services.logic import process_note_data, get_all_notes

router = APIRouter()

@router.get("/")
async def list_notes():
    notes = get_all_notes()
    return {"status": "success", "data": notes}

@router.post("/add")
async def add_note(title: str, content: str):
    result = process_note_data(title, content)
    return {"status": "success", "message": "Note added", "result": result}
