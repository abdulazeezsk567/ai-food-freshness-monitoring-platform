import sys
import sqlite3

def run_query(query=None):
    conn = sqlite3.connect('food_freshness.db')
    cursor = conn.cursor()

    if not query:
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
        else:
            query = "SELECT name FROM sqlite_master WHERE type='table';"

    print(f"\n[Executing Query]: {query}\n")

    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT") or query.strip().upper().startswith("PRAGMA"):
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            
            # Print Header
            header = " | ".join([f"{col:18s}" for col in col_names])
            print(header)
            print("-" * len(header))

            # Print Rows
            for row in rows:
                row_str = " | ".join([f"{str(val):18s}" for val in row])
                print(row_str)
            print(f"\nTotal Rows: {len(rows)}\n")
        else:
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}\n")
    except Exception as e:
        print(f"SQL Error: {e}\n")
    finally:
        conn.close()

if __name__ == "__main__":
    run_query()
