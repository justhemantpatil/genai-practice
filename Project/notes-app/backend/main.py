# -----------------------------
# Database & ORM setup
# -----------------------------
from database import engine
import models

# -----------------------------
# FastAPI core imports
# -----------------------------
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

# -----------------------------
# Application schemas (Pydantic)
# -----------------------------
import schemas

# -----------------------------
# Authentication & authorization helpers
# -----------------------------
from auth import (
    get_db,             # DB session provider
    admin_only,         # Ensures only admin users can access certain routes
    hash_password,      # Hashes plain text passwords
    verify_password,    # Verifies password during login
    create_access_token,# Creates JWT access token
    get_current_user    # Retrieves authenticated user from token
)

# -----------------------------
# Middleware imports
# -----------------------------
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# Tracing (function call tracing for logs / knowledge graph)
# -----------------------------
from tracing.tracer import enable_tracing

# -----------------------------
# Utilities
# -----------------------------
import json
from datetime import datetime
import os


# =====================================================
# FastAPI application initialization
# =====================================================
app = FastAPI(title="Notes App")

# -----------------------------------------------------
# Enable CORS so React frontend can communicate
# -----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# Enable backend function-call tracing
# (Used for logging & Neo4j knowledge graph)
# -----------------------------------------------------
enable_tracing()

# -----------------------------------------------------
# Create database tables if they don't exist
# -----------------------------------------------------
models.Base.metadata.create_all(bind=engine)


# =====================================================
# Health check / root endpoint
# =====================================================
@app.get("/")
def root():
    """
    Root endpoint to verify backend service is running.
    Useful for health checks.
    """
    return {"message": "Backend is running"}


# =====================================================
# Admin-only: Create new users
# =====================================================
@app.post("/admin/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    """
    Creates a new user.
    - Accessible only by admin users.
    - Password is securely hashed before storing.
    """
    db_user = models.User(
        name=user.name,
        username=user.username,
        password=hash_password(user.password),
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# =====================================================
# User login endpoint
# =====================================================
@app.post("/login")
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates user credentials.
    - Verifies username and password
    - Returns JWT access token on success
    """
    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if not user or not verify_password(data.password, user.password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# =====================================================
# Get currently logged-in user's information
# =====================================================
@app.get("/me", response_model=schemas.UserResponse)
def get_my_info(current_user=Depends(get_current_user)):
    """
    Returns details of the currently authenticated user.
    """
    return current_user


# =====================================================
# Update current user's profile
# =====================================================
@app.put("/me", response_model=schemas.UserResponse)
def update_my_profile(
    data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Updates profile details of the logged-in user.
    """
    current_user.username = data.username
    db.commit()
    db.refresh(current_user)
    return current_user


# =====================================================
# Create a new note
# =====================================================
@app.post("/notes", response_model=schemas.NoteResponse)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Creates a new note for the authenticated user.
    """
    new_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


# =====================================================
# Get all notes for the logged-in user
# =====================================================
@app.get("/notes", response_model=list[schemas.NoteResponse])
def get_my_notes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retrieves all notes belonging to the current user.
    """
    return db.query(models.Note).filter(
        models.Note.owner_id == current_user.id
    ).all()


# =====================================================
# Update an existing note
# =====================================================
@app.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id: int,
    data: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Updates a note if it belongs to the logged-in user.
    """
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()

    if not note:
        return {"error": "Note not found"}

    if data.title is not None:
        note.title = data.title
    if data.content is not None:
        note.content = data.content

    db.commit()
    db.refresh(note)
    return note


# =====================================================
# Delete a note
# =====================================================
@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Deletes a note owned by the current user.
    """
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()

    if not note:
        return {"error": "Note not found"}

    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}


# =====================================================
# Receive and store UI (frontend) logs
# =====================================================
@app.post("/ui-logs")
async def receive_ui_logs(request: Request):
    """
    Receives logs sent from frontend (React app).
    Stores them in a file for later analysis and correlation
    with backend traces.
    """
    try:
        payload = await request.json()

        # Ensure log file directory exists
        log_dir = os.path.dirname("frontend.logs")
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        with open("frontend.logs", "a", encoding="utf-8") as f:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                **payload
            }
            f.write(json.dumps(log_entry) + "\n")
            f.flush()

        print(
            f"[UI_LOG] Received and logged: "
            f"{payload.get('function', 'unknown')} "
            f"from {payload.get('file', 'unknown')}"
        )

        return {"status": "ok"}

    except Exception as e:
        print(f"[UI_LOG_ERROR] Failed to log: {str(e)}")
        return {"status": "error", "message": str(e)}
