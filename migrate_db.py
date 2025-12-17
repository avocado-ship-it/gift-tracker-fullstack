import sqlite3

conn = sqlite3.connect('gifts.db')
cursor = conn.cursor()

# Add completed column to existing table
try:
    cursor.execute('ALTER TABLE gifts ADD COLUMN completed INTEGER DEFAULT 0')
    conn.commit()
    print("Successfully added 'completed' column to gifts table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column 'completed' already exists")
    else:
        print(f"Error: {e}")

conn.close()
