# database.py

import pyodbc

from config import DB_CONFIG


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

def sayfa_var_mi(baglanti, url):
    """
    URL veritabanında mevcut mu?
    """

    cursor = baglanti.cursor()

    try:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Pages
            WHERE Url = ?
            """,
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

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO dbo.Pages
            (
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
                ?
            )
            """,
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
            WHERE Url=?
            """,
            title,
            content,
            category,
            keywords,
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

def tum_sayfalari_getir():
    """
    RAG sistemi için bütün sayfaları getirir.

    Dönüş:
        [
            {
                "id": ...,
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
                Id,
                Title,
                Url,
                Content,
                Category,
                Keywords
            FROM dbo.Pages
            ORDER BY Id
            """
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
    Id'ye göre tek sayfa döndürür.
    """

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            SELECT
                Id,
                Title,
                Url,
                Content,
                Category,
                Keywords
            FROM dbo.Pages
            WHERE Id=?
            """,
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
    Kategoriye ait sayfaları döndürür.
    """

    baglanti = baglanti_olustur()

    cursor = baglanti.cursor()

    try:

        cursor.execute(
            """
            SELECT
                Id,
                Title,
                Url,
                Content,
                Category,
                Keywords
            FROM dbo.Pages
            WHERE Category=?
            """,
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
                Id,
                Title,
                Url,
                Content,
                Category,
                Keywords
            FROM dbo.Pages
            WHERE
                Title LIKE ?
                OR Keywords LIKE ?
                OR Content LIKE ?
            """,
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