USE [finalcase];
GO

IF OBJECT_ID(N'dbo.Pages', N'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.Pages;
END;
GO

CREATE TABLE dbo.Pages
(
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(500) NULL,
    Url NVARCHAR(1000) NULL,
    Content NVARCHAR(MAX) NULL,
    Category NVARCHAR(200) NULL,
    Keywords NVARCHAR(1000) NULL
);
GO

SET IDENTITY_INSERT dbo.Pages ON;
GO

INSERT INTO dbo.Pages
(
    Id,
    Title,
    Url,
    Content,
    Category,
    Keywords
)
VALUES
(
    1,
    N'Son Bilançolar',
    N'https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/son-bilancolar',
    N'{
  "page": "Son Bilançolar",
  "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/son-bilancolar",
  "keywords": [
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
  "content": {
    "summary": {
      "total": 632,
      "announced": 616,
      "upcoming": 16
    },
    "records": [
      {
        "stock_code": "SAHOL",
        "announcement_date": "12 Ağu",
        "period": "2026/06",
        "last_price": "88,65",
        "daily_change_percent": "+0,28",
        "market_value": "186.51 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "AEFES",
        "announcement_date": "11 Ağu",
        "period": "2026/06",
        "last_price": "22,10",
        "daily_change_percent": "-0,63",
        "market_value": "130.86 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "MGROS",
        "announcement_date": "11 Ağu",
        "period": "2026/06",
        "last_price": "639,00",
        "daily_change_percent": "+0,47",
        "market_value": "115.69 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "CCOLA",
        "announcement_date": "10 Ağu",
        "period": "2026/06",
        "last_price": "92,00",
        "daily_change_percent": "-0,38",
        "market_value": "258.68 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "GWIND",
        "announcement_date": "10 Ağu",
        "period": "2026/06",
        "last_price": "25,90",
        "daily_change_percent": "+3,68",
        "market_value": "13.99 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "BRSAN",
        "announcement_date": "7 Ağu",
        "period": "2026/06",
        "last_price": "565,00",
        "daily_change_percent": "+0,18",
        "market_value": "79.89 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "LILAK",
        "announcement_date": "5 Ağu",
        "period": "2026/06",
        "last_price": "30,78",
        "daily_change_percent": "0,00",
        "market_value": "18.15 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "TTKOM",
        "announcement_date": "5 Ağu",
        "period": "2026/06",
        "last_price": "58,80",
        "daily_change_percent": "+0,34",
        "market_value": "205.63 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "FROTO",
        "announcement_date": "4 Ağu",
        "period": "2026/06",
        "last_price": "81,45",
        "daily_change_percent": "+0,43",
        "market_value": "285.47 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "TUPRS",
        "announcement_date": "4 Ağu",
        "period": "2026/06",
        "last_price": "312,50",
        "daily_change_percent": "+0,97",
        "market_value": "601.64 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "ISATR",
        "announcement_date": "3 Ağu",
        "period": "2026/06",
        "last_price": "4.950.000,00",
        "daily_change_percent": "0,00",
        "market_value": "4.95 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "ISBTR",
        "announcement_date": "3 Ağu",
        "period": "2026/06",
        "last_price": "515.755,00",
        "daily_change_percent": "-4,48",
        "market_value": "14.96 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "YKBNK",
        "announcement_date": "31 Tem",
        "period": "2026/06",
        "last_price": "32,98",
        "daily_change_percent": "+0,37",
        "market_value": "278.58 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "TOASO",
        "announcement_date": "29 Tem",
        "period": "2026/06",
        "last_price": "295,50",
        "daily_change_percent": "-1,50",
        "market_value": "148.63 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      },
      {
        "stock_code": "AKBNK",
        "announcement_date": "28 Tem",
        "period": "2026/06",
        "last_price": "66,40",
        "daily_change_percent": "-0,45",
        "market_value": "345.02 Mr",
        "net_period_profit": null,
        "annual_profit_change": null,
        "post_balance_return": null,
        "price_earnings_ratio": null,
        "price_to_book_ratio": null,
        "status": "Yaklaşıyor"
      }
    ]
  }
}',
    N'Son Bilançolar',
    N'bilanço, son bilançolar, açıklanan bilançolar, yaklaşan bilançolar, bilanço tarihi, finansal sonuçlar, net dönem karı, F/K, PD/DD'
);
GO

INSERT INTO dbo.Pages
(
    Id,
    Title,
    Url,
    Content,
    Category,
    Keywords
)
VALUES
(
    2,
    N'Halka Arzlar',
    N'https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/halka-arzlar',
    N'{
  "page": "Halka Arzlar",
  "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/halka-arzlar",
  "keywords": [
    "halka arz",
    "güncel halka arz",
    "yaklaşan halka arz",
    "halka arz var mı",
    "arz takvimi"
  ],
  "content": {
    "current_count": 0,
    "upcoming_count": 0,
    "has_current_ipo": false,
    "has_upcoming_ipo": false,
    "status_message": "Gösterilecek halka arz kartı yok.",
    "detail": "Şu an listelenecek güncel kart bulunmuyor."
  }
}',
    N'Halka Arzlar',
    N'halka arz, güncel halka arz, yaklaşan halka arz, halka arz var mı, arz takvimi'
);
GO

INSERT INTO dbo.Pages
(
    Id,
    Title,
    Url,
    Content,
    Category,
    Keywords
)
VALUES
(
    3,
    N'Sektörel Görünüm',
    N'https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/sektorel-gorunum',
    N'{
  "page": "Sektörel Görünüm",
  "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/sektorel-gorunum",
  "keywords": [
    "sektörel görünüm",
    "sektör performansı",
    "haftalık sektör görünümü",
    "öne çıkan sektörler",
    "sektör sinyal matrisi",
    "kısa vadeli trend",
    "orta vadeli trend"
  ],
  "content": {
    "period": "weekly",
    "highlights": [
      {
        "sector": "Hukuk ve Muhasebe Faaliyetleri",
        "comment": "Seçili periyotta sektör genelinde alımlar öne çıkıyor.",
        "change_percent": 9.98
      },
      {
        "sector": "Seyahat Acentesi, Tur Operatörü",
        "comment": "Seçili periyotta sektör genelinde alımlar öne çıkıyor.",
        "change_percent": 9.93
      },
      {
        "sector": "Mimarlık ve Mühendislik Faaliyetleri",
        "comment": "Seçili periyotta sektör negatif ayrışıyor.",
        "change_percent": -2.86
      }
    ]
  }
}',
    N'Sektörel Görünüm',
    N'sektörel görünüm, sektör performansı, haftalık sektör görünümü, öne çıkan sektörler, sektör sinyal matrisi, kısa vadeli trend, orta vadeli trend'
);
GO

