import time
import datetime

# Test: şu andan 1 dakika sonra kontrol et
print(" Test başlatıldı, sistem 1 dakika içinde otomatik kontrol yapacak...\n")
time.sleep(60)

# Şimdi kontrolü çalıştır
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("SELECT name, servis, saat FROM students")
data = cursor.fetchall()
conn.close()

missing = [name for name, servis, saat in data if servis != "Bindi"]

if not missing:
    print("Tüm öğrenciler servise binmiş.")
else:
    print(" Servise binmeyen öğrenciler:")
    for m in missing:
        print(f"   - {m}")
