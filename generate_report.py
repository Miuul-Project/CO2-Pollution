from fpdf import FPDF
import os
import json
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, 'KURESEL CO2 EMISYON ANALIZI', 0, 1, 'C')
        self.set_font('Arial', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, 'Iklim Degisikligi Gostergeleri Uzerine Kapsamli Veri Bilimi Calismasi', 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Sayfa {self.page_no()} | CO2 Veri Analizi Raporu | 2024', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 13)
        self.set_text_color(0, 51, 102)
        self.set_fill_color(230, 240, 250)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(3)

    def section_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, body)
        self.ln(3)

    def add_image(self, image_path, title=""):
        if os.path.exists(image_path):
            self.image(image_path, w=165)
            self.ln(2)
            if title:
                self.set_font('Arial', 'I', 9)
                self.set_text_color(80, 80, 80)
                self.cell(0, 5, f'Sekil: {title}', 0, 1, 'C')
            self.ln(4)
        else:
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f"[Resim bulunamadi: {image_path}]", 0, 1)
            self.set_text_color(0, 0, 0)

    def add_table_row(self, col1, col2, header=False):
        if header:
            self.set_font('Arial', 'B', 10)
            self.set_fill_color(0, 51, 102)
            self.set_text_color(255, 255, 255)
        else:
            self.set_font('Arial', '', 10)
            self.set_fill_color(245, 245, 245)
            self.set_text_color(0, 0, 0)
        self.cell(60, 7, col1, 1, 0, 'L', 1)
        self.cell(110, 7, col2, 1, 1, 'L', 1)

def tr(text):
    mapping = {
        'ğ': 'g', 'Ğ': 'G', 'ş': 's', 'Ş': 'S',
        'ı': 'i', 'İ': 'I', 'ç': 'c', 'Ç': 'C',
        'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U'
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

pdf = PDF()
pdf.set_margins(20, 20, 20)
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=25)

# ============== KAPAK SAYFASI ==============
pdf.set_font('Arial', 'B', 28)
pdf.set_text_color(0, 51, 102)
pdf.ln(30)
pdf.cell(0, 15, 'MEZUNIYET PROJESI', 0, 1, 'C')
pdf.ln(5)
pdf.set_font('Arial', 'B', 22)
pdf.cell(0, 12, tr('Kuresel CO2 Emisyon Analizi'), 0, 1, 'C')
pdf.set_font('Arial', 'I', 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, tr('Iklim Degisikligi Uzerine Veri Odakli Icgoruler'), 0, 1, 'C')
pdf.ln(20)

pdf.set_draw_color(0, 51, 102)
pdf.set_line_width(1)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(20)

pdf.set_font('Arial', '', 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, tr('Kapsamli Calisma Konulari:'), 0, 1, 'C')
pdf.set_font('Arial', 'I', 11)
pdf.cell(0, 7, tr('- Tarihsel CO2 Emisyon Trendleri (1990-2024)'), 0, 1, 'C')
pdf.cell(0, 7, tr('- Ulke Bazli Karsilastirmali Analiz'), 0, 1, 'C')
pdf.cell(0, 7, tr('- Makine Ogrenimi Tabanli Tahminleme'), 0, 1, 'C')
pdf.cell(0, 7, tr('- Interaktif 3D Gorsellestirme'), 0, 1, 'C')
pdf.ln(30)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Rapor Tarihi: Aralik 2024', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('Arial', 'I', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, 'Teknolojiler: Python | Pandas | Scikit-learn | Plotly | Machine Learning', 0, 1, 'C')

# ============== GIRIS ==============
pdf.add_page()

pdf.chapter_title(tr("1. YONETICI OZETI"))
pdf.chapter_body(tr("Bu kapsamli arastirma raporu, dunya iklim sistemini etkileyen en kritik gostergelerden biri olan kuresel karbondioksit (CO2) emisyonlarinin derinlemesine analizini sunmaktadir. Calisma, otuz yili askin bir donem boyunca (1990-2024) tarihsel emisyon trendlerini incelemekte, buyuk ekonomiler genelindeki mevcut kaliplari analiz etmekte ve yakin gelecek (2025-2028) icin veriye dayali projeksiyonlar saglamaktadir.\n\n"
"Arastirma, tahmine dayali modelleme icin makine ogrenimi algoritmalari ve gelistirilmis veri kesfi icin interaktif 3D gorsellestirme teknikleri dahil olmak uzere ileri veri bilimi metodolojileri kullanmaktadir. Bu calismanin temel yeniliklerinden biri, zaman serisi analizinde bilgi sizintisini onleyen 'zaman guvenli' veri on isleme yontemlerinin uygulanmasidir.\n\n"
"Analiz, birlikte kuresel CO2 emisyonlarinin yaklasik %60'ini temsil eden alti buyuk ulkeyi - Cin, Amerika Birlesik Devletleri, Hindistan, Rusya, Almanya ve Turkiye - kapsamaktadir. Bu ulkeler, cesitli ekonomik kalkinma asamalarini, enerji tuketim kaliplarini ve iklim politikasi yaklasimlarini temsil etmek uzere secilmistir."))

