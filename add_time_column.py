
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Eğer "saat" sütunu yoksa ekle
cursor.execute("PRAGMA table_info(students)")
columns = [info[1] for info in cursor.fetchall()]
if "saat" not in columns:
    cursor.execute("ALTER TABLE students ADD COLUMN saat TEXT DEFAULT '-'")
    print("'saat' sütunu eklendi.")
else:
    print("'saat' sütunu zaten mevcut, işlem gerekmedi.")

conn.commit()
conn.close()
