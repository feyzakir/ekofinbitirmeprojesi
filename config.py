# config.py

DB_CONFIG = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=MSI\\SQL2022;"
    "DATABASE=finalcase;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

SAYFALAR = [
    {
        "category": "Genel Trend Özeti",
        "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/genel-trend-ozeti"
    },
    {
        "category": "Son Bilançolar",
        "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/son-bilancolar"
    },
    {
        "category": "Halka Arzlar",
        "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/halka-arzlar"
    },
    {
        "category": "Sektörel Görünüm",
        "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/sektorel-gorunum"
    },
    {
        "category": "Teknik Görünüm",
        "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/teknik"
    },
    {
        "category": "Orta Vadeli Takip Listesi",
        "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/orta-vadeli-takip-listesi"
    },
    {
        "category": "Kısa Yorum / Haftalık Not",
        "url": "https://qa.ekofin.net/yeni-tasarim/piyasa-gorunumu/kisa-yorum-haftalik-not"
    }
]