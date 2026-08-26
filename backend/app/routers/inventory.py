from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.inventory import Inventory
from app.models.food_item import FoodItem
from app.models.user import User
from app.schemas.inventory import InventoryCreate, InventoryResponse, InventoryUpdate
from app.core.security import get_current_active_user
from app.core.permissions import require_roles

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

def compute_inventory_status(inv: Inventory) -> tuple[int, str]:
    today = date.today()
    days_left = (inv.expiry_date - today).days
    if days_left < 0:
        status_label = "Spoiled"
    elif days_left <= 2:
        status_label = "Near Spoilage"
    elif days_left <= 5:
        status_label = "Acceptable"
    elif days_left <= 10:
        status_label = "Good"
    else:
        status_label = "Fresh"
    return days_left, status_label

def prepare_inventory_response(inv: Inventory) -> InventoryResponse:
    days_left, status_label = compute_inventory_status(inv)
    resp = InventoryResponse.model_validate(inv)
    resp.days_to_expiry = days_left
    resp.status = status_label
    return resp

@router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(
    inv_in: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    food_item = db.query(FoodItem).filter(FoodItem.id == inv_in.food_item_id).first()
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id {inv_in.food_item_id} does not exist"
        )

    inventory_item = Inventory(
        food_item_id=inv_in.food_item_id,
        batch_number=inv_in.batch_number,
        quantity=inv_in.quantity,
        unit=inv_in.unit,
        purchase_date=inv_in.purchase_date,
        expiry_date=inv_in.expiry_date,
        storage_temperature=inv_in.storage_temperature,
        storage_humidity=inv_in.storage_humidity,
        packaging_type=inv_in.packaging_type,
        storage_duration=inv_in.storage_duration
    )
    db.add(inventory_item)
    db.commit()
    db.refresh(inventory_item)
    
    # Reload with food_item relationship
    inv_full = db.query(Inventory).options(joinedload(Inventory.food_item)).filter(Inventory.id == inventory_item.id).first()
    return prepare_inventory_response(inv_full)

@router.get("", response_model=List[InventoryResponse])
def list_inventory(
    category: Optional[str] = Query(None, description="Filter by category"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by calculated freshness status"),
    search: Optional[str] = Query(None, description="Search by batch number or item name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Inventory).options(joinedload(Inventory.food_item)).join(FoodItem)
    if category:
        query = query.filter(FoodItem.category == category)
    if search:
        query = query.filter(
            (Inventory.batch_number.ilike(f"%{search}%")) | (FoodItem.name.ilike(f"%{search}%"))
        )

    items = query.order_by(Inventory.expiry_date.asc()).all()
    results = [prepare_inventory_response(item) for item in items]

    if status_filter:
        results = [item for item in results if item.status.lower() == status_filter.lower()]

    return results

@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).options(joinedload(Inventory.food_item)).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory batch record not found")
    return prepare_inventory_response(inv)

@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    inv_in: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).options(joinedload(Inventory.food_item)).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory batch record not found")

    if inv_in.food_item_id is not None:
        food = db.query(FoodItem).filter(FoodItem.id == inv_in.food_item_id).first()
        if not food:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target food item not found")
        inv.food_item_id = inv_in.food_item_id

    if inv_in.batch_number is not None:
        inv.batch_number = inv_in.batch_number
    if inv_in.quantity is not None:
        inv.quantity = inv_in.quantity
    if inv_in.unit is not None:
        inv.unit = inv_in.unit
    if inv_in.purchase_date is not None:
        inv.purchase_date = inv_in.purchase_date
    if inv_in.expiry_date is not None:
        inv.expiry_date = inv_in.expiry_date
    if inv_in.storage_temperature is not None:
        inv.storage_temperature = inv_in.storage_temperature
    if inv_in.storage_humidity is not None:
        inv.storage_humidity = inv_in.storage_humidity
    if inv_in.packaging_type is not None:
        inv.packaging_type = inv_in.packaging_type
    if inv_in.storage_duration is not None:
        inv.storage_duration = inv_in.storage_duration

    db.commit()
    db.refresh(inv)
    return prepare_inventory_response(inv)

@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMINISTRATOR", "RETAIL_MANAGER", "WAREHOUSE_OPERATOR", "FOOD_QUALITY_INSPECTOR"]))
):
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory batch record not found")

    db.delete(inv)
    db.commit()
    return None
