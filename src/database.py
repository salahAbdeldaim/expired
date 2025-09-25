import sqlite3
import os
import flet as ft

DB_NAME = "pharmacy.db"

def get_db_path(page):
    base_dir = os.path.join(os.path.expanduser("~"), ".pharmacy_app")  
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, DB_NAME)


def get_connection(db_path):
    return sqlite3.connect(db_path)

def init_db(db_path):
    print(f"📂 Database path: {db_path}")  # يطبع المسار في الكونسول
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # الجداول زي ما هي
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_en TEXT NOT NULL UNIQUE,
        name_ar TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity >= 0),
        price REAL NOT NULL CHECK(price >= 0),
        expiry_month INTEGER NOT NULL CHECK(expiry_month BETWEEN 1 AND 12),
        expiry_year INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (type_id) REFERENCES types(id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pharmacy_name TEXT NOT NULL,
        phone_number TEXT,
        theme_mode TEXT CHECK(theme_mode IN ('light', 'dark')) DEFAULT 'light'
    )
    """)

    # فهارس
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_name ON items(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_type ON items(type_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_expiry ON items(expiry_year, expiry_month)")

    # بيانات أولية
    cursor.execute("SELECT COUNT(*) FROM types")
    if cursor.fetchone()[0] == 0:
        medicine_types = [
            ("Tablet", "أقراص"),
            ("Syrup", "شراب"),
            ("Injection", "حقن"),
            ("Capsule", "كبسولات"),
            ("Ointment", "مرهم"),
            ("Drops", "نقط"),
            ("Spray", "بخاخ"),
        ]
        cursor.executemany("INSERT INTO types (name_en, name_ar) VALUES (?, ?)", medicine_types)

    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO settings (pharmacy_name, phone_number, theme_mode) VALUES (?, ?, ?)",
            ("My Pharmacy", "0100000000", "light")
        )

    conn.commit()
    conn.close()


