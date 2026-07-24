# normalizer.py

import re


KATEGORI_KEYWORDS = {
    "Genel Trend Özeti": [
        "genel trend",
        "piyasa görünümü",
        "BIST 100",
        "piyasa geneli",
        "endeks durumu",
        "makro göstergeler",
        "destek",
        "direnç",
        "yabancı oranı"
    ],

    "Son Bilançolar": [
        "bilanço",
        "son bilançolar",
        "açıklanan bilançolar",
        "yaklaşan bilançolar",
        "bilanço tarihi",
        "finansal sonuçlar",
        "net dönem karı",
        "F/K",
        "PD/DD"
    ],

    "Halka Arzlar": [
        "halka arz",
        "güncel halka arz",
        "yaklaşan halka arz",
        "halka arz var mı",
        "arz takvimi"
    ],

    "Sektörel Görünüm": [
        "sektörel görünüm",
        "sektör performansı",
        "haftalık sektör görünümü",
        "öne çıkan sektörler",
        "sektör sinyal matrisi",
        "kısa vadeli trend",
        "orta vadeli trend"
    ],

    "Teknik Görünüm": [
        "teknik görünüm",
        "teknik analiz",
        "RSI",
        "MACD",
        "ADX",
        "Bollinger",
        "SMA20",
        "SMA50",
        "kısa vadeli teknik görünüm",
        "orta vadeli teknik görünüm"
    ],

    "Orta Vadeli Takip Listesi": [
        "orta vadeli takip listesi",
        "orta vadeli hisseler",
        "1-3 aylık hisse önerileri",
        "hedef fiyat",
        "potansiyel getiri",
        "analist önerileri",
        "güçlü al"
    ],

    "Kısa Yorum / Haftalık Not": [
        "kısa yorum",
        "haftalık not",
        "piyasa özeti",
        "haftalık piyasa görünümü",
        "analist görüşleri",
        "makro veri etkisi",
        "önümüzdeki hafta ajandası"
    ]
}


def satirlari_temizle(ham_metin):
    """
    Selenium innerText çıktısını temiz bir satır listesine dönüştürür.

    Satır sonlarını korur.
    Satır içindeki gereksiz boşlukları azaltır.
    """

    if not ham_metin:
        return []

    metin = ham_metin.replace("\xa0", " ")
    metin = metin.replace("\r\n", "\n")
    metin = metin.replace("\r", "\n")

    satirlar = []

    for satir in metin.split("\n"):
        satir = re.sub(
            r"[ \t]+",
            " ",
            satir
        ).strip()

        if satir:
            satirlar.append(satir)

    return satirlar


def bolum_arasi_al(
    satirlar,
    baslangic,
    bitis=None
):
    """
    Başlangıç ve bitiş ifadeleri arasındaki satırları döndürür.

    İfadelerin satırla tamamen aynı olmasını şart koşmaz.
    Böylece başlığın yanında ek karakter veya açıklama olsa da bulunur.
    """

    baslangic_indexi = None

    for index, satir in enumerate(satirlar):
        if baslangic.casefold() in satir.casefold():
            baslangic_indexi = index + 1
            break

    if baslangic_indexi is None:
        return []

    if bitis is None:
        return satirlar[baslangic_indexi:]

    for index in range(
        baslangic_indexi,
        len(satirlar)
    ):
        if bitis.casefold() in satirlar[index].casefold():
            return satirlar[
                baslangic_indexi:index
            ]

    return satirlar[baslangic_indexi:]


def ilk_degeri_bul(satirlar, etiket):
    """
    Bir etiketin hemen ardından gelen ilk değeri döndürür.
    """

    for index, satir in enumerate(satirlar):
        if satir.casefold() == etiket.casefold():
            if index + 1 < len(satirlar):
                return satirlar[index + 1]

    return None