pdf.chapter_title(tr("2. GIRIS VE ARASTIRMA HEDEFLERI"))
pdf.section_title(tr("2.1 Arka Plan ve Motivasyon"))
pdf.chapter_body(tr("Baskinn olarak insan kaynakli sera gazi emisyonlari tarafindan tetiklenen iklim degisikligi, 21. yuzyilin belirleyici sorunlarindan birini temsil etmektedir. Hukumetlerarasi Iklim Degisikligi Paneline (IPCC) gore, atmosferik CO2 konsantrasyonlari sanayi oncesi donemden bu yana %50'den fazla artarak yaklasik 280 ppm'den 2024'te 420 ppm'in uzerine cikmistir. Sera gazi konsantrasyonlarindaki bu benzeri gorulmemis artis, kuresel sicaklik artislari, asiri hava olaylari ve ekosistem bozulmalari ile dogrudan baglantilidir.\n\n"
"Fosil yakit yanmasindan kaynaklanan karbondioksit emisyonlari, toplam sera gazi emisyonlarinin yaklasik %75'ini olusturmaktadir. Bu emisyonlarin kaliplarini, suruclerini ve yonelimlerini anlamak, etkili azaltim stratejileri gelistirmek ve kuresel isinmayi sanayi oncesi seviyelerin 1.5-2 santigrat derece uzerinde sinirlamayi amaclayan Paris Anlasmasi gibi uluslararasi iklim anlasmalari hakkinda bilgi vermek icin zorunludur.\n\n"
"Bu arastirma projesi, mezuniyet tezi kapsaminda yurutulmus olup, modern veri bilimi tekniklerinin gercek dunya cevre sorunlarina uygulanmasini gostermektedir."))

pdf.section_title(tr("2.2 Arastirma Hedefleri"))
pdf.chapter_body(tr("Bu arastirmanin birincil hedefleri sunlardir:\n\n"
"1. Tarihsel Trend Analizi: 1990-2024 yillari arasindaki CO2 emisyon trendlerini incelemek ve olcumlemek, farkli bolgeler ve zaman dilimleri arasindaki temel donusu noktalari ve buyume kaliplarini belirlemek.\n\n"
"2. Surucu Belirleme: GSYIH buyumesi, nufus dinamikleri, enerji tuketim kaliplari ve endustriyel gelisim dahil olmak uzere emisyonlari yonlendiren temel sosyoekonomik faktorleri belirlemek ve analiz etmek.\n\n"
"3. Tahmine Dayali Modelleme: Guven araliklari ile nicel tahminler saglayan, gelecekteki emisyon yonelimlerini (2025-2028) tahmin etmek icin makine ogrenimi modelleri gelistirmek.\n\n"
"4. Karsilastirmali Analiz: Karbon yogunlugu, enerji karmasi ve ayristirma basarisi farkliliklarini vurgulayarak alti buyuk ekonomideki emisyon profillerini karsilastirmak.\n\n"
"5. Interaktif Gorsellestirme: Mekansal ve zamansal emisyon kaliplarinin dinamik kesedilmesini saglayan yenilikci 3D gorsellestirmeler olusturmak.\n\n"
"6. Politika Onerileri: Analiz edilen her ulke icin kanita dayali politika onerileri sentezlemek."))

pdf.chapter_title(tr("3. VERI HIKAYESI VE VERI SETI"))
pdf.section_title(tr("3.1 Veri Kaynagi ve Koekeni"))
pdf.chapter_body(tr("Bu analizde kullanilan birincil veri seti, Oxford Universitesi ile baglantili bilimsel bir cevrimici yayin olan 'Our World in Data' (OWID) platformundan alinmistir. OWID, veri setleri akademik yayinlarda, politika belgelerinde ve uluslararasi raporlarda duzenli olarak atifta bulunulan, kuresel kalkinma ve cevre verileri icin en kapsamli ve guvenilir kaynaklardan biri olarak genis capta taninmaktadir.\n\n"
"CO2 emisyonlari veri seti (owid-co2-data.csv) asagidakiler dahil birden fazla yetkili kaynaktan verileri bir araya getirmektedir:\n"
"- Kuresel Karbon Projesi: Bolgesel CO2 emisyonlari icin birincil kaynak\n"
"- Uluslararasi Enerji Ajansi (IEA): Enerji tuketimi ve yakita ozgu emisyonlar\n"
"- Dunya Bankasi: GSYIH ve nufus istatistikleri\n"
"- BP Istatistik Incelemesi: Tarihsel enerji verileri\n\n"
"Veri Ozellikleri:\n"
"- Zamansal Kapsam: 1750 - 2024 (Analiz 1990-2024'e odaklanmaktadir)\n"
"- Cografik Kapsam: 200+ ulke ve bolge\n"
"- Toplam Gozlem: Yaklasik 60.000+ veri noktasi\n"
"- Guncelleme Sikligi: Yillik"))

pdf.section_title(tr("3.2 Analizde Kullanilan Degiskenler"))
pdf.chapter_body(tr("Asagidaki tablo, bu calismada kullanilan temel kategorik ve sayisal degiskenleri sunmaktadir:"))
pdf.ln(2)

