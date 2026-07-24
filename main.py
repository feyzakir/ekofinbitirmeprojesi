# main.py

import json

from config import SAYFALAR

from database import (
    baglanti_olustur,
    sayfa_var_mi,
    sayfa_ekle,
    sayfa_guncelle
)

from scraper import sayfayi_indir
from parser import sayfayi_parse_et

from normalizer import (
    icerigi_yapilandir,
    anahtar_kelime_uret
)


def json_icerik_olustur(
    kategori,
    url,
    keywords,
    structured_content
):
    """
    SQL Content alanına kaydedilecek JSON metnini oluşturur.
    """

    veri = {
        "page": kategori,
        "url": url,
        "keywords": keywords,
        "content": structured_content
    }

    return json.dumps(
        veri,
        ensure_ascii=False,
        indent=2
    )


def main():
    baglanti = None

    try:
        print(
            "SQL Server bağlantısı kuruluyor..."
        )

        baglanti = baglanti_olustur()

        print(
            "SQL Server bağlantısı başarılı."
        )
        print("-" * 60)

        for sira, sayfa in enumerate(
            SAYFALAR,
            start=1
        ):
            kategori = sayfa["category"]
            url = sayfa["url"]

            print(
                f"[{sira}/{len(SAYFALAR)}] "
                f"{kategori} işleniyor..."
            )

            scrape_sonucu = sayfayi_indir(
                url,
                kategori
            )

            if scrape_sonucu is None:
                print(
                    "  Sayfa indirilemedi, atlandı."
                )
                print("-" * 60)
                continue

            parse_sonucu = sayfayi_parse_et(
                scrape_sonucu
            )

            ham_metin = parse_sonucu.get(
                "ham_metin",
                ""
            )

            period = parse_sonucu.get(
                "period"
            )

            structured_content = icerigi_yapilandir(
                ham_metin=ham_metin,
                kategori=kategori,
                period=period
            )

            if not structured_content:
                print(
                    "  Yapılandırılmış içerik "
                    "oluşturulamadı."
                )
                print("-" * 60)
                continue

            keywords_listesi = anahtar_kelime_uret(
                kategori
            )

            json_content = json_icerik_olustur(
                kategori=kategori,
                url=url,
                keywords=keywords_listesi,
                structured_content=structured_content
            )

            keywords_sql = ", ".join(
                keywords_listesi
            )

            print("  JSON önizlemesi:")
            print(json_content[:900])

            if len(json_content) > 900:
                print("  ...")

            if sayfa_var_mi(
                baglanti,
                url
            ):
                sayfa_guncelle(
                    baglanti=baglanti,
                    url=url,
                    title=kategori,
                    content=json_content,
                    category=kategori,
                    keywords=keywords_sql
                )

                print(
                    "  Mevcut kayıt güncellendi."
                )

            else:
                sayfa_ekle(
                    baglanti=baglanti,
                    title=kategori,
                    url=url,
                    content=json_content,
                    category=kategori,
                    keywords=keywords_sql
                )

                print(
                    "  Yeni kayıt eklendi."
                )

            print(
                f"  JSON uzunluğu: "
                f"{len(json_content)} karakter"
            )

            print("-" * 60)

        print("Tüm sayfalar işlendi.")

    except Exception as hata:
        print(
            "\nProgram çalışırken hata oluştu:"
        )
        print(hata)

    finally:
        if baglanti is not None:
            baglanti.close()

            print(
                "SQL Server bağlantısı kapatıldı."
            )


if __name__ == "__main__":
    main()