def ikinci_degeri_bul(satirlar, etiket):
    """
    Bir etiketin ardından gelen ikinci değeri döndürür.

    Örnek:
    MACD Sinyali
    Negatif
    Histogram düşüyor

    Sonuç:
    Histogram düşüyor
    """

    for index, satir in enumerate(satirlar):
        if satir.casefold() == etiket.casefold():
            if index + 2 < len(satirlar):
                return satirlar[index + 2]

    return None


def bos_degeri_duzelt(deger):
    """
    Boş veya anlamsız tablo değerlerini None yapar.
    """

    if deger is None:
        return None

    temiz_deger = deger.strip()

    if temiz_deger in {
        "",
        "-",
        "—",
        "N/A",
        "n/a"
    }:
        return None

    return temiz_deger


def yuzdeyi_sayiya_cevir(deger):
    """
    Türkçe yüzde metnini float değerine çevirir.

    Örnek:
    +%120,0 -> 120.0
    -%3,25  -> -3.25
    """

    if not deger:
        return None

    temiz = (
        deger
        .replace("%", "")
        .replace("+", "")
        .replace(" ", "")
        .replace(".", "")
        .replace(",", ".")
    )

    try:
        return float(temiz)

    except ValueError:
        return None


def tam_sayi_bul(deger):
    """
    Metindeki ilk tam sayıyı döndürür.

    Örnek:
    '2 aracı kurum' -> 2
    'Toplam 92 kayıt' -> 92
    """

    if not deger:
        return None

    eslesme = re.search(
        r"\d+",
        deger
    )

    if eslesme:
        return int(eslesme.group())

    return None


def saat_sil(tarih):
    """
    Tarihin sonundaki gereksiz 00:00 değerini kaldırır.

    Örnek:
    12 Ağu 00:00 -> 12 Ağu
    """

    if not tarih:
        return tarih

    return re.sub(
        r"\s+00:00$",
        "",
        tarih
    ).strip()


def hisse_kodu_mu(deger):
    """
    Bir metnin BIST hisse koduna benzeyip benzemediğini kontrol eder.
    """

    if not deger:
        return False

    return bool(
        re.fullmatch(
            r"[A-Z0-9]{3,6}",
            deger
        )
    )


# --------------------------------------------------
# GENEL TREND ÖZETİ
# --------------------------------------------------

def genel_degerlendirmeyi_ayikla(satirlar):
    """
    Genel Değerlendirme bölümündeki yorumları alır.

    Grafik ekseni değerlerini ve gereksiz sayıları içermez.
    """

    bolum = bolum_arasi_al(
        satirlar,
        "Genel Değerlendirme",
        "Endeks Durumu"
    )

    sonuc = {
        "trend": None,
        "balance": None,
        "comment": None,
        "global_context": None
    }

    if not bolum:
        return sonuc

    if len(bolum) > 0:
        sonuc["trend"] = bolum[0]

    if len(bolum) > 1:
        sonuc["balance"] = bolum[1]

    if len(bolum) > 2:
        sonuc["comment"] = bolum[2]

    for index, satir in enumerate(bolum):
        if "Küresel Bağlam" in satir:
            if index + 1 < len(bolum):
                sonuc["global_context"] = bolum[index + 1]

            break

    return sonuc


