from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def sekmeye_tikla(driver, sekme_adi):
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

        sleep(3)

        return True

    except Exception:
        print(f"{sekme_adi} sekmesine tıklanamadı.")
        return False
    

HATA_MESAJLARI = [
    "bu bölüm yüklenirken bir sorun oluştu",
    "sunucu yanıt veremedi",
    "bağlantı kesildi",
    "sayfa bulunamadı",
    "bir hata oluştu",
]


def driver_olustur():
    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(40)
    return driver


def sayfanin_yuklenmesini_bekle(
    driver,
    selector=None,
    bekleme_suresi=15
):
    wait = WebDriverWait(
        driver,
        bekleme_suresi
    )

    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    if selector:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, selector)
            )
        )


def sayfayi_kademeli_kaydir(
    driver,
    kaydirma_sayisi=4,
    bekleme_suresi=1
):
    """
    Sayfayı sınırlı sayıda aşağı kaydırır.

    Sonsuz liste veya çok uzun tabloların
    tamamının yüklenmesini engeller.
    """

    for _ in range(kaydirma_sayisi):
        driver.execute_script(
            """
            window.scrollBy({
                top: window.innerHeight * 0.85,
                behavior: 'smooth'
            });
            """
        )

        sleep(bekleme_suresi)

    driver.execute_script(
        "window.scrollTo(0, 0);"
    )

    sleep(0.5)


def icerik_elementini_bul(
    driver,
    content_selector=None
):
    """
    Sayfanın ana içerik alanını bulmaya çalışır.
    """

    selectorlar = []

    if content_selector:
        selectorlar.append(content_selector)

    selectorlar.extend([
        "main",
        '[role="main"]',
        "article",
        "#main-content",
        ".main-content",
        ".page-content",
        ".content",
    ])

    for selector in selectorlar:
        try:
            element = driver.find_element(
                By.CSS_SELECTOR,
                selector
            )

            metin = element.text.strip()

            if len(metin) >= 50:
                return element, selector

        except Exception:
            continue

    return (
        driver.find_element(
            By.TAG_NAME,
            "body"
        ),
        "body"
    )


def temiz_metni_al(driver, element):
    """
    Ana içerik içerisindeki anlamlı metinleri
    satır satır toplar.

    Menü, reklam, modal, footer ve benzeri
    gereksiz alanları mümkün olduğunca çıkarır.
    """

    metin_satirlari = driver.execute_script(
        """
        const original = arguments[0];
        const clone = original.cloneNode(true);

        const removeSelectors = [
            'script',
            'style',
            'noscript',
            'svg',
            'canvas',

            'nav',
            'header',
            'footer',
            'aside',

            '[role="dialog"]',
            '[aria-modal="true"]',

            '.modal',
            '.popup',
            '.popover',
            '.tooltip',

            '.advertisement',
            '.advert',
            '.ads',
            '.banner',

            '.cookie',
            '.cookie-banner',

            '.pagination',
            '.breadcrumb',

            '.navbar',
            '.header',
            '.footer',
            '.sidebar'
        ];

        removeSelectors.forEach(selector => {
            clone.querySelectorAll(selector).forEach(
                node => node.remove()
            );
        });

        const blockSelectors = [
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'p',
            'li',
            'label',
            'th',
            'td',
            'article',
            'section',
            '[role="heading"]',
            '[role="cell"]',
            '[role="columnheader"]',
            '[role="rowheader"]'
        ];

        const blockSelectorText = blockSelectors.join(',');

        const elements = clone.querySelectorAll(
            blockSelectorText
        );

        const lines = [];
        const seen = new Set();

        elements.forEach(element => {
            /*
            İçinde başka bir anlamlı blok bulunan üst kapsayıcıyı
            ayrıca alma. Böylece aynı metin iki kez kaydedilmez.
            */
            const childBlock = element.querySelector(
                blockSelectorText
            );

            if (childBlock) {
                return;
            }

            const text = (
                element.innerText ||
                element.textContent ||
                ''
            )
                .replace(/\\s+/g, ' ')
                .trim();

            if (!text) {
                return;
            }

            if (text.length < 2) {
                return;
            }

            if (seen.has(text)) {
                return;
            }

            seen.add(text);
            lines.push(text);
        });

        /*
        Sayfada uygun blok bulunamazsa genel metni
        satırlara ayırarak döndür.
        */
        if (lines.length === 0) {
            return (
                clone.innerText ||
                clone.textContent ||
                ''
            )
                .split('\\n')
                .map(text => {
                    return text
                        .replace(/\\s+/g, ' ')
                        .trim();
                })
                .filter(text => text.length >= 2);
        }

        return lines;
        """,
        element
    )

    if not metin_satirlari:
        return ""

    return "\n".join(metin_satirlari)


