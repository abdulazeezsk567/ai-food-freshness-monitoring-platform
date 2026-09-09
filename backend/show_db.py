import sqlite3

def display_db():
    conn = sqlite3.connect('food_freshness.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if not row[0].startswith('sqlite_')]

    print("================================================================================")
    print("                    FOOD FRESHNESS MONITORING DATABASE                          ")
    print("================================================================ utility =======\n")

    for table in tables:
        print(f"--- TABLE: {table.upper()} ---")
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]
        print("  Columns: " + ", ".join(columns))
        print("  " + "-" * 75)

        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        if not rows:
            print("  (No records found)\n")
            continue

        for idx, row in enumerate(rows, 1):
            print(f"  [{idx}]")
            for col_name, val in zip(columns, row):
                if col_name == 'password_hash':
                    val = f"{str(val)[:25]}... [HASHED BCRYPT]"
                print(f"      - {col_name:20s}: {val}")
            print()
        print()

    conn.close()

if __name__ == "__main__":
    display_db()