# Degiskenler Tablosu
pdf.add_table_row("Degisken", "Aciklama", header=True)
pdf.add_table_row("co2", "Toplam CO2 emisyonlari (Milyon ton/yil)")
pdf.add_table_row("country", tr("Ulke veya bolge adi (kategorik)"))
pdf.add_table_row("year", tr("Gozlem yili (1750-2024)"))
pdf.add_table_row("gdp", "Gayri Safi Yurtici Hasila (USD, PPP)")
pdf.add_table_row("population", tr("Toplam nufus"))
pdf.add_table_row("co2_per_capita", tr("Kisi basi CO2 emisyonu (ton/kisi)"))
pdf.add_table_row("co2_per_gdp", "Karbon yogunlugu (kg CO2 / $ GSYIH)")
pdf.add_table_row("energy_per_capita", tr("Kisi basi enerji tuketimi (kWh)"))
pdf.add_table_row("coal_co2", tr("Komur yanmasindan CO2"))
pdf.add_table_row("oil_co2", tr("Petrol yanmasindan CO2"))
pdf.add_table_row("gas_co2", tr("Dogalgaz yanmasindan CO2"))
pdf.add_table_row("consumption_co2", tr("Tuketim tabanli CO2 (ithalat dahil)"))
pdf.ln(5)

pdf.chapter_title("4. METODOLOJI")
pdf.section_title(tr("4.1 Veri On Isleme Hatti"))
pdf.chapter_body(tr("Veri kalitesini saglamak ve zaman serisi analizindeki yaygin tuzaklardan kacinmak icin titiz bir on isleme hatti uygulanmistir:\n\n"
"1. Eksik Deger Isleme: Bu calisma icin ozellikle yeni bir 'zaman guvenli' lineer interpolasyon yontemi gelistirilmis olup:\n"
"   - Egitim verisi (2000-2018): Sadece egitim donemi icinde cift yonlu interpolasyon kullanir\n"
"   - Test verisi (2019-2024): Sadece gecmis gozlemlerden ileri doldurma kullanir, asla gelecek bilgisine erisemez\n\n"
"2. Aykiri Deger Tespiti ve Isleme: Dordunculer Arasi Aralik (IQR) analizi ve Z-skor hesaplamalari dahil istatistiksel yontemler potansiyel aykiri degerleri belirlemek icin uygulanmistir.\n\n"
"3. Ozellik Muhendisligi: Analizi gelistirmek icin cesitli turetilmis ozellikler hesaplanmistir:\n"
"   - Yildan yila emisyon buyume oranlari\n"
"   - Karbon yogunlugu oranlari (birim GSYIH basina emisyon)\n"
"   - Nufusa normallenmis metrikler\n"
"   - Yakit karmasi yuzdeleri"))

pdf.section_title(tr("4.2 Makine Ogrenimi Yaklasimi"))
pdf.chapter_body(tr("Model Mimarisi:\n"
"- Algoritma: Yorumlanabilirlik ve sinirli egitim verisiyle saglan performans icin Cok Degiskenli Lineer Regresyon secilmistir\n"
"- Ozellik Seti: Yil, GSYIH, nufus, enerji tuketimi ve yakita ozgu emisyonlar\n"
"- Egitim Donemi: 2000-2018 (19 yillik veri)\n"
"- Dogrulama Donemi: 2019-2024 (test icin ayrilan 5 yil)\n"
"- Tahmin Ufku: 2025-2028 (gelecege donuk 4 yil)\n\n"
"Temel Metodolojik Yenilik - Zaman Guvenli Dogrulama:\n"
"Geleneksel capraz dogrulama yontemleri istemeden gelecek bilgisinin gecmis tahminlere sizmisina neden olabilir ve asiri iyimser performans tahminlerine yol acabilir. Zaman guvenli yaklasimimiz zamansal siralamayi kesinlikle korur:\n"
"1. Veri, herhangi bir on islemeden once kronolojik olarak bolunur\n"
"2. Imputation test verisi icin sadece cagdas veya gecmis bilgi kullanir\n"
"3. Model egitimi asla test donemi verisine erisemez"))

# Metrikleri yukle
try:
    with open("metrics_timesafe.json", "r") as f:
        metrics = json.load(f)
    
    pdf.section_title("4.3 Model Performans Metrikleri")
    pdf.chapter_body(tr(f"Model, tutulan test seti (2019-2024) uzerinde standart regresyon metrikleri kullanilarak titizlikle degerlendirilmistir:\n\n"
                        f"- Kok Ortalama Kare Hatasi (RMSE): {metrics['rmse']:.4f}\n"
                        f"  Yorum: Ortalama olarak tahminler gercek degerlerden yaklasik {metrics['rmse']:.2f} milyon ton sapar\n\n"
                        f"- Ortalama Mutlak Hata (MAE): {metrics['mae']:.4f}\n"
                        f"  Yorum: Ortalama mutlak tahmin hatasi {metrics['mae']:.2f} milyon tondur\n\n"
                        f"- R-Kare (R2): {metrics['r2']:.4f}\n"
                        f"  Yorum: Model CO2 emisyonlarindaki varyansin yaklasik %{metrics['r2']*100:.1f}'ini aciklamaktadir\n\n"
                        "Zaman guvenli dogrulama yoluyla elde edilen bu metrikler, gelecek veriler uzerindeki model performansinin gercekci tahminlerini saglar."))
