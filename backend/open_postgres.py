import os
import sys
import json
import urllib.parse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.session import Base
from app.models.user import User
from app.models.food_item import FoodItem
from app.models.inventory import Inventory
from app.models.analysis import AnalysisResult
from app.services.seed import seed_database

def connect_and_init_postgres(password: str, host: str = "localhost", port: int = 5432, db_name: str = "food_freshness_db"):
    print(f"Connecting to PostgreSQL at {host}:{port} with user 'postgres'...")
    try:
        # 1. Connect to default 'postgres' database via psycopg2
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=password,
            host=host,
            port=port,
            connect_timeout=5
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 2. Check if food_freshness_db exists, create if not
        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (db_name,))
        exists = cursor.fetchone()
        if not exists:
            print(f"Database '{db_name}' does not exist. Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}";')
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")
            
        cursor.close()
        conn.close()

        # 3. Formulate DATABASE_URL (URL-encode password for special characters like @)
        encoded_password = urllib.parse.quote_plus(password)
        pg_url = f"postgresql://postgres:{encoded_password}@{host}:{port}/{db_name}"
        
        # Update .env files
        env_paths = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), ".env")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
        ]
        
        for env_path in env_paths:
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                new_lines = []
                updated = False
                for line in lines:
                    if line.startswith("DATABASE_URL="):
                        new_lines.append(f"DATABASE_URL={pg_url}\n")
                        updated = True
                    else:
                        new_lines.append(line)
                if not updated:
                    new_lines.append(f"DATABASE_URL={pg_url}\n")
                with open(env_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"Updated {env_path} with PostgreSQL connection string.")

        # 4. Connect SQLAlchemy to PostgreSQL
        print("Creating PostgreSQL database tables via SQLAlchemy...")
        engine = create_engine(pg_url)
        Base.metadata.create_all(bind=engine)
        print("All database tables (users, food_items, inventory, analysis_results) created in PostgreSQL!")

        # 5. Seed initial data
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            print("Seeding initial demo data into PostgreSQL...")
            seed_database(db)
            print("Demo data seeded successfully!")
        finally:
            db.close()

        # 6. Query and display table contents
        db = SessionLocal()
        try:
            users_count = db.query(User).count()
            food_count = db.query(FoodItem).count()
            inv_count = db.query(Inventory).count()
            analysis_count = db.query(AnalysisResult).count()
            
            print("\n==================================================")
            print("  POSTGRESQL DATABASE SUMMARY & OVERVIEW")
            print("==================================================")
            print(f"  Database Name   : {db_name}")
            print(f"  Host / Port     : {host}:{port}")
            print(f"  Total Users     : {users_count}")
            print(f"  Food Items      : {food_count}")
            print(f"  Inventory       : {inv_count}")
            print(f"  Analysis Records: {analysis_count}")
            print("==================================================")
            
            print("\n--- Users Table ---")
            for u in db.query(User).all():
                print(f"  ID: {u.id} | Email: {u.email} | Name: {u.name} | Role: {u.role}")
                
            print("\n--- Food Items Table ---")
            for f_item in db.query(FoodItem).all()[:5]:
                print(f"  ID: {f_item.id} | Name: {f_item.name} | Category: {f_item.category}")
                
            print("\n--- Inventory Batches Table ---")
            for inv in db.query(Inventory).all()[:5]:
                print(f"  Batch: {inv.batch_number} | Food ID: {inv.food_item_id} | Qty: {inv.quantity} {inv.unit} | Expiry: {inv.expiry_date} | Temp: {inv.storage_temperature}°C")
                
            print("==================================================\n")
        finally:
            db.close()
            
        return True

    except Exception as e:
        print(f"\nFailed to connect to PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    pwd = sys.argv[1] if len(sys.argv) > 1 else ""
    if not pwd:
        print("Usage: python open_postgres.py <your_postgres_password>")
    else:
        connect_and_init_postgres(pwd)
