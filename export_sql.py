# export_sql.py

from pathlib import Path

import pyodbc

from config import DB_CONFIG


TABLO_ADI = "dbo.Pages"
CIKTI_DOSYASI = "Pages_Table.sql"


def sql_unicode_deger(deger):
    """
    Python değerini güvenli SQL metnine dönüştürür.

    None      -> NULL
    metin     -> N'metin'
    tek tırnak -> iki tek tırnak
    """

    if deger is None:
        return "NULL"

    metin = str(deger)

    # SQL içindeki tek tırnakları kaçır.
    metin = metin.replace("'", "''")

    return f"N'{metin}'"


def pages_verilerini_oku(baglanti):
    """
    Pages tablosundaki bütün kayıtları Id sırasıyla okur.
    """

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
            ORDER BY Id;
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()


def tablo_olusturma_betigi():
    """
    Pages tablosunun oluşturulma SQL betiğini döndürür.
    """

    return """USE [finalcase];
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

"""


def insert_betigi_olustur(kayit):
    """
    Tek bir Pages kaydı için INSERT komutu oluşturur.
    """

    (
        id_degeri,
        title,
        url,
        content,
        category,
        keywords
    ) = kayit

    return f"""INSERT INTO dbo.Pages
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
    {id_degeri},
    {sql_unicode_deger(title)},
    {sql_unicode_deger(url)},
    {sql_unicode_deger(content)},
    {sql_unicode_deger(category)},
    {sql_unicode_deger(keywords)}
);
GO

"""


def kapanis_betigi():
    """
    Identity insert işlemini kapatır ve doğrulama sorgusu ekler.
    """

    return """SET IDENTITY_INSERT dbo.Pages OFF;
GO

SELECT
    Id,
    Title,
    Category,
    ISJSON(Content) AS JsonGecerliMi
FROM dbo.Pages
ORDER BY Id;
GO
"""


def main():
    baglanti = None

    try:
        print("SQL Server bağlantısı kuruluyor...")

        baglanti = pyodbc.connect(DB_CONFIG)

        print("Bağlantı başarılı.")

        kayitlar = pages_verilerini_oku(
            baglanti
        )

        if not kayitlar:
            print(
                "Pages tablosunda aktarılacak kayıt bulunamadı."
            )
            return

        proje_klasoru = Path(__file__).resolve().parent
        cikti_yolu = proje_klasoru / CIKTI_DOSYASI

        with open(
            cikti_yolu,
            "w",
            encoding="utf-8-sig",
            newline="\n"
        ) as dosya:

            dosya.write(
                tablo_olusturma_betigi()
            )

            for kayit in kayitlar:
                dosya.write(
                    insert_betigi_olustur(
                        kayit
                    )
                )

            dosya.write(
                kapanis_betigi()
            )

        print(
            f"{len(kayitlar)} kayıt başarıyla aktarıldı."
        )

        print(
            f"Dosya oluşturuldu:\n{cikti_yolu}"
        )

    except pyodbc.Error as hata:
        print(
            "SQL Server işlemi sırasında hata oluştu:"
        )
        print(hata)

    except OSError as hata:
        print(
            "Dosya oluşturulurken hata oluştu:"
        )
        print(hata)

    except Exception as hata:
        print(
            "Beklenmeyen bir hata oluştu:"
        )
        print(hata)

    finally:
        if baglanti is not None:
            baglanti.close()
            print("SQL Server bağlantısı kapatıldı.")


if __name__ == "__main__":
    main()