except FileNotFoundError:
    pass

pdf.section_title("4.4 Teknolojiler ve Araclar")
pdf.chapter_body(tr("Asagidaki teknoloji yigini kullanilmistir:\n\n"
"- Python 3.x: Birincil programlama dili, zengin veri bilimi kutuphane ekosistemi icin secilmistir\n"
"- Pandas: Yuksek performansli veri manipulasyonu ve analizi\n"
"- NumPy: Sayisal hesaplamalar ve dizi islemleri\n"
"- Scikit-learn: Makine ogrenimi model gelistirme ve degerlendirme\n"
"- Matplotlib & Seaborn: Yayin kalitesinde statik gorsellestirmeler\n"
"- Plotly: Animasyon yetenekleri ile interaktif 3D dunya gorsellestirmesi\n"
"- FPDF: Otomatik PDF rapor olusturma"))

# ============== ANALIZ BOLUMLERI ==============
pdf.add_page()
pdf.chapter_title("5. TARIHSEL TREND ANALIZI")
pdf.section_title(tr("5.1 Zamana Gore Kuresel CO2 Emisyonlari"))
pdf.chapter_body(tr("Son otuz yildaki kuresel CO2 emisyonlarinin analizi, buyuk ekonomik olaylar sirasinda kisa kesintilerle noktali tutarli bir yukselis yonelimi ortaya koymaktadir. Kuresel emisyonlar 1990'da yaklasik 22 milyar tondan 2023'te 37 milyar tonun uzerine cikmis olup %68'lik bir artisi temsil etmektedir.\n\n"
"Tarihsel trendden temel gozlemler:\n\n"
"1. Istikrarli Buyume (1990-2000): Baskinlikcla gelismekte olan ekonomilerdeki sanayilesme tarafindan yonlendirilen yillik yaklasik %1.5 buyume oranlari.\n\n"
"2. Hizlanan Buyume (2000-2010): En hizli buyume on yili, Cin'in hizli sanayilesmesi kuresel emisyonlari yilda yaklaski %3 yukari itmistir.\n\n"
"3. Plato Girisimleri (2014-2016): Cin'in ekonomik yeniden dengelenmesi ve gelismis ulkelerdeki yenilenebilir enerji genislemesine atfedilen kisa sureli stabilizasyon.\n\n"
"4. COVID-19 Etkisi (2020): Kuresel kilitlenmeler nedeniyle benzeri gorulmemis %5.4 dusus, kayitli tarihteki en buyuk tek yillik azalma.\n\n"
"5. Pandemi Sonrasi Toparlanma (2021-2024): Emisyonlar hizla toparlanmis ve pandemi oncesi seviyeleri asmistir, bu da kalici azalmalar icin enerji sisteminde yapisal degisikliklerin gerekli oldugunu gostermektedir."))
pdf.add_image("img/global_co2_trend.png", tr("Kuresel Ortalama CO2 Emisyon Trendi (1990-2024)"))

