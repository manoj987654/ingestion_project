import sqlite3

try:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables:", tables)

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        print(f"{table_name}: {cursor.fetchone()[0]} rows")

    conn.close()

except Exception as e:
    print(e)