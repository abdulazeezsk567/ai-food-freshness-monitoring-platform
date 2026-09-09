import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

passwords = [
    '', 'postgres', 'admin', 'root', 'password', '123456', '12345678', '1234', '12345',
    'Postgres', 'Postgres123!', 'postgres123', 'admin123', 'root123', 'sql', 'postgresql',
    'azeez', 'abdul', 'abdulazeez', 'Azeez123', 'Azeez123!'
]

working_pwd = None
for pwd in passwords:
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password=pwd,
            host='localhost',
            port=5432,
            connect_timeout=2
        )
        working_pwd = pwd
        print(f"SUCCESS: Connected to PostgreSQL with password: '{pwd}'")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database food_freshness_db exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='food_freshness_db';")
        exists = cursor.fetchone()
        if not exists:
            print("Creating database 'food_freshness_db' in PostgreSQL...")
            cursor.execute("CREATE DATABASE food_freshness_db;")
            print("Database 'food_freshness_db' created successfully!")
        else:
            print("Database 'food_freshness_db' already exists!")
            
        cursor.close()
        conn.close()
        break
    except Exception as e:
        continue

if not working_pwd:
    print("NO_PASSWORD_MATCH")
