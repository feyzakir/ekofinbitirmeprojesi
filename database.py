# database.py
import pyodbc
import uuid
import json
from config import DB_CONFIG
APPLICATION_NAME = "Ekofin"
# ==========================================================
# BAĞLANTI
# ==========================================================

def baglanti_olustur():
    """
    config.py dosyasındaki bağlantı bilgilerini kullanarak
    SQL Server bağlantısı oluşturur.
    """

    return pyodbc.connect(DB_CONFIG)


# ==========================================================
# SCRAPER TARAFI (ELİF)
# ==========================================================
def tum_sayfalari_getir(baglanti):
    """
    Scraper için seçili uygulamaya ait tüm sayfaları getirir.
    """

    application_id = application_id_getir(baglanti)

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            SELECT
                Title,
                Url,
                Category
            FROM dbo.Pages
            WHERE ApplicationId = ?
            ORDER BY Id
            """,
            application_id
        )

        sonuc = []

        for row in cursor.fetchall():

            sonuc.append(
                {
                    "title": row.Title,
                    "category": row.Category,
                    "url": row.Url
                }
            )

        return sonuc

    finally:

        cursor.close()
def application_id_getir(baglanti):
    """
    ApplicationName'den ApplicationId döndürür.
    """

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            SELECT Id
            FROM dbo.Applications
            WHERE ApplicationName = ?
            """,
            APPLICATION_NAME
        )

        sonuc = cursor.fetchone()

        if sonuc is None:
            raise Exception(f"{APPLICATION_NAME} bulunamadı.")

        return sonuc[0]

    finally:

        cursor.close()


def sayfa_var_mi(baglanti, url):
    """
    URL veritabanında mevcut mu?
    """
    application_id = application_id_getir(baglanti)

    cursor = baglanti.cursor()

    try:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Pages
            WHERE
                ApplicationId=?
                AND Url=?
            """,
            application_id,
            url
        )

        sonuc = cursor.fetchone()

        if sonuc is None:
            return False

        return sonuc[0] > 0

    finally:
        cursor.close()


def sayfa_ekle(
    baglanti,
    title,
    url,
    content,
    category,
    keywords
):
    """
    Yeni sayfa ekler.
    """

    application_id = application_id_getir(baglanti)

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO dbo.Pages
            (
                ApplicationId,
                Title,
                Url,
                Content,
                Category,
                Keywords
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """,
            application_id,
            title,
            url,
            content,
            category,
            keywords
        )

        baglanti.commit()

    except Exception:

        baglanti.rollback()
        raise

    finally:

        cursor.close()

def sayfa_guncelle(
    baglanti,
    url,
    title,
    content,
    category,
    keywords
):
    """
    Mevcut sayfayı günceller.
    """

    application_id = application_id_getir(baglanti)

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            UPDATE dbo.Pages
            SET
                Title=?,
                Content=?,
                Category=?,
                Keywords=?
            WHERE
                ApplicationId=?
                AND Url=?
            """,
            title,
            content,
            category,
            keywords,
            application_id,
            url
        )

        baglanti.commit()

    except Exception:

        baglanti.rollback()
        raise

    finally:

        cursor.close()

# ==========================================================
# KİŞİ 2 (RAG)
# ==========================================================

def tum_sayfalari_getir_rag():
    """
    RAG sistemi için seçili uygulamaya ait bütün sayfaları getirir.

    Dönüş:
        [
            {
                "id": ...,
                "applicationname": ...,
                "title": ...,
                "url": ...,
                "content": ...,
                "category": ...,
                "keywords": ...
            }
        ]
    """

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            SELECT
                p.Id,
                a.ApplicationName,
                p.Title,
                p.Url,
                p.Content,
                p.Category,
                p.Keywords
            FROM dbo.Pages p
            INNER JOIN dbo.Applications a
                ON p.ApplicationId = a.Id
            WHERE a.ApplicationName = ?
            ORDER BY p.Id
            """,
            APPLICATION_NAME
        )

        kolonlar = [
            kolon[0].lower()
            for kolon in cursor.description
        ]

        sonuc = []

        for satir in cursor.fetchall():

            sonuc.append(
                dict(
                    zip(
                        kolonlar,
                        satir
                    )
                )
            )

        return sonuc

    finally:

        cursor.close()
        baglanti.close()