def genel_trend_yapilandir(satirlar, period):
    """
    Genel Trend Özeti sayfasını yapılandırılmış veriye dönüştürür.
    """

    return {
        "period": period or "daily",

        "summary": {
            "bist100": {
                "value": ilk_degeri_bul(
                    satirlar,
                    "BIST-100"
                )
            },

            "market_outlook": {
                "status": ilk_degeri_bul(
                    satirlar,
                    "Piyasa Geneli"
                )
            },

            "foreign_ratio": {
                "value": ilk_degeri_bul(
                    satirlar,
                    "Yabancı Oranı"
                )
            }
        },

        "general_evaluation":
            genel_degerlendirmeyi_ayikla(
                satirlar
            ),

        "macro_indicators": {
            "inflation": ilk_degeri_bul(
                satirlar,
                "Enflasyon (TUFE)"
            ),

            "policy_rate": ilk_degeri_bul(
                satirlar,
                "TCMB Faiz"
            ),

            "usd_try": ilk_degeri_bul(
                satirlar,
                "USD/TRY"
            ),

            "gold_ounce": ilk_degeri_bul(
                satirlar,
                "Altin ($/ons)"
            ),

            "brent_oil": ilk_degeri_bul(
                satirlar,
                "Brent Petrol"
            ),

            "vix": ilk_degeri_bul(
                satirlar,
                "VIX (Korku)"
            )
        },

        "support_resistance": {
            "resistance_3": ilk_degeri_bul(
                satirlar,
                "3. Direnç"
            ),

            "resistance_2": ilk_degeri_bul(
                satirlar,
                "2. Direnç"
            ),

            "resistance_1": ilk_degeri_bul(
                satirlar,
                "1. Direnç"
            ),

            "pivot": ilk_degeri_bul(
                satirlar,
                "Pivot Noktası"
            ),

            "current_price": ilk_degeri_bul(
                satirlar,
                "Güncel Fiyat"
            ),

            "support_1": ilk_degeri_bul(
                satirlar,
                "1. Destek"
            ),

            "support_2": ilk_degeri_bul(
                satirlar,
                "2. Destek"
            ),

            "support_3": ilk_degeri_bul(
                satirlar,
                "3. Destek"
            )
        }
    }


# --------------------------------------------------
# SON BİLANÇOLAR
# --------------------------------------------------

def bilanco_kayitlarini_ayikla(satirlar):
    """
    Son Bilançolar tablosundaki satırları kayıt nesnelerine dönüştürür.

    Kayıt düzeni:

    Hisse kodu
    Açıklama tarihi
    Periyot
    Son fiyat
    G etiketi
    Günlük değişim
    Piyasa değeri
    Net dönem kârı
    Yıllık kâr değişimi
    Bilanço sonrası getiri
    F/K
    PD/DD
    Durum
    """

    try:
        baslangic = satirlar.index("Durum") + 1

    except ValueError:
        return []

    veri = satirlar[baslangic:]

    kayitlar = []
    index = 0

    while index < len(veri):
        if veri[index].startswith("Toplam "):
            break

        if not hisse_kodu_mu(veri[index]):
            index += 1
            continue

        # Bir kayıt, hisse koduyla birlikte 13 elemandan oluşur.
        if index + 12 >= len(veri):
            break

        kayit = {
            "stock_code": veri[index],

            "announcement_date": saat_sil(
                veri[index + 1]
            ),

            "period": veri[index + 2],

            "last_price": veri[index + 3],

            # index + 4 değeri fiyat yanındaki gereksiz G etiketidir.
            "daily_change_percent": veri[index + 5],

            "market_value": veri[index + 6],

            "net_period_profit": bos_degeri_duzelt(
                veri[index + 7]
            ),

            "annual_profit_change": bos_degeri_duzelt(
                veri[index + 8]
            ),

            "post_balance_return": bos_degeri_duzelt(
                veri[index + 9]
            ),

            "price_earnings_ratio": bos_degeri_duzelt(
                veri[index + 10]
            ),

            "price_to_book_ratio": bos_degeri_duzelt(
                veri[index + 11]
            ),

            "status": bos_degeri_duzelt(
                veri[index + 12]
            )
        }

        kayitlar.append(kayit)

        index += 13

    return kayitlar


def son_bilancolar_yapilandir(satirlar):
    """
    Son Bilançolar sayfasının özetini ve kayıtlarını oluşturur.
    """

    return {
        "summary": {
            "total": tam_sayi_bul(
                ilk_degeri_bul(
                    satirlar,
                    "Tümü"
                )
            ),

            "announced": tam_sayi_bul(
                ilk_degeri_bul(
                    satirlar,
                    "Açıklananlar"
                )
            ),

            "upcoming": tam_sayi_bul(
                ilk_degeri_bul(
                    satirlar,
                    "Yaklaşanlar"
                )
            )
        },

        "records": bilanco_kayitlarini_ayikla(
            satirlar
        )
    }


