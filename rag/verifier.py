"""
verifier.py

Hibrit doğrulama katmanı:
    - hizli_dogrulama(): String tabanlı hızlı kontrol (Katman 2.5)
    - dogrula(): LLM-as-Judge doğrulama (Katman 3)
"""
import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

JUDGE_MODEL = "gpt-5-nano"

# ==========================================
# KATMAN 3 - LLM as Judge
# ==========================================

SYSTEM_PROMPT = """Sen bir cevap doğrulayıcısısın. Cevaptaki iddialar kaynaklarda destekleniyor mu?

Kurallar:
- "bulunamadı", "bilgi yok" gibi RED cevabı → grounded=true, score=1.0
- Kaynakta olmayan iddia → grounded=false
- Kaynakla çelişme → grounded=false
- Tablo sütun-değer karışıklığı → grounded=false

SADECE bu JSON'u dön: {"grounded": true/false, "score": 0.0-1.0, "gerekce": "kısa"}"""


def _kaynaklari_formatla(pages, max_chars=1500):
    text = ""
    for i, p in enumerate(pages, 1):
        content = str(p.get("content", ""))[:max_chars]
        text += f"\n[KAYNAK {i}] {p.get('title', '')}\n{content}\n"
    return text


def dogrula(soru, cevap, pages):
    """Katman 3: Judge LLM ile derinlemesine doğrulama"""
    kaynak_metni = _kaynaklari_formatla(pages)
    user_prompt = f"Soru: {soru}\n\nCevap: {cevap}\n\nKaynaklar:{kaynak_metni}"

    try:
        response = client.chat.completions.create(
            model=JUDGE_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=150
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "grounded": False,
            "score": 0.0,
            "gerekce": f"Doğrulayıcı hata: {e}"
        }


# ==========================================
# KATMAN 2.5 - Hızlı String Doğrulama
# ==========================================

# Türkçe stopwords - anlamsız yaygın kelimeler (kontrol dışı bırakılır)
TR_STOPWORDS = {
    "bir", "bu", "şu", "ve", "ile", "için", "olarak", "gibi", "her",
    "hangi", "kaç", "ama", "veya", "eğer", "sonra", "önce", "içinde",
    "arasında", "aynı", "farklı", "başka", "diğer", "bazı", "tüm", "hiç",
    "çok", "önemli", "gerekli", "olan", "olur", "eder", "yapar", "olabilir",
    "bulunur", "vardır", "biri", "birçok", "ise", "hem", "yani", "kadar",
    "üzere", "sadece", "ancak", "fakat", "böyle", "şöyle", "öyle", "işte",
    "ilgili", "durum", "bilgi", "bilgiler", "içeriyor", "içerir", "içermez",
    "içeren", "genel", "detaylı", "kısa", "buna", "şuna", "ona", "burada",
    "sayfa", "sayfası", "sayfanın", "linki", "ilişkin", "üzerinden",
    "ayrıca", "not", "url"
}

# Negasyon pattern'leri - varsa hızlı doğrulama güvensizdir, judge'a gönderilir
NEGASYON_PATTERNS = [
    r'\byok\b', r'\byoktur\b', r'\bdeğil',
    r'\bolmayan\b', r'\bbulunmuyor', r'\bbulunmamak', r'\bbulunmaz',
    r'mevcut değil', r'yer almamakta', r'yer almıyor', r'listelenmi',
]


def _negasyon_var_mi(cevap):
    """Cevapta olumsuzluk ifadesi var mı?"""
    cevap_lower = cevap.lower()
    return any(re.search(p, cevap_lower) for p in NEGASYON_PATTERNS)


def _terimleri_cikart(metin):
    """Cevaptan anahtar terimleri çıkar: URL, kelime öbeği, anlamlı kelime"""
    # URL'leri çıkar
    urls = re.findall(r'https?://\S+', metin)
    urls = [u.rstrip('.,;:!?)\]}"') for u in urls]

    # URL'leri metinden temizle
    metin_url_yok = re.sub(r'https?://\S+', '', metin)

    # Büyük harfle başlayan 2-4 kelimelik öbekler
    # Örnek: "Orta Vadeli Takip Listesi", "Analist Tahminleri"
    obek_pattern = r'\b([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})\b'
    obekler = re.findall(obek_pattern, metin_url_yok)

    # Anlamlı kelimeler (4+ harf, stopword değil)
    kelimeler = re.findall(r'\b[a-zçğıöşüA-ZÇĞİÖŞÜ]{4,}\b', metin_url_yok)
    kelimeler = [k.lower() for k in kelimeler if k.lower() not in TR_STOPWORDS]

    return {
        "urls": list(set(urls)),
        "obekler": list(set(obekler)),
        "kelimeler": list(set(kelimeler))
    }


def hizli_dogrulama(cevap, pages):
    """
    Katman 2.5: String tabanlı hızlı doğrulama.

    Cevaptaki URL, özel isim ve anlamlı kelimelerin
    kaynak sayfalarda gerçekten geçip geçmediğini kontrol eder.

    Return: (skor 0.0-1.0, detay dict)
    """
    # Negasyon kontrolü - varsa güvensiz
    if _negasyon_var_mi(cevap):
        return 0.0, {"sebep": "negasyon_tespit_edildi"}

    # Kaynak metnini birleştir
    kaynak_metni = ""
    for p in pages:
        kaynak_metni += " " + str(p.get("content", ""))
        kaynak_metni += " " + str(p.get("title", ""))
        kaynak_metni += " " + str(p.get("url", ""))
    kaynak_lower = kaynak_metni.lower()

    # Terimleri çıkar
    terimler = _terimleri_cikart(cevap)

    puanlar = {}
    agirliklar = {}

    # URL doğrulama (en güvenilir kanıt)
    if terimler["urls"]:
        eslesen = sum(1 for u in terimler["urls"] if u in kaynak_metni)
        puanlar["url"] = eslesen / len(terimler["urls"])
        agirliklar["url"] = 0.4

    # Öbek doğrulama (özel isim / sayfa adı)
    if terimler["obekler"]:
        eslesen = sum(1 for o in terimler["obekler"] if o.lower() in kaynak_lower)
        puanlar["obek"] = eslesen / len(terimler["obekler"])
        agirliklar["obek"] = 0.35

    # Kelime doğrulama (genel içerik uyumu)
    if terimler["kelimeler"]:
        eslesen = sum(1 for k in terimler["kelimeler"] if k in kaynak_lower)
        puanlar["kelime"] = eslesen / len(terimler["kelimeler"])
        agirliklar["kelime"] = 0.25

    if not agirliklar:
        return 0.0, {"sebep": "terim_bulunamadi"}

    # Ağırlıklı ortalama - eksik kategoriler ağırlıkları normalize et
    toplam_agirlik = sum(agirliklar.values())
    toplam_skor = sum(
        puanlar[k] * agirliklar[k] / toplam_agirlik
        for k in puanlar
    )

    return toplam_skor, {
        "puanlar": {k: round(v, 2) for k, v in puanlar.items()},
        "toplam": round(toplam_skor, 2),
        "url_sayisi": len(terimler["urls"]),
        "obek_sayisi": len(terimler["obekler"]),
        "kelime_sayisi": len(terimler["kelimeler"])
    }
