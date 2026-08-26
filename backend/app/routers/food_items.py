from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.food_item import FoodItem
from app.models.user import User
from app.schemas.food_item import FoodItemCreate, FoodItemResponse, FoodItemUpdate
from app.core.security import get_current_active_user
from app.core.permissions import require_roles

router = APIRouter(prefix="/api/food-items", tags=["Food Items"])

@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
def create_food_item(
    food_in: FoodItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    food_item = FoodItem(
        name=food_in.name,
        category=food_in.category,
        description=food_in.description,
        created_by=current_user.id
    )
    db.add(food_item)
    db.commit()
    db.refresh(food_item)
    return food_item

@router.get("", response_model=List[FoodItemResponse])
def list_food_items(
    category: Optional[str] = Query(None, description="Filter by food category"),
    search: Optional[str] = Query(None, description="Search by item name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(FoodItem)
    if category:
        query = query.filter(FoodItem.category == category)
    if search:
        query = query.filter(FoodItem.name.ilike(f"%{search}%"))
    return query.order_by(FoodItem.name.asc()).all()

@router.get("/{item_id}", response_model=FoodItemResponse)
def get_food_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    item = db.query(FoodItem).filter(FoodItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
    return item

@router.put("/{item_id}", response_model=FoodItemResponse)
def update_food_item(
    item_id: int,
    food_in: FoodItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    item = db.query(FoodItem).filter(FoodItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
    
    # Non-admins/inspectors can only update items they created
    if current_user.role not in ["ADMINISTRATOR", "FOOD_QUALITY_INSPECTOR", "RETAIL_MANAGER", "WAREHOUSE_OPERATOR"] and item.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if food_in.name is not None:
        item.name = food_in.name
    if food_in.category is not None:
        item.category = food_in.category
    if food_in.description is not None:
        item.description = food_in.description

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMINISTRATOR", "RETAIL_MANAGER", "FOOD_QUALITY_INSPECTOR"]))
):
    item = db.query(FoodItem).filter(FoodItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")

    db.delete(item)
    db.commit()
    return None
