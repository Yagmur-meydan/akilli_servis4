import sqlite3
import time

def create_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        servis TEXT DEFAULT 'Yok',
        saat TEXT DEFAULT '-'
    )
    """)
    conn.commit()
    conn.close()

def add_student(name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO students (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def update_servis(name, durum):
    saat = time.strftime("%H:%M")
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET servis=?, saat=? WHERE name=?", (durum, saat, name))
    conn.commit()
    conn.close()
    print(f" {name} için durum '{durum}' olarak güncellendi ({saat})")

def check_servis(name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT servis FROM students WHERE name=?", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def list_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, servis, saat FROM students ")
    data = cursor.fetchall()
    conn.close()
    return data

def reset_servis():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET servis='Yok', saat='-'")
    conn.commit()
    conn.close()
    print("Servis durumu sıfırlandı.")

# İlk çalıştırmada tabloyu kurar ve öğrenci ekler
if __name__ == "__main__":
    create_db()
    for name in ["yagmur", "vesile", "hatice", "huseyin"]:
        add_student(name)
    print(" Veritabanı hazır:", list_students())
