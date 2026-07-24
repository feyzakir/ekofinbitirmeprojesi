# database.py

import pyodbc

from config import DB_CONFIG


def baglanti_olustur():
    """
    config.py dosyasındaki bağlantı bilgilerini kullanarak
    SQL Server bağlantısı oluşturur.

    Dönüş değeri:
        pyodbc.Connection
    """

    return pyodbc.connect(DB_CONFIG)


def sayfa_var_mi(baglanti, url):
    """
    Verilen URL'nin Pages tablosunda bulunup bulunmadığını kontrol eder.

    Böylece program tekrar çalıştırıldığında aynı sayfa için
    yeni bir kayıt oluşturulmaz. Mevcut kayıt güncellenir.
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
    Pages tablosuna yeni bir sayfa kaydı ekler.
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
    URL'ye ait mevcut Pages kaydını günceller.

    Scraping işlemi tekrar çalıştırıldığında güncel veriler
    aynı kayıt üzerine yazılır.
    """

    cursor = baglanti.cursor()

    try:
        cursor.execute(
            """
            UPDATE dbo.Pages
            SET
                Title = ?,
                Content = ?,
                Category = ?,
                Keywords = ?
            WHERE Url = ?
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