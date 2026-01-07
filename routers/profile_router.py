from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Profile, User
from app.schemas import ProfileCreate
from fastapi import Depends

router = APIRouter(prefix="/profile", tags=["Profile"])

# ---------------- CREATE PROFILE ----------------
@router.post("/")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db), user_id: int = 1):
    # Check if profile already exists for this user
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")

    # Create new profile
    db_profile = Profile(
        user_id=user_id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        age=profile.age,
        phone=profile.phone,
        photo_url=profile.photo_url
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return {"msg": "Profile created", "profile": db_profile.id}


# ---------------- GET PROFILE ----------------
@router.get("/")
def get_profile(db: Session = Depends(get_db), user_id: int = 1):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# ---------------- UPDATE PROFILE ----------------
@router.put("/")
def update_profile(profile: ProfileCreate, db: Session = Depends(get_db), user_id: int = 1):
    db_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db_profile.first_name = profile.first_name
    db_profile.last_name = profile.last_name
    db_profile.age = profile.age
    db_profile.phone = profile.phone
    db_profile.photo_url = profile.photo_url
    
    db.commit()
    db.refresh(db_profile)
    return {"msg": "Profile updated"}

# ---------------- DELETE PROFILE ----------------
@router.delete("/")
def delete_profile(db: Session = Depends(get_db), user_id: int = 1):
    db_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(db_profile)
    db.commit()
    return {"msg": "Profile deleted"}
