from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.notes import router as notes_router
from api.users import router as users_router
from tracing.tracer import enable_tracing

app = FastAPI(title="Tracing Demo Backend")

# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

enable_tracing()

app.include_router(notes_router, prefix="/api/notes", tags=["notes"])
app.include_router(users_router, prefix="/api/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tracing Demo API"}