INSERT INTO dbo.Pages
(
    Id,
    Title,
    Url,
    Content,
    Category,
    Keywords
)
VALUES
(
    4,
    N'Teknik Görünüm',
    N'https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/teknik',
    N'{
  "page": "Teknik Görünüm",
  "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/teknik",
  "keywords": [
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
  "content": {
    "period": "daily",
    "summary": {
      "bist100_rsi14": {
        "value": "43,7",
        "status": "Nötr Bölge (40–60)"
      },
      "macd": {
        "signal": "Negatif",
        "comment": "Histogram düşüyor"
      },
      "bollinger": {
        "position": "Orta Bant",
        "comment": "Sıkışma bölgesi var"
      },
      "sma50_trend": {
        "direction": "Aşağı",
        "price_relation": "Fiyat < SMA50"
      }
    },
    "rsi_distribution": [
      {
        "category": "Aşırı Alım (>70)",
        "percentage": 4.0,
        "stock_count": 23
      },
      {
        "category": "Güçlü - RSI (60-70)",
        "percentage": 8.0,
        "stock_count": 50
      },
      {
        "category": "Nötr (40-60)",
        "percentage": 55.0,
        "stock_count": 334
      },
      {
        "category": "Zayıf (30-40)",
        "percentage": 28.0,
        "stock_count": 169
      },
      {
        "category": "Aşırı Satım (<30)",
        "percentage": 5.0,
        "stock_count": 31
      }
    ]
  }
}',
    N'Teknik Görünüm',
    N'teknik görünüm, teknik analiz, RSI, MACD, ADX, Bollinger, SMA20, SMA50, kısa vadeli teknik görünüm, orta vadeli teknik görünüm'
);
GO