def sayfa_getir(page_id):
    """
    Id'ye göre seçili uygulamaya ait tek sayfayı döndürür.
    """

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            SELECT
                p.Id,
                a.ApplicationName,
                p.Title,
                p.Url,
                p.Content,
                p.Category,
                p.Keywords
            FROM dbo.Pages p
            INNER JOIN dbo.Applications a
                ON p.ApplicationId = a.Id
            WHERE
                a.ApplicationName = ?
                AND p.Id = ?
            """,
            APPLICATION_NAME,
            page_id
        )

        satir = cursor.fetchone()

        if satir is None:
            return None

        kolonlar = [
            kolon[0].lower()
            for kolon in cursor.description
        ]

        return dict(
            zip(
                kolonlar,
                satir
            )
        )

    finally:

        cursor.close()
        baglanti.close()

def kategoriye_gore_getir(kategori):
    """
    Seçili uygulamada belirtilen kategoriye ait sayfaları döndürür.
    """

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            SELECT
                p.Id,
                a.ApplicationName,
                p.Title,
                p.Url,
                p.Content,
                p.Category,
                p.Keywords
            FROM dbo.Pages p
            INNER JOIN dbo.Applications a
                ON p.ApplicationId = a.Id
            WHERE
                a.ApplicationName = ?
                AND p.Category = ?
            ORDER BY p.Id
            """,
            APPLICATION_NAME,
            kategori
        )

        kolonlar = [
            kolon[0].lower()
            for kolon in cursor.description
        ]

        sonuc = []

        for satir in cursor.fetchall():

            sonuc.append(
                dict(
                    zip(
                        kolonlar,
                        satir
                    )
                )
            )

        return sonuc

    finally:

        cursor.close()
        baglanti.close()

def keyword_ara(keyword):
    """
    Basit SQL araması.

    Hybrid Search içinde kullanılacak.
    """

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    try:

        arama = f"%{keyword}%"

        cursor.execute(
            """
            SELECT
                p.Id,
                a.ApplicationName,
                p.Title,
                p.Url,
                p.Content,
                p.Category,
                p.Keywords
            FROM dbo.Pages p
            INNER JOIN dbo.Applications a
                ON p.ApplicationId = a.Id
            WHERE
                a.ApplicationName = ?
                AND
                (
                    p.Title LIKE ?
                    OR p.Keywords LIKE ?
                    OR p.Content LIKE ?
                )
            ORDER BY p.Id
            """,
            APPLICATION_NAME,
            arama,
            arama,
            arama
        )

        kolonlar = [
            kolon[0].lower()
            for kolon in cursor.description
        ]

        sonuc = []

        for satir in cursor.fetchall():

            sonuc.append(
                dict(
                    zip(
                        kolonlar,
                        satir
                    )
                )
            )

        return sonuc

    finally:

        cursor.close()
        baglanti.close()

def yeni_session(user_id=None, title="Yeni Sohbet"):

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    session_id = str(uuid.uuid4())

    cursor.execute("""

        INSERT INTO ChatSessions
        (SessionId, UserId, Title)

        VALUES (?, ?, ?)

    """, session_id, user_id, title)

    baglanti.commit()

    baglanti.close()

    return session_id
def mesaj_ekle(session_id, role, message):

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    cursor.execute("""

        INSERT INTO ChatMessages
        (SessionId, Role, Message)

        VALUES (?, ?, ?)

    """, session_id, role, message)

    baglanti.commit()

    baglanti.close()
def mesajlari_getir(session_id, limit=10):

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    cursor.execute("""

        SELECT TOP (?)
            Role,
            Message,
            CreatedAt

        FROM ChatMessages

        WHERE SessionId=?

        ORDER BY Id DESC

    """, limit, session_id)

    rows = cursor.fetchall()

    baglanti.close()

    rows = rows[::-1]

    sonuc = []

    for row in rows:

        sonuc.append({

            "role": row.Role,

            "message": row.Message,

            "created_at": row.CreatedAt

        })

    return sonuc
def sessionlari_getir():

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    cursor.execute("""

        SELECT
            SessionId,
            Title,
            CreatedAt

        FROM ChatSessions

        ORDER BY UpdatedAt DESC

    """)

    rows = cursor.fetchall()

    baglanti.close()

    sonuc = []

    for row in rows:

        sonuc.append({

            "session_id": row.SessionId,

            "title": row.Title,

            "created_at": row.CreatedAt

        })

    return sonuc
def session_mesajlarini_getir(session_id):

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    try:

        cursor.execute("""

            SELECT
                Role,
                Message

            FROM ChatMessages

            WHERE SessionId = ?

            ORDER BY Id

        """, session_id)

        sonuc = []

        for row in cursor.fetchall():

            sonuc.append({

                "role": row.Role,

                "content": row.Message

            })

        return sonuc

    finally:

        cursor.close()
        baglanti.close()