# --------------------------------------------------
# HALKA ARZLAR
# --------------------------------------------------

def halka_arzlar_yapilandir(satirlar):
    """
    Halka arz sayfasındaki güncel ve yaklaşan durumunu oluşturur.
    """

    current_count = tam_sayi_bul(
        ilk_degeri_bul(
            satirlar,
            "Güncel"
        )
    )

    upcoming_count = tam_sayi_bul(
        ilk_degeri_bul(
            satirlar,
            "Yaklaşan"
        )
    )

    status_message = None
    detail = None

    for satir in satirlar:
        if "Gösterilecek halka arz kartı yok" in satir:
            status_message = satir

        if "Şu an listelenecek güncel kart bulunmuyor" in satir:
            detail = satir

    return {
        "current_count": current_count,
        "upcoming_count": upcoming_count,
        "has_current_ipo": bool(current_count),
        "has_upcoming_ipo": bool(upcoming_count),
        "status_message": status_message,
        "detail": detail
    }


# --------------------------------------------------
# SEKTÖREL GÖRÜNÜM
# --------------------------------------------------

def sektor_highlightlarini_ayikla(satirlar):
    """
    Günün Öne Çıkanları bölümündeki sektör yorumlarını ayrıştırır.
    """

    veri = bolum_arasi_al(
        satirlar,
        "Günün Öne Çıkanları"
    )

    sonuc = []
    index = 0

    while index + 2 < len(veri):
        sektor = veri[index]
        yorum = veri[index + 1]
        yuzde = veri[index + 2]

        if (
            "sektör" in yorum.casefold()
            and "%" in yuzde
        ):
            sonuc.append(
                {
                    "sector": sektor,
                    "comment": yorum,
                    "change_percent":
                        yuzdeyi_sayiya_cevir(
                            yuzde
                        )
                }
            )

            index += 3

        else:
            index += 1

    return sonuc


def sektorel_gorunum_yapilandir(
    satirlar,
    period
):
    """
    Sektörel Görünüm sayfasını yapılandırır.
    """

    return {
        "period": period or "weekly",

        "highlights":
            sektor_highlightlarini_ayikla(
                satirlar
            )
    }


# --------------------------------------------------
# TEKNİK GÖRÜNÜM
# --------------------------------------------------

def rsi_dagilimini_ayikla(satirlar):
    """
    RSI Dağılımı bölümünü yapılandırılmış listeye dönüştürür.
    """

    veri = bolum_arasi_al(
        satirlar,
        "RSI Dağılımı"
    )

    sonuc = []
    index = 0

    while index + 2 < len(veri):
        kategori = veri[index]
        yuzde = veri[index + 1]
        hisse_sayisi = veri[index + 2]

        if (
            "%" in yuzde
            and "Hisse" in hisse_sayisi
        ):
            sonuc.append(
                {
                    "category": kategori,

                    "percentage":
                        yuzdeyi_sayiya_cevir(
                            yuzde
                        ),

                    "stock_count":
                        tam_sayi_bul(
                            hisse_sayisi
                        )
                }
            )

            index += 3

        else:
            index += 1

    return sonuc


def teknik_gorunum_yapilandir(
    satirlar,
    period
):
    """
    Teknik Görünüm sayfasının üst özetini ve RSI dağılımını çıkarır.
    """

    return {
        "period": period or "daily",

        "summary": {
            "bist100_rsi14": {
                "value": ilk_degeri_bul(
                    satirlar,
                    "RSI-14 (BİST-100)"
                ),

                "status": ikinci_degeri_bul(
                    satirlar,
                    "RSI-14 (BİST-100)"
                )
            },

            "macd": {
                "signal": ilk_degeri_bul(
                    satirlar,
                    "MACD Sinyali"
                ),

                "comment": ikinci_degeri_bul(
                    satirlar,
                    "MACD Sinyali"
                )
            },

            "bollinger": {
                "position": ilk_degeri_bul(
                    satirlar,
                    "Bollinger Bant"
                ),

                "comment": ikinci_degeri_bul(
                    satirlar,
                    "Bollinger Bant"
                )
            },

            "sma50_trend": {
                "direction": ilk_degeri_bul(
                    satirlar,
                    "Trend (SMA50)"
                ),

                "price_relation": ikinci_degeri_bul(
                    satirlar,
                    "Trend (SMA50)"
                )
            }
        },

        "rsi_distribution":
            rsi_dagilimini_ayikla(
                satirlar
            )
    }


