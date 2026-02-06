from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def get_current_user():
    return {
        "status": "success",
        "user": {
            "id": 1,
            "username": "hemantadmin",
            "role": "admin"
        }
    }

@router.post("/login")
async def login():
    return {"status": "success", "message": "Login successful", "token": "fake-jwt-token"}
