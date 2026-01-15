from database import engine
import models
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas
from auth import get_db, admin_only, hash_password
from auth import verify_password, create_access_token
from auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from tracing.tracer import enable_tracing



app = FastAPI(title="Notes App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

enable_tracing()
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/admin/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
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

@app.post("/login")
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserResponse)
def get_my_info(current_user=Depends(get_current_user)):
    return current_user


@app.put("/me", response_model=schemas.UserResponse)
def update_my_profile(
    data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    current_user.username = data.username
    db.commit()
    db.refresh(current_user)
    return current_user


@app.post("/notes", response_model=schemas.NoteResponse)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes", response_model=list[schemas.NoteResponse])
def get_my_notes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Note).filter(
        models.Note.owner_id == current_user.id
    ).all()


@app.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id: int,
    data: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
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

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()

    if not note:
        return {"error": "Note not found"}

    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}

