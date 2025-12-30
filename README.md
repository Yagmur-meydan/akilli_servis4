# akilli_servis4
Öğrenci Servis Takip ve Ebeveyn Bildirim Sistemi

# 1. Proje Özeti
Bu proje, öğrenci servis araçlarına yerleştirilen kamera sistemi aracılığıyla
öğrencilerin servise **biniş durumunun yüz tanıma teknolojisi** kullanarak
otomatik olarak tespit eden akıllı bir takip ve bildirim sistemidir.
Sistem, elde edilen verileri IoT tabanlı bir yapı üzerinden sunucuya iletir ve
ebeveynleri **gerçek zamanlı bildirimler** ile bilgilendirir.
# 2. Problem Tanımı
- Öğrenci servislerinde manuel yoklama sistemlerinin hataya açık olması  
- Velilerin çocuklarının servise binip binmediğini anlık olarak takip edememesi  
- Olası risklerin geç fark edilmesi
# 3. Projenin Amacı
- Öğrenci güvenliğini artırmak  
- Velilere gerçek zamanlı bilgi sağlamak  
- Servis süreçlerini dijitalleştirmek  
- IoT teknolojilerini entegre etmek 
# 4. Sistem Mimarisi
Sistem aşağıdaki ana bileşenlerden oluşur:
1. **Görüntü Toplama Katmanı**
   - Servis içine yerleştirilen kamera
2. **Görüntü İşleme Katmanı**
   - Yüz algılama
   - Yüz tanıma (LBPH / embedding tabanlı)
3. **Uygulama & İş Mantığı Katmanı**
   - Öğrenci kontrolü
   - Binip/binmeme takibi
4. **Veri Tabanı Katmanı**
   - Öğrenci bilgileri
   - Yüz verileri
   - Zaman kayıtları
5. **Bildirim Katmanı**
   - e-mail
# 5.Çalışma Mimarisi
![Çalışma Mimarisi](diyagram/diyagram.drawio.png)
# 6.Sistem Çalışma Prensibi
Sistem, birden fazla servis bileşeninden oluşan modüler bir yapıya sahiptir.Çift terminal yapısıyla çalışmaktadır.
Uygulama çalıştırılırken ana uygulama ile bildirim servisi ayrı süreçler
olarak başlatılmaktadır.
Ana uygulama (`app.py`), kamera üzerinden alınan görüntüleri işleyerek
öğrenci biniş ve iniş durumlarını tespit eder. Bildirim servisi
(`send_mail.py`) ise backend üzerinde sürekli çalışarak gerekli durumlarda
velilere e-posta bildirimi gönderir.
Bu yapı sayesinde sistem daha esnek, yönetilebilir ve genişletilebilir
hale getirilmiştir.
# 7.Kullanılan Teknolojiler
### Yazılım
- Python
- OpenCV
- MediaPipe
- Flask
- SQLite
### Donanım
- Kamera
- Bilgisayar / Sunucu
# 8.Konfigürasyon
Sistemin doğru şekilde çalışabilmesi için bazı yapılandırma (konfigürasyon)
ayarlarının yapılması gerekmektedir.
### E-posta Bildirim Ayarları
Bildirim servisi (`send_mail.py`), SMTP protokolü üzerinden e-posta
göndermektedir. Bu nedenle aşağıdaki bilgiler yapılandırılmalıdır:
- Gönderen e-posta adresi
- SMTP sunucu adresi
- SMTP port numarası
- E-posta hesap kimlik doğrulama bilgileri
Bu bilgiler, güvenlik nedeniyle doğrudan kod içerisine yazılmamakta,
ortam değişkenleri veya ayrı bir yapılandırma dosyası üzerinden
tanımlanmaktadır.
### Kamera Ayarları
Ana uygulama (`app.py`), varsayılan kamera aygıtı üzerinden görüntü almaktadır.
Farklı bir kamera kullanılması durumunda kamera indeksinin güncellenmesi
gerekmektedir.
### Veri Tabanı Ayarları
Sistem, öğrenci bilgileri ve giriş/çıkış kayıtlarını saklamak için
veri tabanı kullanmaktadır. Veri tabanı bağlantı ayarları uygulama
başlatılmadan önce yapılandırılmalıdır.
#  9.Kurulum
Projeyi çalıştırmadan önce gerekli yazılım bağımlılıklarının kurulması
gerekmektedir.
### Gereksinimler
- Python 3.10
- Kamera erişimi
- İnternet bağlantısı (e-posta bildirimi için)
### Kurulum Adımları
1. Proje deposu klonlanır:
```bash
git clone https://github.com/kullaniciAdi/Aakilli_servis4.git
```
2.Proje dizinine girilir:
```bash
cd akilli_servis4
```
3.Gerekli Python kütüphaneleri yüklenir:
```bash
pip install mediapipe opencv-python flask numpy
```
4.Konfigürasyon ayarları tamamlandıktan sonra ana uygulama başlatılır:
```bash
python app.py
```
5.Bildirim servisi ayrı bir süreç olarak çalıştırılır:
```bash
python send_mail.py
```
6.Tarayıcı açılır.
http://127.0.0.1:5000
veya
http://localhost:5000

# 10.Geliştiriciler
- Yağmur Meydanoğulları  
- Vesile Nur Mert  
- Hatice Nisa Tan

# 11.Lisans
Bu proje eğitim ve akademik amaçlı geliştirilmiştir.