pdf.section_title(tr("5.2 Ulkeye Ozgu Emisyon Profilleri"))
pdf.chapter_body(tr("Secilen alti ulkenin karsilastirmali analizi, farkli ekonomik kalkinma yollarini, enerji politikalarini ve demografik trendleri yansitan dramatik olarak farkli emisyon yonelimleri ortaya koymaktadir:\n\n"
"CIN:\n"
"Cin, dunyanin en buyuk CO2 yaycisi olarak ortaya cikmis olup, su anda kuresel emisyonlarin yaklasik %30'undan sorumludur. Temel ozellikler sunlardir:\n"
"- 1990-2024 arasinda emisyonlar yaklaski %400 artmistir\n"
"- Komur baskin enerji kaynagi olmaya devam etmektedir (birincil enerjinin >%60'i)\n"
"- Son yillar yenilenebilir kapasite hizla genislerken plato isaretleri gostermektedir\n"
"- Kisi basi emisyonlar artik AB ortalamasini asmistir ancak ABD seviyelerinin altinda kalmaktadir\n\n"
"AMERIKA BIRLESIK DEVLETLERI:\n"
"Tarihsel olarak en buyuk yayci olan ABD artik kuresel olarak ikinci siradadir:\n"
"- Zirve emisyonlar 2007'de meydana gelmis, ardindan yaklasik %15 dusus yasanmistir\n"
"- Emisyonlarin GSYIH buyumesinden basarili ayristirmasi gosterilmistir\n"
"- Dogalgazin komuru degistirmesi onemli azalmalari yonlendirmistir\n"
"- Buyuk ekonomiler arasinda en yuksek kisi basi emisyonlar (yaklasik 15 ton/kisi)\n\n"
"HINDISTAN:\n"
"Hizla gelisen bir ekonomi olarak Hindistan guclu emisyon buyumesi gostermektedir:\n"
"- 1990'dan bu yana emisyonlar uc katina cikmistir\n"
"- Artik kuresel olarak ucuncu en buyuk yaycidir\n"
"- Kisi basi emisyonlar cok dusuk kalmaktadir (yaklasik 1.9 ton/kisi)\n"
"- Onemli gunes yatirimina ragmen komur genislemesi devam etmektedir\n\n"
"RUSYA:\n"
"Rusya'nin emisyonlari benzersiz Sovyet sonrasi dinamikler gostermektedir:\n"
"- Ekonomik cokusun ardindan 1990'larda keskin dusus\n"
"- 2000'den bu yana kademeli toparlanma, su anda 1990 seviyelerinin yaklasik %15 altinda\n"
"- Yerli enerji icin dogalgaza agir bagimlilik\n"
"- Onemli fosil yakit ihracatcisi\n\n"
"ALMANYA:\n"
"Almanya emisyon azaltmada bir Avrupa basari hikayesini temsil etmektedir:\n"
"- 1990 seviyelerinden yaklasik %40 dusus\n"
"- Hirsli 'Energiewende' (Enerji Donusumu) politikasi degisimi yonlendirmektedir\n"
"- Enerji guvenligini korurken komuru asamali olarak kaldrma zorluklari devam etmektedir\n\n"
"TURKIYE:\n"
"Turkiye gelismekte olan bir ekonominin ozelliklerini gostermektedir:\n"
"- 1990'dan bu yana emisyonlar yaklasik %150 artmistir\n"
"- Buyuyen ekonomi artan enerji talebini yonlendirmektedir\n"
"- Onemli komur ve dogalgaz tuketimi\n"
"- Yerli yenilenebilir enerji kapasitesi gelistirilmektedir"))
pdf.add_image("img/country_co2_trend.png", tr("Ulkeye Gore CO2 Emisyonlari (1990-2024)"))

# ============== 3D GORSELLESTIRME - BURAYA TASINDI ==============
pdf.add_page()
pdf.chapter_title("6. INTERAKTIF 3D GORSELLESTIRME")
pdf.chapter_body(tr("Bu arastirma projesinin temel yeniliklerinden biri, kullanicilarin CO2 emisyon verilerini dinamik olarak kesfetmelerini saglayan interaktif 3D dunya gorsellestirmesinin gelistirilmesidir. Bu gorsellestirme, iklim verilerini sunmak icin statik grafiklerin otesine gecen ve surukleyici mekansal analize olanak taniyan yenilikci bir yaklasimi temsil etmektedir.\n\n"
"Gorsellestirme, soyut emisyon istatistiklerini asagidakileri kolaylastiran sezgisel, ilgi cekici bir formata donusturmektedir:\n"
"- Ulkeler arasindaki emisyon seviyelerini bir bakista karsilastirma\n"
"- Animasyonlu oynatma yoluyla zamansal degisiklikleri gozlemleme\n"
"- Verilerdeki kaliplari ve aykiriliklari belirleme\n"
"- Bulgulari teknik olmayan kitlelere etkili bir sekilde iletme\n\n"
"TEMEL GORSELLESTIRME OZELLIKLERI:\n\n"
"1. 3D Donen Dunya: Gercekci bir mekansal baglam saglayan ortografik dunya projeksiyonu. Dunya, profesyonel sunumlar icin uygun, kontrast optimizasyonlu bir tema ile ulke sinirlarini ve cografi ozellikleri gostermektedir.\n\n"
"2. Dinamik Isaretleyiciler: Analiz edilen her ulke, cografi merkezine konumlandirilmis dairesel bir isaretleyici ile temsil edilmektedir. Isaretleyici ozellikleri cok boyutlu emisyon verilerini kodlamaktadir:\n"
"   - Boyut: Toplam CO2 emisyonlari ile orantili (daha buyuk isaretleyiciler daha yuksek emisyonlari gosterir)\n"
"   - Renk: Yesilden (dusuk etki) kirmiziya (kritik etki) degisen gradyan skalasi\n"
"   - Siddet Gostergeleri: Kirlilik yogunluk seviyelerini belirten gorsel ipuclari\n\n"
"3. Zamansal Evrim: Gorsellestirme, izleyicilerin 2000'den 2024'e kadar emisyonlarin evrimine tanik olmalarini saglayan zamansal bir boyut icermektedir. Bu animasyonlu gorunum, zaman icinde kuresel emisyonlarin degisen merkezini ortaya koymaktadir.\n\n"
"4. Veri Zengini Etkilesim: Sistem, talep uzerine asagidakiler dahil olmak uzere ayrintili analitik veriler saglamaktadir:\n"
"   - Yillik toplam CO2 emisyonlari\n"
"   - Kuresel katki yuzdeleri\n"
"   - Kisi basi emisyon metrikleri\n"
"   - Demografik baglam\n\n"
"Bu interaktif arac, karmasik istatistiksel veriler ile kamuoyu anlayisi arasinda bir kopru gorevi gorerek iklim trendleri hakkinda daha bilincli tartismalari kolaylastirmaktadir."))