INSERT INTO dbo.Pages
(
    Id,
    Title,
    Url,
    Content,
    Category,
    Keywords
)
VALUES
(
    5,
    N'Orta Vadeli Takip Listesi',
    N'https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/orta-vadeli-takip-listesi',
    N'{
  "page": "Orta Vadeli Takip Listesi",
  "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/orta-vadeli-takip-listesi",
  "keywords": [
    "orta vadeli takip listesi",
    "orta vadeli hisseler",
    "1-3 aylık hisse önerileri",
    "hedef fiyat",
    "potansiyel getiri",
    "analist önerileri",
    "güçlü al"
  ],
  "content": {
    "summary": {
      "time_horizon": "1-3 ay",
      "description": "Analistlerin 1-3 aylık vadede takip ettiği hisseler",
      "total_record_count": 92
    },
    "records": [
      {
        "stock_code": "BIGCH",
        "sector": "Yiyecek ve İçecek Hizmetleri",
        "current_price": "7,07",
        "target_price": "20,28",
        "potential_return_percent": 182.5,
        "analyst_count": 2,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "KLKIM",
        "sector": "Taş ve Toprağa Dayalı",
        "current_price": "27,16",
        "target_price": "59,22",
        "potential_return_percent": 118.8,
        "analyst_count": 6,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "GLCVY",
        "sector": "Varlık Yönetim Şirketleri",
        "current_price": "55,90",
        "target_price": "121,06",
        "potential_return_percent": 116.8,
        "analyst_count": 3,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "TKNSA",
        "sector": "Perakende Ticaret",
        "current_price": "18,19",
        "target_price": "37,91",
        "potential_return_percent": 108.8,
        "analyst_count": 6,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "ISFIN",
        "sector": "Finansal Kiralama ve Faktoring Şirketleri",
        "current_price": "19,44",
        "target_price": "40,00",
        "potential_return_percent": 106.4,
        "analyst_count": 2,
        "recommendation": "Tut / Nötr"
      },
      {
        "stock_code": "GEDZA",
        "sector": "Kimya, İlaç, Petrol, Lastik ve Plastik",
        "current_price": "29,66",
        "target_price": "56,60",
        "potential_return_percent": 90.3,
        "analyst_count": 2,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "HTTBT",
        "sector": "Bilişim",
        "current_price": "37,18",
        "target_price": "69,41",
        "potential_return_percent": 88.1,
        "analyst_count": 4,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "ULKER",
        "sector": "Gıda, İçecek ve Tütün",
        "current_price": "96,10",
        "target_price": "179,75",
        "potential_return_percent": 86.8,
        "analyst_count": 14,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "KOTON",
        "sector": "Perakende Ticaret",
        "current_price": "13,73",
        "target_price": "25,50",
        "potential_return_percent": 85.6,
        "analyst_count": 7,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "SAHOL",
        "sector": "Holdingler ve Yatırım Şirketleri",
        "current_price": "88,65",
        "target_price": "164,37",
        "potential_return_percent": 84.3,
        "analyst_count": 14,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "LKMNH",
        "sector": "İnsan Sağlığı ve Sosyal Hizmetler",
        "current_price": "14,72",
        "target_price": "26,80",
        "potential_return_percent": 81.6,
        "analyst_count": 5,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "FROTO",
        "sector": "Metal Eşya Makine Elektrikli Cihaz Ulaşım Araçları",
        "current_price": "81,40",
        "target_price": "147,46",
        "potential_return_percent": 80.1,
        "analyst_count": 29,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "YATAS",
        "sector": "Tekstil, Giyim Eşyası ve Deri",
        "current_price": "36,08",
        "target_price": "64,77",
        "potential_return_percent": 79.3,
        "analyst_count": 6,
        "recommendation": "Güçlü Al"
      },
      {
        "stock_code": "OTKAR",
        "sector": "Metal Eşya Makine Elektrikli Cihaz Ulaşım Araçları",
        "current_price": "323,00",
        "target_price": "576,89",
        "potential_return_percent": 78.9,
        "analyst_count": 9,
        "recommendation": "Al"
      },
      {
        "stock_code": "GLRMK",
        "sector": "İnşaat ve Bayındırlık İşleri",
        "current_price": "163,70",
        "target_price": "290,09",
        "potential_return_percent": 77.9,
        "analyst_count": 6,
        "recommendation": "Güçlü Al"
      }
    ]
  }
}',
    N'Orta Vadeli Takip Listesi',
    N'orta vadeli takip listesi, orta vadeli hisseler, 1-3 aylık hisse önerileri, hedef fiyat, potansiyel getiri, analist önerileri, güçlü al'
);
GO

