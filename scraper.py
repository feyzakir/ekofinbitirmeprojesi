# scraper.py

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import HEADERS


def tarayici_olustur():
    """
    Arka planda çalışan Chrome tarayıcısı oluşturur.
    """

    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument(
        f"--user-agent={HEADERS['User-Agent']}"
    )

    return webdriver.Chrome(options=options)


def sekmeye_tikla(driver, sekme_adi):
    """
    Sayfa içindeki Günlük, Haftalık veya Aylık sekmesine tıklar.
    """

    try:
        sekme = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//*[normalize-space()='{sekme_adi}']"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            sekme
        )

        time.sleep(4)

        return True

    except Exception:
        print(
            f"  [UYARI] '{sekme_adi}' sekmesine tıklanamadı."
        )
        return False


def sayfayi_kademeli_kaydir(driver):
    """
    Lazy loading ile gelen alanların yüklenmesi için
    sayfayı kademeli olarak aşağı kaydırır.
    """

    sayfa_yuksekligi = driver.execute_script(
        "return document.body.scrollHeight"
    )

    mevcut_konum = 0
    kaydirma_miktari = 700

    while mevcut_konum < sayfa_yuksekligi:
        driver.execute_script(
            f"window.scrollTo(0, {mevcut_konum});"
        )

        time.sleep(0.35)

        mevcut_konum += kaydirma_miktari

        yeni_yukseklik = driver.execute_script(
            "return document.body.scrollHeight"
        )

        if yeni_yukseklik > sayfa_yuksekligi:
            sayfa_yuksekligi = yeni_yukseklik

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )

    time.sleep(2)

    driver.execute_script(
        "window.scrollTo(0, 0);"
    )

    time.sleep(1)


def selenium_ile_indir(url, kategori):
    """
    Sayfayı JavaScript çalışmış hâliyle indirir.

    Sonuç:
    {
        "html": "...",
        "gorunen_metin": "...",
        "period": "weekly" veya "daily"
    }
    """

    driver = None

    try:
        driver = tarayici_olustur()

        driver.set_page_load_timeout(60)
        driver.get(url)

        WebDriverWait(driver, 60).until(
            lambda tarayici: tarayici.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        time.sleep(6)

        period = None

        # Mentörün testinde "Bu hafta sektörel görünüm nasıl?"
        # sorulduğu için haftalık veri çekilir.
        if kategori == "Sektörel Görünüm":
            if sekmeye_tikla(driver, "Haftalık"):
                period = "weekly"
            else:
                period = "daily"

        elif kategori == "Teknik Görünüm":
            period = "daily"

        elif kategori == "Genel Trend Özeti":
            period = "daily"

        sayfayi_kademeli_kaydir(driver)

        body = driver.find_element(
            By.TAG_NAME,
            "body"
        )

        gorunen_metin = body.get_attribute(
            "innerText"
        )

        if not gorunen_metin:
            print(
                "  [HATA] Görünür sayfa metni alınamadı."
            )
            return None

        return {
            "html": driver.page_source,
            "gorunen_metin": gorunen_metin,
            "period": period
        }

    except Exception as hata:
        print(
            f"  [HATA] Selenium ile sayfa alınamadı: {url}"
        )
        print(f"  Detay: {hata}")

        return None

    finally:
        if driver is not None:
            driver.quit()


def sayfayi_indir(url, kategori):
    """
    main.py tarafından çağrılan ana fonksiyon.
    """

    print(
        "  Dinamik içerik Selenium ile yükleniyor..."
    )

    return selenium_ile_indir(
        url,
        kategori
    )