# --------------------------------------------------
# ORTA VADELİ TAKİP LİSTESİ
# --------------------------------------------------

def orta_vade_kayitlarini_ayikla(satirlar):
    """
    Orta Vadeli Takip Listesi tablosunu kayıt nesnelerine dönüştürür.
    """

    try:
        baslangic = satirlar.index("Öneri") + 1

    except ValueError:
        return []

    veri = satirlar[baslangic:]

    sonuc = []
    index = 0

    while index < len(veri):
        if veri[index].startswith("Toplam "):
            break

        if not hisse_kodu_mu(veri[index]):
            index += 1
            continue

        if index + 7 >= len(veri):
            break

        sonuc.append(
            {
                "stock_code": veri[index],

                "sector": veri[index + 1],

                "current_price": veri[index + 2],

                # index + 3, fiyatın yanındaki gereksiz G etiketidir.
                "target_price": veri[index + 4],

                "potential_return_percent":
                    yuzdeyi_sayiya_cevir(
                        veri[index + 5]
                    ),

                "analyst_count":
                    tam_sayi_bul(
                        veri[index + 6]
                    ),

                "recommendation":
                    veri[index + 7]
            }
        )

        index += 8

    return sonuc


def orta_vadeli_takip_yapilandir(satirlar):
    """
    Orta vadeli takip listesinin özetini ve kayıtlarını oluşturur.
    """

    toplam = None

    for satir in satirlar:
        if satir.startswith("Toplam "):
            toplam = tam_sayi_bul(satir)
            break

    return {
        "summary": {
            "time_horizon": "1-3 ay",

            "description": (
                "Analistlerin 1-3 aylık vadede "
                "takip ettiği hisseler"
            ),

            "total_record_count": toplam
        },

        "records":
            orta_vade_kayitlarini_ayikla(
                satirlar
            )
    }


# --------------------------------------------------
# KISA YORUM / HAFTALIK NOT
# --------------------------------------------------

def ajandayi_ayikla(satirlar):
    """
    Önümüzdeki Hafta Ajandası tablosunu kayıt nesnelerine dönüştürür.
    """

    veri = bolum_arasi_al(
        satirlar,
        "Önümüzdeki Hafta Ajandası"
    )

    basliklar = {
        "Tarih",
        "Etkinlik / Veri",
        "Ülke"
    }

    veri = [
        satir
        for satir in veri
        if satir not in basliklar
    ]

    sonuc = []
    index = 0

    while index + 2 < len(veri):
        tarih = veri[index]
        etkinlik = veri[index + 1]
        ulke = veri[index + 2]

        if re.search(
            r"\d{1,2}\s+\w+\s+\d{2}:\d{2}",
            tarih
        ):
            sonuc.append(
                {
                    "datetime": tarih,
                    "event": etkinlik,
                    "country": ulke
                }
            )

            index += 3

        else:
            index += 1

    return sonuc[:15]


