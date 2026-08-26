from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import get_current_active_user, get_password_hash
from app.core.permissions import require_roles

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMINISTRATOR", "FOOD_QUALITY_INSPECTOR", "RETAIL_MANAGER"]))
):
    return db.query(User).order_by(User.id.desc()).all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Non-admins can only fetch their own user profile unless they are admins/inspectors
    if current_user.role not in ["ADMINISTRATOR", "FOOD_QUALITY_INSPECTOR"] and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Users can update themselves, Admins can update anyone
    if current_user.role != "ADMINISTRATOR" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_in.name is not None:
        user.name = user_in.name
    if user_in.email is not None:
        existing = db.query(User).filter(User.email == user_in.email, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken")
        user.email = user_in.email
    if user_in.role is not None and current_user.role == "ADMINISTRATOR":
        user.role = user_in.role.upper()
    if user_in.is_active is not None and current_user.role == "ADMINISTRATOR":
        user.is_active = user_in.is_active
    if user_in.password is not None:
        user.password_hash = get_password_hash(user_in.password)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMINISTRATOR"]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete current admin user")

    db.delete(user)
    db.commit()
    return None
