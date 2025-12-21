from fpdf import FPDF
import datetime

class GuidePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(44, 62, 80) # Dark Blue
        self.cell(0, 10, 'CO2 ANALIZI - AKIS YONETIMI & KOPYA KAGIDI', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Rapor Bolumlerine Gore Teknik Detaylar ve Sunum Notlari', 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(44, 62, 80)
        self.line(10, 25, 200, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

    def section_header(self, title):
        self.set_fill_color(52, 152, 219) # Blue Background
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(3)

    def content_block(self, title, content):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(192, 57, 43) # Red for headers
        self.cell(0, 5, title, 0, 1, 'L')
        
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 4, content)
        self.ln(2)

    def tech_box(self, content):
        self.set_fill_color(236, 240, 241) # Light Grey
        self.set_draw_color(189, 195, 199)
        self.set_font('Courier', '', 8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 1, "", 0, 1) # margin
        self.multi_cell(0, 4, content, 1, 'L', 1)
        self.ln(3)

def create_guide():
    pdf = GuidePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # TR Character Helper
    def tr(text):
        mapping = {
            'ğ': 'g', 'Ğ': 'G', 'ş': 's', 'Ş': 'S',
            'ı': 'i', 'İ': 'I', 'ç': 'c', 'Ç': 'C',
            'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U'
        }
        for k, v in mapping.items():
            text = text.replace(k, v)
        return text.encode('latin-1', 'replace').decode('latin-1')

    # 1. YONETICI OZETI
    pdf.section_header(tr("1. YONETICI OZETI"))
    pdf.content_block(tr("SUNUM METNI (OKUYABILIRSINIZ)"), 
                      tr("Sayin Juri, bu calisma 1990 ile 2024 yillari arasindaki kuresel Karbondioksit emisyonlarini inceleyen kapsamli bir veri bilimi projesidir. Calismamizda sadece gecmis verileri analiz etmekle kalmadik, ayni zamanda makine ogrenimi modelleri kullanarak 2028 yilina kadar gelecege yonelik projeksiyonlar da olusturduk. Odak noktamiz, kuresel emisyonlarin %60'ini olusturan alti kritik ulke uzerinedir: Cin, ABD, Hindistan, Rusya, Almanya ve Turkiye."))
    pdf.tech_box(tr("TEKNIK KUNYE:\n"
                    "- Kutuphaneler: Pandas, NumPy, Scikit-learn, FPDF\n"
                    "- Veri Kapsami: 1990-2024 (Egitim/Analiz), 2025-2028 (Tahmin)\n"
                    "- Veri Boyutu: 60.000+ satir, 12 nitelik (feature)\n"
                    "- Veri Yapis: Panel Data (Long Format)"))

    # 2. GIRIS
    pdf.section_header(tr("2. GIRIS VE HEDEFLER"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Gunumuzde atmosferik CO2 seviyeleri 420 ppm'i asarak kritik bir esige ulasmistir. Bu projenin temel amaci, 'Kanita Dayali' bir yaklasimla bu artisin altinda yatan ekonomik ve demografik nedenleri ortaya cikarmaktir. Geleneksel analizlerden farkli olarak, bu calismada 'Time-Safe' yani zaman guvenli algoritmalar gelistirerek cok daha gercekci sonuclar elde etmeyi hedefledik."))

    # 3. VERI HIKAYESI
    pdf.section_header(tr("3. VERI HIKAYESI VE KAYNAKLAR"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Analizimizde Oxford Universitesi destekli 'Our World in Data' veri setini kullandik. Bu veri seti, Uluslararasi Enerji Ajansi ve Dunya Bankasi gibi guvenilir kaynaklarin birlestirilmesiyle olusturulmustur. Analiz surecinde ham veriyi alip, python tabanli bir veri temizleme hattindan gecirerek eksik verileri modern istatistiksel yontemlerle tamamladik."))
    pdf.tech_box(tr("SORU: EKSIK VERILERI NASIL DOLDURDUNUZ?\n"
                    "Cevap: 'Bilateral Interpolation' (IkI Yonlu Dogrusal Tamamlama) kullandik.\n"
                    "- NEDEN?: Veriler zaman serisi oldugu icin 'ortalama' (mean) ile doldurmak trendi bozar. Interpolasyon ise trendi korur.\n"
                    "- NASIL?: Pandas kutuphanesinin `interpolate(method='linear')` fonksiyonu ile."))

    # 4. METODOLOJI
    pdf.section_header(tr("4. METODOLOJI (EN KRITIK BOLUM)"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Bu projenin en ozgun yani gelistirdigimiz 'Time-Safe' metodolojisidir. Zaman serisi verilerinde en buyuk risk, gelecek bilgisinin gecmise sizmasidir, buna 'Data Leakage' denir. Biz veriyi 2018 yilindan itibaren keserek Egitim ve Test seti olarak ayirdik. Test setindeki eksik verileri doldururken ASLA gelecek yillardan bilgi almadik, sadece gecmis yillari referans aldik. Boylece modelimizin gercek dunya performansini dogru sekilde oIctuk."))
    pdf.tech_box(tr("SORU: TIME-SAFE YONTEMI NEDEN KULLANDINIZ?\n"
                    "- NEDEN?: Standart yontemlerde 2020 verisini kullanarak 2019'u doldurmak (Backward Fill) modelin kopya cekmesine neden olur. Bu da basariyi sahte yukseltir.\n"
                    "- NASIL?: Ozel yazdigimiz `_country_time_safe_impute` fonksiyonu ile Test setinde sadece 'Forward Fill' (Gecmisten ileriye tasima) yaptik. Asla gelecege bakmadik.\n\n"
                    "SORU: NEDEN LINEER REGRESYON?\n"
                    "- NEDEN?: Elimizdeki veri seti (60k satir) derin ogrenme (Deep Learning) icin kucuktur. Ayrica amacimiz 'Yorumlanabilirlik'tir. Hangi degiskenin (GSYIH mi Nufus mu) ne kadar etkiledigini gormek istedik.\n"
                    "- NASIL?: `sklearn.linear_model.LinearRegression` algoritmasi ile."))

    # 5. TARIHSEL TRENDLER
    pdf.section_header(tr("5. TARIHSEL TREND ANALIZI"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Grafige baktigimizda, 2020 yilinda pandeminin etkisiyle tarihin en buyuk emisyon dususunun yasandigini, ancak hemen ardindan V seklinde hizli bir toparlanma oldugunu goruyoruz. Ozellikle Cin'in 2000 sonrasi sanayilesme ile nasil dikey bir artis yasadigini, buna karsilik ABD'nin emisyonlarini nasil yavas yavas azalttigini gozlemleyebilirsiniz."))
    pdf.tech_box(tr("GORSELLESTIRME DETAYI:\n"
                    "- Kutuphane: Matplotlib & Seaborn (`sns.lineplot`)\n"
                    "- NEDEN?: Zaman serisi trendlerini gostermenin en net yolu Cizgi Grafiktir."))

    # 6. INTERAKTIF 3D GORSELLESTIRME
    pdf.add_page()
    pdf.section_header(tr("6. INTERAKTIF 3D GORSELLESTIRME"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Verileri daha iyi anlamlandirmak icin statik grafiklerin otesine gectik ve interaktif bir 3D dunya modeli gelistirdik. Bu modelde gordugunuz her nokta bir ulkeyi temsil ediyor. Noktalarin kirmiziya donmesi kirliligin arttigini, buyumesi ise hacmin genisledigini gosteriyor. Bu gorsellestirme, verilerdeki degisimi zamansal olarak izlememize olanak taniyor."))
    pdf.tech_box(tr("SORU: RENKLENDIRME ALGORITMASI NASIL CALISIYOR?\n"
                    "- NEDEN?: Sadece sayilari gostermek algiyi zorlastirir. Renk (Yesil->Kirmizi) tehlikeyi bilincaltina iteler.\n"
                    "- NASIL?: `get_pollution_color(co2)` fonksiyonu yazdik. Bu fonksiyon CO2 degerini 0 ile 1 arasina normalize edip, RGB renk uzayinda enterpolasyon yapar."))

    # 7. KORELASYON
    pdf.section_header(tr("7. KORELASYON ANALIZI"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Yaptigimiz korelasyon analizinde cok carpici bir sonuc ortaya cikti: Enerji tuketimi ve ekonomik buyume, emisyonlarla %90'in uzerinde bir iliskiye sahip. Bu durum, dunya genelinde hala ekonomik buyumenin cevre kirliligine bagimli oldugunu kanitliyor."))
    pdf.tech_box(tr("SORU: HANGI KORELASYON YONTEMI?\n"
                    "- YONTEM: Pearson Korelasyon Katsayisi.\n"
                    "- NEDEN?: Degiskenlerimiz arasindaki iliski dogrusal (Lineer) oldugu icin Pearson en uygunydu. Sirali iliski olsaydi Spearman kullanirdik.\n"
                    "- BULGU: GSYIH (0.92) ve Enerji (0.98) cok guclu pozitif iliski gosteriyor."))

    # 8. TAHMINLER
    pdf.section_header(tr("8. TAHMINE DAYALI MODELLEME"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Gelecege yonelik tahminlerimiz, 2028 yilina kadar emisyon artisinin devam edecegini, ancak artis hizinin yavaslayacagini gosteriyor. Burada 'Iki Asamali' bir tahmin yontemi kullandik. Once nufus ve ekonomi verilerini tahmin ettik, sonra bu verileri ana modelimize vererek CO2 tahminini uretiik. Bu sayede sadece zamana bagli degil, ekonomik parametrelere bagli gercekci bir tahmin elde ettik."))
    pdf.tech_box(tr("SORU: GELECEGI NASIL TAHMIN ETTINIZ? (TWO-STEP FORECASTING)\n"
                    "- NEDEN?: Modelimiz GSYIH ve Nufusa bagli calisiyor. Ama 2026'nin GSYIH verisi elimizde yok. O yuzden once girdileri tahmin etmemiz gerekti.\n"
                    "- NASIL? (Adim 1): 'Polinom Regresyon' (np.polyfit, derece=2) ile GSYIH'nin 2028'e kadarki egimini modelledik.\n"
                    "- NASIL? (Adim 2): Tahmin edilen bu GSYIH degerlerini ana Lineer modelimize verdik."))

    # 9. KISI BASI ANALIZ
    pdf.section_header(tr("9. KISI BASI EMISYON"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Burasi cok onemli bir ayrimi gosteriyor. Toplam emisyonlarda Cin lider olsa da, kisi basina dusen emisyonlarda ABD acik ara birincidir. Bu durum, sorunun sadece nufus degil, yasam tarzi ve tuketim aliskanliklari oldugunu net bir sekilde ortaya koyuyor."))
    pdf.tech_box(tr("ANALITIK YONTEM:\n"
                    "- Feature Engineering: `co2_per_capita` dogrudan veri setinde yoktu, biz turettik. (CO2 / Population)"))

    # 10. DEMOGRAFIK DINAMIKLER
    pdf.section_header(tr("10. DEMOGRAFIK DINAMIKLER"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Nufus ve emisyon iliskisini inceledigimizde, her ulkenin farkli bir hikayesi oldugunu goruyoruz. Ornegin Rusya'da nufus azalmasina ragmen emisyonlar dalgali seyrederken, Hindistan'da nufus ve emisyon birebir paralel ilerliyor."))
    pdf.tech_box(tr("TEKNIK: NORMALIZASYON (INDEXING)\n"
                    "- NEDEN?: Nufus (Milyar) ve CO2 (Milyon) farkli olceklerde. Ayni grafikte cizilemezler.\n"
                    "- NASIL?: Hepsini 2004 yilina gore endeksleyip (Base=100) yuzdesel degisime donusturduk."))

    # 11. ENERJI KARMASI
    pdf.section_header(tr("11. ENERJI KARMASI"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Bu grafik ulkelerin enerji 'parmak izlerini' gosteriyor. Cin'in grafigindeki devasa siyah alan komur kullanimini, Rusya'daki mavi alan ise dogalgaz bagimliligini temsil ediyor. Turkiye ise ne yazik ki hala yuksek oranda fosil yakit bagimliligina sahip."))
    pdf.tech_box(tr("GORSELLESTIRME:\n"
                    "- Tur: Stacked Area Chart (Yigilmis Alan Grafigi) - `plt.stackplot`\n"
                    "- NEDEN?: Toplam emisyonun hangi kaynaktan (komur, petrol, gaz) geldigini oransal gostermek icin."))

    # 12. POLITIKA ONERILERI
    pdf.section_header(tr("12. SONUC VE POLITIKA ONERILERI"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Sonuc olarak, veriler bize 'Tek Tip' bir cozumun olamayacagini gosterdi. Analizlerimiz isiginda Turkiye icin acil olarak Gunes ve Ruzgar potansiyelinin degerlendirilmesini, Almanya icin ise komurden cikis surecinin hizlandirilmasini oneriyoruz."))

    # 13. KAPINIS
    pdf.section_header(tr("KAPANIS"))
    pdf.content_block(tr("SUNUM METNI"), 
                      tr("Beni dinlediginiz icin tesekkur ederim. Projenin kodlarina ve detayli raporuna GitHub reposundan erisebilirsiniz. Sorularinizi yanitlamaktan memnuniyet duyarim."))


    pdf.output("Sunum_Rehberi_Profesyonel.pdf")
    print("PDF Olusturuldu: Sunum_Rehberi_Profesyonel.pdf")

if __name__ == "__main__":
    create_guide()