INSERT INTO dbo.Pages
(
    Id,
    Title,
    Url,
    Content,
    Category,
    Keywords
)
VALUES
(
    6,
    N'Kısa Yorum / Haftalık Not',
    N'https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/kisa-yorum-haftalik-not',
    N'{
  "page": "Kısa Yorum / Haftalık Not",
  "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/kisa-yorum-haftalik-not",
  "keywords": [
    "kısa yorum",
    "haftalık not",
    "piyasa özeti",
    "haftalık piyasa görünümü",
    "analist görüşleri",
    "makro veri etkisi",
    "önümüzdeki hafta ajandası"
  ],
  "content": {
    "ai_summary": {
      "updated_at": "22 Temmuz 2026, Çarşamba — 14:43",
      "sections": [
        {
          "title": "Piyasa Görünümü",
          "text": "BIST 100 endeksi hafta boyunca yatay seyir izledi. Bankacılık ve savunma hisseleri endekse pozitif katkı sağlarken, enerji sektöründe kar satışları dikkat çekti. Küresel piyasalarda ABD tarafında faiz beklentileri fiyatlamalara yansımaya devam ediyor."
        },
        {
          "title": "Sektörel Değerlendirme",
          "text": "Bankacılık sektöründe kredi büyümesi verileri olumlu seyrederken, savunma sanayi hisseleri yeni sipariş haberleriyle öne çıktı. Perakende tarafında tüketim verileri sektör performansını destekleyici nitelikte."
        },
        {
          "title": "Teknik Görünüm",
          "text": "Endeks 11.111 seviyesinde dirençle karşılaşıyor. Kısa vadede 11.111 destek bölgesinin korunması kritik. Hacim artışı ile birlikte yukarı yönlü kırılım senaryosu gündeme gelebilir."
        }
      ]
    },
    "next_week_agenda": [
      {
        "datetime": "20 Temmuz 01:45",
        "event": "İhracatlar (Haz)",
        "country": "Yeni Zelanda"
      },
      {
        "datetime": "20 Temmuz 01:45",
        "event": "İthalatlar (Haz)",
        "country": "Yeni Zelanda"
      },
      {
        "datetime": "20 Temmuz 01:45",
        "event": "Ticaret Dengesi (Aylık) (Haz)",
        "country": "Yeni Zelanda"
      },
      {
        "datetime": "20 Temmuz 01:45",
        "event": "Ticaret Dengesi (Yıllık) (Haz)",
        "country": "Yeni Zelanda"
      },
      {
        "datetime": "20 Temmuz 02:01",
        "event": "Rightmove Ev Fiyat Endeksi (Yıllık) (Tem)",
        "country": "Birleşik Krallık"
      },
      {
        "datetime": "20 Temmuz 04:00",
        "event": "PBOC En Düşük Kredi Faiz Oranı (Tem)",
        "country": "Çin"
      },
      {
        "datetime": "20 Temmuz 04:15",
        "event": "PBOC En Düşük Kredi Faiz Oranı",
        "country": "Çin"
      },
      {
        "datetime": "20 Temmuz 07:00",
        "event": "İhracatlar (Yıllık) (Haz)",
        "country": "Malezya"
      },
      {
        "datetime": "20 Temmuz 07:00",
        "event": "İthalatlar (Yıllık) (Haz)",
        "country": "Malezya"
      },
      {
        "datetime": "20 Temmuz 07:00",
        "event": "Ticaret Dengesi (Haz)",
        "country": "Malezya"
      },
      {
        "datetime": "20 Temmuz 08:00",
        "event": "Estonya Üretici Fiyat Endeksi (ÜFE) (Aylık) (Haz)",
        "country": "Estonya"
      },
      {
        "datetime": "20 Temmuz 08:00",
        "event": "Estonya Üretici Fiyat Endeksi (ÜFE) (Yıllık) (Haz)",
        "country": "Estonya"
      },
      {
        "datetime": "20 Temmuz 09:00",
        "event": "Almanya Üretici Fiyat Endeksi (ÜFE) (Aylık) (Haz)",
        "country": "Almanya"
      },
      {
        "datetime": "20 Temmuz 09:00",
        "event": "Almanya Üretici Fiyat Endeksi (ÜFE) (Yıllık) (Haz)",
        "country": "Almanya"
      },
      {
        "datetime": "20 Temmuz 10:00",
        "event": "Yıl Sonu Tüketici Fiyat Endeksi (TÜFE) Tahmini (Tem)",
        "country": "Türkiye"
      }
    ]
  }
}',
    N'Kısa Yorum / Haftalık Not',
    N'kısa yorum, haftalık not, piyasa özeti, haftalık piyasa görünümü, analist görüşleri, makro veri etkisi, önümüzdeki hafta ajandası'
);
GO

