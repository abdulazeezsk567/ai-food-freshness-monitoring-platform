from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.food_item import FoodItem, FoodCategory
from app.models.inventory import Inventory
from app.core.security import get_password_hash

def seed_database(db: Session):
    # Seed Users if not already present
    if db.query(User).count() == 0:
        users_data = [
            ("System Admin", "admin@foodfreshness.com", "Admin123!", UserRole.ADMINISTRATOR.value),
            ("Sarah Retailer", "retail@foodfreshness.com", "Manager123!", UserRole.RETAIL_MANAGER.value),
            ("David Inspector", "inspector@foodfreshness.com", "Inspector123!", UserRole.FOOD_QUALITY_INSPECTOR.value),
            ("Warehouse Dave", "warehouse@foodfreshness.com", "Warehouse123!", UserRole.WAREHOUSE_OPERATOR.value),
            ("Alice Consumer", "consumer@foodfreshness.com", "Consumer123!", UserRole.CONSUMER.value),
        ]
        created_users = []
        for name, email, raw_password, role in users_data:
            user = User(
                name=name,
                email=email,
                password_hash=get_password_hash(raw_password),
                role=role,
                is_active=True
            )
            db.add(user)
            created_users.append(user)
        db.commit()

    admin_user = db.query(User).filter(User.role == UserRole.ADMINISTRATOR.value).first()

    # Seed Food Items if not present
    if db.query(FoodItem).count() == 0 and admin_user:
        items_data = [
            ("Organic Gala Apples", FoodCategory.FRUITS.value, "Crisp sweet organic Gala apples from local orchards"),
            ("Fresh Hass Avocados", FoodCategory.FRUITS.value, "Ripe creamy Hass avocados"),
            ("Baby Spinach Leaves", FoodCategory.VEGETABLES.value, "Washed and ready-to-eat organic baby spinach"),
            ("Whole Dairy Milk 1L", FoodCategory.DAIRY.value, "Pasteurized fresh whole milk in glass bottle"),
            ("Free Range Chicken Breast", FoodCategory.MEAT_POULTRY.value, "Skinless fresh chicken breast cuts"),
            ("Wild Atlantic Salmon Fillet", FoodCategory.SEAFOOD.value, "Freshly caught Atlantic salmon fillets"),
            ("Artisanal Sourdough Bread", FoodCategory.BAKERY.value, "Freshly baked organic sourdough loaf"),
            ("Rolled Whole Oats 1kg", FoodCategory.PACKAGED.value, "100% whole grain premium rolled oats"),
            ("Cold Pressed Orange Juice", FoodCategory.BEVERAGES.value, "Pure fresh squeezed unpasteurized orange juice"),
        ]
        for name, category, desc in items_data:
            food = FoodItem(
                name=name,
                category=category,
                description=desc,
                created_by=admin_user.id
            )
            db.add(food)
        db.commit()

    # Seed Inventory Batches if not present
    if db.query(Inventory).count() == 0:
        today = date.today()
        apples = db.query(FoodItem).filter(FoodItem.name == "Organic Gala Apples").first()
        milk = db.query(FoodItem).filter(FoodItem.name == "Whole Dairy Milk 1L").first()
        salmon = db.query(FoodItem).filter(FoodItem.name == "Wild Atlantic Salmon Fillet").first()
        spinach = db.query(FoodItem).filter(FoodItem.name == "Baby Spinach Leaves").first()

        batches = []
        if apples:
            batches.append(Inventory(
                food_item_id=apples.id,
                batch_number="BATCH-APP-2026-01",
                quantity=150.0,
                unit="kg",
                purchase_date=today - timedelta(days=5),
                expiry_date=today + timedelta(days=14),
                storage_temperature=3.5,
                storage_humidity=88.0,
                packaging_type="Wooden Crate",
                storage_duration=19
            ))
        if milk:
            batches.append(Inventory(
                food_item_id=milk.id,
                batch_number="BATCH-MLK-2026-04",
                quantity=45.0,
                unit="liters",
                purchase_date=today - timedelta(days=3),
                expiry_date=today + timedelta(days=2), # Expiring Soon
                storage_temperature=2.0,
                storage_humidity=75.0,
                packaging_type="Glass Bottle",
                storage_duration=5
            ))
        if salmon:
            batches.append(Inventory(
                food_item_id=salmon.id,
                batch_number="BATCH-SLM-2026-09",
                quantity=20.0,
                unit="kg",
                purchase_date=today - timedelta(days=7),
                expiry_date=today - timedelta(days=1), # Expired / Spoiled
                storage_temperature=1.0,
                storage_humidity=90.0,
                packaging_type="Vacuum Sealed",
                storage_duration=6
            ))
        if spinach:
            batches.append(Inventory(
                food_item_id=spinach.id,
                batch_number="BATCH-SPN-2026-12",
                quantity=30.0,
                unit="units",
                purchase_date=today - timedelta(days=2),
                expiry_date=today + timedelta(days=5), # Acceptable
                storage_temperature=4.0,
                storage_humidity=85.0,
                packaging_type="Plastic Tray",
                storage_duration=7
            ))

        for b in batches:
            db.add(b)
        db.commit()
