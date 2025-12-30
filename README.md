# akilli_servis4
AI Tabanlı Öğrenci Servis Takip ve Ebeveyn Bildirim Sistemi

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