# 2024 statik dunya gorseli ekle
pdf.add_image("img/3d_globe_2024_static.png", tr("3D Dunya: CO2 Emisyonlari 2024 - Gorsellestirme Anlik Goruntusu"))

pdf.chapter_title("7. ISTATISTIKSEL KORELASYON ANALIZI")
pdf.chapter_body(tr("CO2 emisyonlarinin temel suruclerini belirlemek icin 1990 sonrasi veriler uzerinde kapsamli bir korelasyon analizi yurutlmustur. Korelasyon matrisi, emisyonlar ve cesitli sosyoekonomik gostergeler arasindaki iliskilerin gucunu ve yonunu ortaya koymaktadir.\n\n"
"Temel Bulgular:\n\n"
"1. GSYIH-Emisyon Iliskisi (r = 0.95+): Kuresel duzeyde ekonomik cikti ve CO2 emisyonlari arasinda cok guclu pozitif korelasyon mevcuttur. Ancak bu iliski ulke kalkinma asamasina gore onemli olcude degismektedir.\n\n"
"2. Nufus-Emisyon Korelasyonu (r = 0.85+): Nufus buyuklugu toplam emisyonlarla guclu sekilde iliskilidir, ancak kisi basi metrikler ulkeler arasinda genis varyasyon gostermektedir.\n\n"
"3. Enerji-Emisyon Baglantisi (r = 0.90+): Birincil enerji tuketimi belki de emisyonlarin en guclu ongornucusudur, iklim azaltiminda enerji sistemlerinin merkezi rolunu vurgulamaktadir.\n\n"
"4. Ayristirma Kanitlari: Gelismis ekonomiler (ABD, Almanya) son yillarda azalan korelasyon gucu gostermekte olup, ekonomik buyumenin emisyon buyumesinden basarili kismi ayristirmasini isaret etmektedir."))
pdf.add_image("img/correlation_matrix.png", tr("Temel Degiskenlerin Korelasyon Matrisi"))

pdf.add_page()
pdf.chapter_title("8. TAHMINE DAYALI MODELLEME VE PROJEKSIYONLAR")
pdf.section_title(tr("8.1 Kuresel Emisyon Tahmini (2025-2028)"))
pdf.chapter_body(tr("Cok degiskenli regresyon modelleme ve trend analizine dayanarak, buyuk politika mudahaleleri veya teknolojik atilimlar olmaksizin kuresel CO2 emisyonlarinin 2028'e kadar kademeli artisini surdurmesi ongurulmektedir.\n\n"
"Tahmin Metodolojisi:\n"
"Tahmin, surucu degiskenler (GSYIH, nufus, enerji) icin polinom trend ekstrapolasyonunu gelecek emisyonlari tahmin etmek icin egitilmis regresyon modeli ile birlestirir. Guven aralikleri tarihsel tahmin hatalarina dayanarak hesaplanmistir.\n\n"
"Temel Projeksiyonlar:\n"
"- 2025: 2024 seviyelerinin uzerinde ilimli %1-2 artis\n"
"- 2026-2028: Devam eden kademeli buyume, mevcut yenilenebilir enerji genislemesi devam ederse plato potansiyeli\n"
"- Kumulatif 2025-2028: Yaklasik 145-155 milyar ton ilave CO2"))
pdf.add_image("img/global_forecast_multivariate.png", tr("Kuresel CO2 Emisyon Tahmini (2025-2028)"))

pdf.section_title(tr("8.2 Ulke Duzeyinde Projeksiyonlar"))
pdf.chapter_body(tr("Bireysel ulke tahminleri farkli yonelimleri ortaya koymaktadir:\n\n"
"- Cin: Yenilenebilir kapasite komuru dengeledikce potansiyel zirve ve baslangic dususu ongurulmektedir\n"
"- Hindistan: Kalkinma ilerledikce devam eden buyume beklenmekte, ancak buyume orani yavaslayanilir\n"
"- ABD: Devam eden komurden gaza ve yenilenebilire gecislerle kademeli dusus ongurulmektedir\n"
"- Almanya: Komurden cikisla guclu dusus yoneliminin hizlanmasi beklenmektedir\n"
"- Rusya: Ilimli varyasyonla nispeten istikrarli emisyonlar ongurulmektedir\n"
"- Turkiye: Yenilenebilir yatirim hizlanirsa daha hizli azalma potansiyeli ile ilimli buyume ongurulmektedir"))
pdf.add_image("img/country_forecasts_multivariate.png", tr("Ulkeye Ozgu Emisyon Tahminleri"))

