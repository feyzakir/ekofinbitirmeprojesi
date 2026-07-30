# config.py

DB_CONFIG = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=MSI\\SQL2022;"
    "DATABASE=GenericChatbotDB;"
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
