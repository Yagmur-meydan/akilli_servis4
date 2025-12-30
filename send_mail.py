import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import time

# GMAIL bilgileri
GMAIL_USER = "vesilenurmert13@gmail.com"  #kendi adresim
GMAIL_PASS = "kpim cwce zfvz edec"     # Google'dan aldığım 16 haneli şifre

# Öğrenci–veli listesi
VELI_MAILLERI = {
    "yagmur": "yagmurmeydan597@gmail.com",
    "vesile": "yagmurmeydan597@gmail.com",
    "hatice": "yagmurmeydan597@gmail.com",
    "huseyin": "yagmurmeydan597@gmail.com"
}

print("Sistem başlatıldı, 1 dakika sonra durum kontrolü yapılacak...\n")
time.sleep(60)  # 1 dakika bekle

# Veritabanını oku
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("SELECT name, servis, saat FROM students")
data = cursor.fetchall()
conn.close()

def send_email(to, subject, body):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        print(f" Mail gönderildi → {to}")
    except Exception as e:
        print(f"Mail gönderilemedi → {to}: {e}")

# Her öğrenci için duruma göre mail gönder
for name, servis, saat in data:
    if name in VELI_MAILLERI:
        mail = VELI_MAILLERI[name]
        if servis == "Bindi":
            subject = f"{name.title()} servise bindi "
            body = f"Sayın veli,\n\n{name.title()} saat {saat}’te servise binmiştir.\n\nAkıllı Servis Sistemi "
        else:
            subject = f"{name.title()} servise binmedi "
            body = f"Sayın veli,\n\n{name.title()} servise binmemiştir.\n\nAkıllı Servis Sistemi "
        send_email(mail, subject, body)

print("\nKontrol tamamlandı. Mail gönderimi bitti.")
