# parser.py


def sayfayi_parse_et(scrape_sonucu):
    """
    Selenium sonucunu ortak biçime dönüştürür.
    """

    if not scrape_sonucu:
        return {
            "ham_metin": "",
            "period": None
        }

    if isinstance(scrape_sonucu, str):
        return {
            "ham_metin": scrape_sonucu,
            "period": None
        }

    if not isinstance(scrape_sonucu, dict):
        return {
            "ham_metin": str(scrape_sonucu),
            "period": None
        }

    return {
        "ham_metin": scrape_sonucu.get(
            "raw_text",
            ""
        ),
        "period": scrape_sonucu.get(
            "period"
        )
    }