INSERT INTO dbo.Pages
(
    Id,
    Title,
    Url,
    Content,
    Category,
    Keywords
)
VALUES
(
    7,
    N'Genel Trend Özeti',
    N'https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/genel-trend-ozeti',
    N'{
  "page": "Genel Trend Özeti",
  "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/genel-trend-ozeti",
  "keywords": [
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
  "content": {
    "period": "daily",
    "summary": {
      "bist100": {
        "value": "14.034,08"
      },
      "market_outlook": {
        "status": "Boğa Eğilimli"
      },
      "foreign_ratio": {
        "value": "21,4"
      }
    },
    "general_evaluation": {
      "trend": "Boğa Eğilimli",
      "balance": "Dengeli",
      "comment": "Piyasa genelinde ortalama getiri pozitif. Görünüm yukarı eğilimli, ancak hareket seçici ilerliyor.",
      "global_context": "VIX normal bölgede yükseliyor; küresel risk algısı artıyor. USD/TRY -0,01, Brent 2,08 değişimde."
    },
    "macro_indicators": {
      "inflation": "%32,1",
      "policy_rate": "%37,0",
      "usd_try": "47,06",
      "gold_ounce": "4.014",
      "brent_oil": "73,62",
      "vix": "17,4"
    },
    "support_resistance": {
      "resistance_3": "14.503,10",
      "resistance_2": "14.348,54",
      "resistance_1": "14.219,63",
      "pivot": "14.065,07",
      "current_price": "14.034,08",
      "support_1": "13.936,16",
      "support_2": "13.781,60",
      "support_3": "13.652,69"
    }
  }
}',
    N'Genel Trend Özeti',
    N'genel trend, piyasa görünümü, BIST 100, piyasa geneli, endeks durumu, makro göstergeler, destek, direnç, yabancı oranı'
);
GO

SET IDENTITY_INSERT dbo.Pages OFF;
GO

SELECT
    Id,
    Title,
    Category,
    ISJSON(Content) AS JsonGecerliMi
FROM dbo.Pages
ORDER BY Id;
GO