pdf.chapter_title(tr("9. KISI BASI EMISYON ANALIZI"))
pdf.chapter_body(tr("Kisi basi emisyonlarin incelenmesi, bireysel sorumluluk ve kalkinma adaleti konusunda onemli perspektif saglamaktadir:\n\n"
"Mevcut Kisi Basi Emisyonlar (2024 tahminleri):\n"
"- Amerika Birlesik Devletleri: ~15 ton CO2/kisi (buyuk ekonomiler arasinda en yuksek)\n"
"- Rusya: ~12 ton CO2/kisi\n"
"- Almanya: ~8 ton CO2/kisi (dususte)\n"
"- Cin: ~8 ton CO2/kisi (artik AB ortalamasini asiyor)\n"
"- Turkiye: ~5 ton CO2/kisi\n"
"- Hindistan: ~2 ton CO2/kisi (en dusuk, kalkinma asamasini yansitmaktadir)\n\n"
"Politika Etkileri:\n"
"Kisi basi emisyonlardaki genis esitsizlik, iklim azaltiminda adil yuk paylasimu hakkinda onemli sorular ortaya koymaktadir."))
pdf.add_image("img/co2_per_capita_trend.png", tr("Ulkeye Gore Kisi Basi CO2 Emisyonlari"))

pdf.chapter_title("10. DEMOGRAFIK DINAMIKLER VE EMISYONLAR")
pdf.chapter_body(tr("Nufus buyumesi ve emisyonlar arasindaki iliski, farkli kalkinma modellerini ve politika secimlerini yansitarak ulkeler arasinda dramatik olarak degismektedir:"))
pdf.add_image("img/pop_vs_co2_China.png", tr("Cin: Nufus vs CO2 Buyume Endeksi (2004=100)"))
pdf.add_image("img/pop_vs_co2_United States.png", tr("ABD: Nufus vs CO2 Buyume Endeksi (2004=100)"))

pdf.add_page()
pdf.chapter_title("11. ENERJI KARMASIMI VE KARBON YOGUNLUGU")
pdf.section_title(tr("11.1 Fosil Yakit Bagimliligi Analizi"))
pdf.chapter_body(tr("Fosil yakit tuketiminin bilesimi, azaltim stratejilerini bilgilendiren farkli enerji profillerini ortaya koymaktadir:\n\n"
"Komur-Baskin Ulkeler (Cin, Hindistan):\n"
"Komur en buyuk emisyon kaynagini temsil etmektedir (fosil CO2'nin %60-70'i). Komur endustriyel sureclere ve enerji uretimine derinden gomulu oldugu icin bu ulkeler karbonsuzlasmada en buyuk zorlukla karsi karsiydir. Ancak her ikisi de hizli yenilenebilir konuslandirma gormektedir.\n\n"
"Petrol-Baskin Ulkeler (ABD):\n"
"Ulasim sektoru petrol tuketimi birincil zorluktur. Elektrikli arac benimsemesi ve verimlilik standartlari temel kaldiraclardır.\n\n"
"Gaz-Baskin Ulkeler (Rusya):\n"
"Dogalgaz, komurden daha temiz olmakla birlikte yine de onemli emisyonlar uretmektedir. Rusya'nin ekonomisi gaz ihracatina agir olarak bagimlidir, karmasik tesvik yapilari olusturmaktadir.\n\n"
"Karma Profiller (Almanya, Turkiye):\n"
"Bu ulkeler her uc fosil yakisi da onemli miktarlarda kullanmakta olup, enerji uretimi, sanayi, ulasim ve isitmayi ele alan kapsamli stratejiler gerektirmektedir."))
pdf.add_image("img/fossil_fuel_mix.png", tr("Ulkeye Gore Fosil Yakit Emisyon Bilesimi"))

pdf.section_title(tr("11.2 Karbon Yogunlugu Trendleri"))
pdf.chapter_body(tr("Karbon yogunlugu (birim GSYIH basina CO2 emisyonlari) ekonomik faaliyetin 'yesiligini' olcer. Azalan yogunluk ekonomik buyumenin emisyonlardan basarili ayristirmasini gosterir:\n\n"
"Kayda Deger Trendler:\n"
"- Kuresel karbon yogunlugu 1990'dan bu yana yaklasik %35 azalmistir\n"
"- Cin en hizli iyilesme oranini gostermekte olup, yogunluk buyuk emisyon buyumesine ragmen %60'in uzerinde dusmestur\n"
"- Gelismis ekonomiler dusuk, istikrarli yogunluk seviyelerini korumaktadir\n"
"- Enerji verimliligi ve temiz enerji konuslandirmasi yoluyla daha fazla yogunluk iyilestirmeleri mumkun ve gereklidir"))
pdf.add_image("img/carbon_intensity_trend.png", tr("Karbon Yogunlugu (CO2/GSYIH) Trend Analizi"))

