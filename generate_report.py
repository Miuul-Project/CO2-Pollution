from fpdf import FPDF
import os
import json

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CO2 Veri Analizi Raporu', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

    def add_image(self, image_path, title=""):
        if os.path.exists(image_path):
            # Page width 210mm. Margins 20mm left, 20mm right.
            # Content width = 210 - 20 - 20 = 170mm.
            self.image(image_path, w=170)
            self.ln(2)
            if title:
                self.set_font('Arial', 'I', 10)
                self.cell(0, 5, title, 0, 1, 'C')
            self.ln(5)
        else:
            self.cell(0, 10, f"Resim bulunamadi: {image_path}", 0, 1)

pdf = PDF()
# Set equal margins: 20mm (2cm) on Left, Top, Right
pdf.set_margins(20, 20, 20)
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=20)

# Helper for Turkish chars
def tr(text):
    mapping = {
        'ğ': 'g', 'Ğ': 'G',
        'ş': 's', 'Ş': 'S',
        'ı': 'i', 'İ': 'I',
        'ç': 'c', 'Ç': 'C',
        'ö': 'o', 'Ö': 'O',
        'ü': 'u', 'Ü': 'U'
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

# Content
pdf.chapter_body(tr("Bu rapor, küresel CO2 emisyon trendlerinin derinlemesine analizini sunmakta, seçilmiş ülkelerin emisyon profillerini karşılaştırmakta ve bu değişimleri yönlendiren temel faktörleri incelemektedir. Çalışma, küresel emisyon modelleri ve gelecek projeksiyonları hakkında veri odaklı içgörüler sağlamayı amaçlamaktadır."))

pdf.chapter_title(tr("Veri ve Metodoloji"))
pdf.chapter_body(tr("Bu analizde kullanilan yontem ve veri detaylari asagidaki gibidir:\n\n"
                    "Veri Seti: 'Our World in Data' (owid-co2-data.csv) kaynakli kuresel CO2 verileri kullanilmistir.\n\n"
                    "On Isleme (Preprocessing):\n"
                    "- Eksik Veriler: Ulke bazinda yillara gore siralanarak 'Linear Interpolation' yontemiyle doldurulmustur.\n"
                    "- Filtreleme: Analizler genelde 1990 sonrasi, tahmin modelleri ise 2000-2024 arasi verilere odaklanmistir.\n\n"
                    "Model Egitimi:\n"
                    "- Regresyon Modeli: Verilerdeki non-lineer egilimleri yakalamak icin 2. Dereceden Polinom Regresyon (Polynomial Regression Degree 2) kullanilmistir.\n"
                    "- Egitim Seti: 2000-2024 yillari arasindaki verilerle model egitilmis, 2025-2030 icin tahmin uretilmistir.\n\n"
                    "Kullanilan Teknolojiler:\n"
                    "- Python: Pandas (Veri Manipulasyonu), Scikit-learn (Makine Ogrenmesi), Matplotlib & Seaborn (Gorsellestirme)."))

# Load metrics
try:
    with open("metrics.json", "r") as f:
        metrics = json.load(f)
    
    pdf.chapter_title(tr("Model Performansı"))
    pdf.chapter_body(tr(f"Modelin güvenilirliğini test etmek için veri seti %{int(metrics['train_split']*100)} Eğitim ve %{int(metrics['test_split']*100)} Test olarak ayrılmıştır.\n"
                        f"- RMSE (Kök Ortalama Kare Hatası): {metrics['rmse']:.2f}\n"
                        f"- MAE (Ortalama Mutlak Hata): {metrics['mae']:.2f}\n"
                        f"- R² Skoru (Belirtme Katsayısı): {metrics['r2']:.2f}\n"
                        "Yüksek R² skoru ve düşük hata oranları, modelin tarihsel verileri başarıyla temsil ettiğini göstermektedir."))
except FileNotFoundError:
    print("metrics.json bulunamadi, model performansi eklenemedi.")

pdf.chapter_title(tr("1. Küresel CO2 Emisyonlarının Tarihsel Gelişimi"))
pdf.chapter_body(tr("Kuresel ortalama CO2 emisyonlari yillar icinde istikrarli bir sekilde artmaktadir."))
pdf.add_image("img/global_co2_trend.png", tr("Kuresel CO2 Trendi"))

pdf.chapter_title(tr("2. Ülke Bazlı Emisyon Profilleri ve Karşılaştırmalı Analiz"))
pdf.chapter_body(tr("Cin, ABD, Rusya, Turkiye ve Almanya'nin CO2 emisyonlarini karsilastirdim.\n"
                    "- Cin: Son yillarda emisyonlarda buyuk bir artis goruldu.\n"
                    "- ABD: Yuksek emisyonlara sahip ancak son zamanlarda hafif bir dusus egilimi var.\n"
                    "- Almanya ve Rusya: Nispeten istikrarli veya hafif dusus egilimi gosteriyor.\n"
                    "- Turkiye: Kademeli bir artis gosteriyor."))
pdf.add_image("img/country_co2_trend.png", tr("Ulke Bazli CO2 Trendi"))

pdf.chapter_title(tr("3. Emisyon Sürücüleri: İstatistiksel Korelasyon Analizi"))
pdf.chapter_body(tr("1990 sonrasi veriler icin CO2, GSYIH, Nufus, Kisi Basi Enerji ve Kisi Basi CO2 arasindaki iliskiyi inceledim.\n"
                    "- CO2, GSYIH ve Nufus ile yuksek korelasyona sahiptir.\n"
                    "- Kisi Basi Enerji, Kisi Basi CO2 ile guclu bir iliskiye sahiptir."))
pdf.add_image("img/correlation_matrix.png", tr("Korelasyon Matrisi"))

pdf.chapter_title(tr("4. Gelecek Projeksiyonları: Küresel CO2 Tahmini (2025-2030)"))
pdf.chapter_body(tr("2000-2024 verileriyle egitilen Polinom Regresyon modeli kullanilarak 2030'a kadar tahmin yapildi.\n"
                    "- Trend, buyuk degisiklikler olmazsa kuresel emisyonlarin artmaya devam edecegini gosteriyor."))
pdf.add_image("img/global_forecast.png", tr("Kuresel Tahmin"))

pdf.chapter_title(tr("5. Bölgesel Tahminler ve Trend Analizi"))
pdf.chapter_body(tr("Tahmin modeli anahtar ulkelere uygulandi:\n"
                    "- Cin: Artis Egiliminde (Dik egim).\n"
                    "- Turkiye: Artis Egiliminde.\n"
                    "- ABD: Dusus Egiliminde.\n"
                    "- Almanya: Dusus Egiliminde.\n"
                    "- Rusya: Istikrarli/Hafif Artis."))
pdf.add_image("img/country_forecasts.png", tr("Ulke Tahminleri"))

pdf.chapter_title(tr("6. Stratejik Öneriler ve Emisyon Azaltım Senaryoları"))
pdf.chapter_body(tr("2050'ye kadar emisyonlari yariya indirmek icin (2024 seviyelerine gore), ulkelerin yillik ciddi azaltimlar yapmasi gerekiyor:\n\n"
                    "Cin (~%2.63 Yillik Azaltim): GSYIH odakli. Oneri: Ekonomik buyumeyi emisyonlardan ayirmaya odaklanin (Yesil Buyume).\n"
                    "ABD (~%2.63): GSYIH odakli. Oneri: Ayirmaya devam edin, verimlilige odaklanin.\n"
                    "Turkiye (~%2.63): Enerji odakli. Oneri: Yuksek enerji bagimliligi. Yenilenebilir enerjiye oncelik verin.\n"
                    "Almanya (~%2.63): GSYIH odakli. Oneri: Yesil buyume stratejilerini surdurun.\n"
                    "Rusya (~%2.63): Enerji odakli. Oneri: Fosil yakit bagimliligindan uzaklasin."))

pdf.chapter_title(tr("7. Nüfus Yoğunluğu ve Kişi Başına Düşen Emisyonlar"))
pdf.chapter_body(tr("Nufusa gore emisyon yogunlugunu anlamak icin kisi basi emisyonlari inceledim.\n"
                    "- ABD en yuksek kisi basi emisyona sahip ancak dusus egiliminde.\n"
                    "- Cin'in kisi basi emisyonlari onemli olcude artti ancak hala ABD'den dusuk."))
pdf.add_image("img/co2_per_capita_trend.png", tr("Kisi Basi CO2 Trendi"))

pdf.chapter_title(tr("8. Demografik Büyüme ve Emisyon İlişkisi"))
pdf.chapter_body(tr("Emisyonlarin nufustan daha hizli buyuyup buyumedigini gormek icin karsilastirma yaptim.\n\n"
                    "Cin: CO2 emisyonlari nufustan cok daha hizli artti.\n"
                    "ABD: Nufus artarken emisyonlar azaldi, bu da basarili bir ayrisma oldugunu gosteriyor."))
pdf.add_image("img/pop_vs_co2_China.png", tr("Cin: Nufus vs CO2"))
pdf.add_image("img/pop_vs_co2_United States.png", tr("ABD: Nufus vs CO2"))

pdf.chapter_title(tr("9. Nüfus Ölçeği ve Kişi Başına Emisyon Dinamikleri"))
pdf.chapter_body(tr("Grafik üzerindeki dağılım, nüfus büyüklüğü ile kişi başı emisyonlar arasında doğrudan bir ilişki olmadığını, ancak kalkınma modellerinin belirleyici olduğunu göstermektedir:\n"
                    "- Çin: Çok yüksek nüfusa sahip olmasına rağmen, kişi başı emisyonları orta seviyededir (Sanayileşme etkisi).\n"
                    "- ABD: Nüfusu Çin'e göre düşük olmasına rağmen, kişi başı emisyonları çok yüksektir (Yüksek tüketim ve enerji yoğunluğu).\n"
                    "- Türkiye: Düşük nüfus ve orta seviye kişi başı emisyon ile gelişmekte olan ülke profilini yansıtmaktadır."))
pdf.add_image("img/population_vs_per_capita.png", tr("Nufus vs Kisi Basi"))

pdf.chapter_title(tr("10. Demografik Projeksiyonlar (2025-2035)"))
pdf.chapter_body(tr("Gelecek on yil icin nufus buyumesini tahmin ettim.\n"
                    "- Cin: Zirve yapip dususe gecmesi bekleniyor.\n"
                    "- ABD ve Turkiye: Buyumeye devam etmesi bekleniyor.\n"
                    "- Rusya ve Almanya: Nispeten istikrarli kalmasi veya azalmasi bekleniyor."))
pdf.add_image("img/population_forecast.png", tr("Nufus Tahmini"))

pdf.chapter_title(tr("11. Nüfus Kaynaklı Emisyon Etki Analizi"))
pdf.chapter_body(tr("Sadece nufus buyumesinin CO2 uzerindeki etkisini modelledim.\n"
                    "- Bu projeksiyon, nufus ve CO2 arasindaki tarihsel iliskinin sabit kaldigini varsayar.\n"
                    "- Sapma: Bunu gercek CO2 tahminiyle karsilastirmak, ulkelerin emisyonlari nufus artisindan nerede basariyla ayirdigini gosterir."))
pdf.add_image("img/co2_impact_analysis.png", tr("CO2 Etki Analizi"))

pdf.chapter_title(tr("15. Sonuç ve Özet"))
pdf.chapter_body(tr("Küresel CO2 Geleceği: Mevcut trendler, acil müdahale edilmediği takdirde emisyonların artmaya devam edeceğini göstermektedir.\n\n"
                    "Ülke Bazlı Çıkarımlar:\n"
                    "- Çin ve Türkiye: Büyüme odaklı emisyon artışı devam etmektedir.\n"
                    "- ABD ve Almanya: Verimlilik ve politika değişiklikleri ile emisyonları düşürmeyi başarmışlardır.\n"
                    "- Rusya: Fosil yakıt bağımlılığı nedeniyle durağan bir seyir izlemektedir.\n\n"
                    "En Kritik Riskler: İklim değişikliğine bağlı aşırı hava olayları, kaynak kıtlığı ve halk sağlığı üzerindeki baskılar artmaktadır.\n\n"
                    "Etkili Politika Önerileri: Yenilenebilir enerjiye geçişin hızlandırılması, döngüsel ekonomi modellerinin benimsenmesi ve uluslararası işbirliğinin güçlendirilmesi gerekmektedir."))

pdf.output("CO2_Analiz_Raporu.pdf")
print("PDF olusturuldu: CO2_Analiz_Raporu.pdf")
