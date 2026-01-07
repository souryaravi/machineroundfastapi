from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.email import send_email
from app.schemas import UserCreate, UserLogin
from app.models import User
from app.database import get_db
from app.auth import hash_password, verify_password, create_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_email(
        to_email=user.email,
        subject="Welcome to SSH Manager",
        body=f"Hello,\n\nYour account has been created successfully.\n\nThanks!"
    )

    return {"msg": "Registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.email})
    return {"access_token": token}