def haftalik_not_yapilandir(satirlar):
    """
    Kısa Yorum / Haftalık Not sayfasındaki AI özetini
    ve önümüzdeki hafta ajandasını yapılandırır.

    Başlıklar birebir bulunamazsa AI Özeti ile
    Analist Görüşleri arasındaki metni genel özet olarak saklar.
    """

    updated_at = None

    for satir in satirlar:
        if "Son güncelleme:" in satir:
            updated_at = satir.split(
                "Son güncelleme:",
                maxsplit=1
            )[1].strip()
            break

    # Sayfada bulunması muhtemel özet başlıkları.
    bilinen_basliklar = [
        "BIST Gün Ortası Görünümü",
        "BIST 100 Gün Ortası Görünümü",
        "Piyasa Görünümü",
        "Küresel Piyasalarda Son Durum",
        "Küresel Piyasa Görünümü",
        "Sektörel Performanslar",
        "Sektörel Değerlendirme",
        "Makro Veri Etkisi",
        "Teknik Görünüm"
    ]

    # AI Özeti ile Analist Görüşleri arasındaki bütün alanı al.
    ai_ozet_satirlari = bolum_arasi_al(
        satirlar,
        "Ekofin AI Özeti",
        "Analist Görüşleri"
    )

    # AI açıklaması ve güncelleme bilgisini özet metninden çıkar.
    gereksiz_ifadeler = {
        "Yapay zeka destekli faaliyet raporu analizi"
    }

    temiz_ai_satirlari = []

    for satir in ai_ozet_satirlari:
        if satir in gereksiz_ifadeler:
            continue

        if "Son güncelleme:" in satir:
            continue

        temiz_ai_satirlari.append(satir)

    sections = []

    # Bulunan başlıkların özet alanındaki konumlarını tespit et.
    bulunan_basliklar = []

    for index, satir in enumerate(temiz_ai_satirlari):
        for baslik in bilinen_basliklar:
            if baslik.casefold() in satir.casefold():
                bulunan_basliklar.append(
                    {
                        "index": index,
                        "title": satir
                    }
                )
                break

    # Başlıklar bulunduysa her başlığı kendi metniyle eşleştir.
    for sira, bulunan in enumerate(bulunan_basliklar):
        baslangic_indexi = bulunan["index"] + 1

        if sira + 1 < len(bulunan_basliklar):
            bitis_indexi = bulunan_basliklar[
                sira + 1
            ]["index"]
        else:
            bitis_indexi = len(temiz_ai_satirlari)

        metin_satirlari = temiz_ai_satirlari[
            baslangic_indexi:bitis_indexi
        ]

        metin = " ".join(metin_satirlari).strip()

        if metin:
            sections.append(
                {
                    "title": bulunan["title"],
                    "text": metin
                }
            )

    # Başlıklar bulunamazsa bütün AI özetini tek bölüm olarak sakla.
    if not sections and temiz_ai_satirlari:
        sections.append(
            {
                "title": "Piyasa Özeti",
                "text": " ".join(
                    temiz_ai_satirlari
                ).strip()
            }
        )

    return {
        "ai_summary": {
            "updated_at": updated_at,
            "sections": sections
        },

        "next_week_agenda": ajandayi_ayikla(
            satirlar
        )
    }


# --------------------------------------------------
# ORTAK YAPILANDIRMA
# --------------------------------------------------

def icerigi_yapilandir(
    ham_metin,
    kategori,
    period=None
):
    """
    Kategoriye göre uygun yapılandırıcı fonksiyonu çağırır.
    """

    satirlar = satirlari_temizle(
        ham_metin
    )

    if kategori == "Genel Trend Özeti":
        return genel_trend_yapilandir(
            satirlar,
            period
        )

    if kategori == "Son Bilançolar":
        return son_bilancolar_yapilandir(
            satirlar
        )

    if kategori == "Halka Arzlar":
        return halka_arzlar_yapilandir(
            satirlar
        )

    if kategori == "Sektörel Görünüm":
        return sektorel_gorunum_yapilandir(
            satirlar,
            period
        )

    if kategori == "Teknik Görünüm":
        return teknik_gorunum_yapilandir(
            satirlar,
            period
        )

    if kategori == "Orta Vadeli Takip Listesi":
        return orta_vadeli_takip_yapilandir(
            satirlar
        )

    if kategori == "Kısa Yorum / Haftalık Not":
        return haftalik_not_yapilandir(
            satirlar
        )

    return {}


def anahtar_kelime_uret(kategori):
    """
    Kategoriye ait arama anahtar kelimelerini döndürür.
    """

    return KATEGORI_KEYWORDS.get(
        kategori,
        []
    )