pdf.chapter_title(tr("12. POLITIKA ONERILERI"))
pdf.chapter_body(tr("Bu raporda sunulan kapsamli analize dayanarak, analiz edilen her ulke icin asagidaki kanita dayali politika onerileri onerilerdir:\n\n"
"CIN:\n"
"- Enerji guvenligini saglarken komur enerji santrali asamali kaldirmayi hizlandirin\n"
"- Buyuk yenilenebilir enerji konuslandirmasini surdurun (gunes, ruzgar)\n"
"- Elektrikli arac benimsemesini ve sarj altyapisini genisletin\n"
"- Karbon pazari mekanizmalarini ve fiyatlandirmayi guclendirin\n\n"
"HINDISTAN:\n"
"- Komur genislemesi yerine yenilenebilir enerjiye siçramayi onceliklendirin\n"
"- Agresif gunes ve ruzgar hedefleri uygulayin\n"
"- Biyokutle yakmayi azaltmak icin temiz pisirme cozumleri gelistirin\n"
"- Yenilenebilir entegrasyonu icin sebeke altyapisina yatirim yapin\n\n"
"AMERIKA BIRLESIK DEVLETLERI:\n"
"- Federal iklim politikasini ve emisyon standartlarini guclendirin\n"
"- Komur enerji santrali emekliliklerini hizlandirin\n"
"- Elektrikli arac tesviklerini ve altyapisini genisletin\n"
"- Azaltilmasi zor sektorler icin karbon yakalama teknolojisine yatirim yapin\n\n"
"ALMANYA:\n"
"- 2030'a kadar komurden cikisi tamamlayin\n"
"- Yenilenebilir enerji kapasitesini ve sebeke ara baglantilarini genisletin\n"
"- Endustriyel uygulamalar icin yesil hidrojen gelistirin\n"
"- AB iklim politikasinda liderllgi surdurun\n\n"
"RUSYA:\n"
"- Ekonomiyi fosil yakit ihracat bagimliligindan cesitlendirin\n"
"- Yerli enerji verimlilligini iyilestirin (onemli potansiyel)\n"
"- Petrol ve gaz operasyonlarindan metan emisyonlarini azaltin\n"
"- Uygun bolgelerde yenilenebilir kaynaklari gelistirin\n\n"
"TURKIYE:\n"
"- Yerli yenilenebilir enerji gelismesini hizlandirin (mukemmel gunes/ruzgar potansiyeli)\n"
"- Enerji guvenligi icin ithal fosil yakitlara bagimliligi azaltin\n"
"- Karbon fiyatlandirma mekanizmalari uygulayin\n"
"- Bina enerji verimliligi standartlarini iyilestirin"))

pdf.chapter_title(tr("13. SONUCLAR"))
pdf.chapter_body(tr("Bu kapsamli analiz birkac temel sonuc vermektedir:\n\n"
"1. Emisyonlar Artmaya Devam Ediyor: Artan farkindaliik ve politika cabalarina ragmen, kuresel CO2 emisyonlari artmaya devam etmekte olup, baskinllikla gelismekte olan ekonomiler tarafindan yonlendirilmektedir.\n\n"
"2. Farkli Ulusal Yonelimler: Veriler, emisyonlari basariyla azaltan gelismis ekonomiler (ABD, Almanya) ile hala buyume yasayan gelismekte olan ekonomiler (Cin, Hindistan, Turkiye) arasinda net bir bolunme ortaya koymaktadir.\n\n"
"3. Ayristirma Mumkundur: Birkac ulke, yesil buyume stratejileri icin kanitsal konsept saglayarak emisyonlar duserken ekonomik buyumenin devam edebilecegini gostermektedir.\n\n"
"4. Enerji Sistemi Donusumu Merkezidir: Analiz, ozellikle komur olmak uzere fosil yakit yanmasinin baskin emisyon kaynagi oldugunu dogrulamaktadir.\n\n"
"5. Tahmine Dayali Modeller Planlama Degeri Saglar: Tahminler belirsizlik tasimasina ragmen, zaman guvenli modelleme yaklasimlari politika planlamasi icin yararli rehberlik saglayabilir.\n\n"
"6. Gorsellestirme Anlayisi Artirir: Interaktif 3D gorsellestirmeler karmasik emisyon verilerini daha genis kitlelere eriselebilir kilmaktadir.\n\n"
"Iklim eylemi aciliyeti bu analiz boyunca vurgulanmaktadir. Temiz enerji konuslandirmasini hizlandirmak, verimliligi iyilestirmek ve fosil yakitlari asamali olarak kaldirmak icin koordineli kuresel cabalar olmaksizin, emisyon trendleri iklim degisikligi etkilerini agrrlastirmaya devam edecektir."))

pdf.chapter_title("14. KAYNAKLAR VE VERI KAYNAKLARI")
pdf.chapter_body("1. Our World in Data - CO2 ve Sera Gazi Emisyonlari Veri Seti\n"
"   Ritchie, H., Roser, M., & Rosado, P. (2024)\n"
"   https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions\n\n"
"2. Kuresel Karbon Projesi - Yillik Karbon Butcesi Raporlari\n"
"   Friedlingstein ve ark. (2023)\n"
"   https://www.globalcarbonproject.org/\n\n"
"3. IPCC Altinci Degerlendirme Raporu (AR6)\n"
"   Hukumetlerarasi Iklim Degisikligi Paneli (2021-2023)\n\n"
"4. Uluslararasi Enerji Ajansi - Dunya Enerji Gorunumu\n"
"   IEA (2024)\n\n"
"5. Dunya Bankasi Kalkinma Gostergeleri Veritabani\n"
"   https://data.worldbank.org/")

pdf.output("CO2_Analiz_Raporu.pdf")
print("PDF olusturuldu: CO2_Analiz_Raporu.pdf")