def hata_mesaji_var_mi(text):
    kucuk_metin = text.lower()

    return any(
        hata_mesaji in kucuk_metin
        for hata_mesaji in HATA_MESAJLARI
    )


def sayfayi_tara(
    driver,
    page,
    wait_seconds=3,
    retry_count=2
):
    title = page["title"]
    url = page["url"]
    category = page["category"]

    content_selector = page.get(
        "content_selector"
    )

    wait_for = page.get(
        "wait_for"
    )

    scroll_count = page.get(
        "scroll_count",
        4
    )

    print(f"\nSayfa açılıyor: {title}")
    print(f"URL: {url}")

    son_hata = None

    toplam_deneme = retry_count + 1

    for deneme in range(
        1,
        toplam_deneme + 1
    ):
        try:
            driver.get(url)

            sayfanin_yuklenmesini_bekle(
                driver=driver,
                selector=wait_for,
                bekleme_suresi=15
            )

            sleep(wait_seconds)
            if category == "Sektörel Görünüm":
                sekmeye_tikla(driver, "Haftalık")

            sayfayi_kademeli_kaydir(
                driver=driver,
                kaydirma_sayisi=scroll_count
            )

            (
                content_element,
                kullanilan_selector
            ) = icerik_elementini_bul(
                driver=driver,
                content_selector=content_selector
            )

            raw_text = temiz_metni_al(
                driver=driver,
                element=content_element
            )

            page_title = driver.title.strip()

            if hata_mesaji_var_mi(raw_text):
                raise RuntimeError(
                    "Sayfada sunucu veya içerik "
                    "yükleme hatası tespit edildi."
                )

            if len(raw_text) < 20:
                return {
                    "title": title,
                    "page_title": page_title,
                    "url": url,
                    "category": category,
                    "raw_text": raw_text,
                    "content_selector": kullanilan_selector,
                    "content_available": False,
                    "scrape_status": "empty",
                    "error_message": None
                }

            return {
                "title": title,
                "page_title": page_title,
                "url": url,
                "category": category,
                "raw_text": raw_text,
                "content_selector": kullanilan_selector,
                "content_available": True,
                "scrape_status": "success",
                "error_message": None
            }

        except (
            TimeoutException,
            RuntimeError,
            Exception
        ) as error:
            son_hata = str(error)

            print(
                f"Deneme başarısız "
                f"({deneme}/{toplam_deneme}): "
                f"{son_hata}"
            )

            if deneme < toplam_deneme:
                sleep(3)

                try:
                    driver.refresh()
                    sleep(2)
                except Exception:
                    pass

    return {
        "title": title,
        "page_title": driver.title.strip(),
        "url": url,
        "category": category,
        "raw_text": "",
        "content_selector": content_selector,
        "content_available": False,
        "scrape_status": "failed",
        "error_message": son_hata
    }


def uygulamayi_tara(config):
    driver = driver_olustur()
    results = []

    try:
        for page in config["pages"]:
            try:
                result = sayfayi_tara(
                    driver=driver,
                    page=page,
                    wait_seconds=page.get(
                        "wait_seconds",
                        3
                    ),
                    retry_count=page.get(
                        "retry_count",
                        2
                    )
                )

                results.append(result)

                print(
                    f"Durum: "
                    f"{result['scrape_status']} | "
                    f"{page['title']} | "
                    f"{len(result['raw_text'])} karakter | "
                    f"Alan: "
                    f"{result['content_selector']}"
                )

            except Exception as error:
                print(
                    f"Sayfa taranamadı: "
                    f"{page['title']}"
                )

                print(error)

                results.append({
                    "title": page["title"],
                    "page_title": "",
                    "url": page["url"],
                    "category": page["category"],
                    "raw_text": "",
                    "content_selector": None,
                    "content_available": False,
                    "scrape_status": "failed",
                    "error_message": str(error)
                })

    finally:
        driver.quit()

    return results
def sayfayi_indir(url, kategori):
    """
    Mevcut main.py ile uyumluluk için eklendi.
    """

    driver = driver_olustur()

    try:
        page = {
            "title": kategori,
            "url": url,
            "category": kategori
        }

        return sayfayi_tara(
            driver=driver,
            page=page
        )

    finally:
        driver.quit()