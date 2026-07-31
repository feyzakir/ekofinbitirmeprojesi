"""
verifier.py

LLM-as-judge doğrulama katmanı.
Üretilen cevap, RAG kaynaklarıyla uyuşuyor mu kontrol eder.
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

JUDGE_MODEL = "gpt-5-nano"

SYSTEM_PROMPT = """
Sen bir cevap doğrulayıcısısın.

Görevin: Verilen "cevap" içindeki her iddianın "kaynaklar"
tarafından desteklenip desteklenmediğini kontrol etmek.

Kurallar:
- Cevap kaynaklarda yoksa veya çelişiyorsa: grounded=false
- Cevap "Bilgi bulunamadı" gibi dürüst bir red ise: grounded=true
- Kısmen destekleniyorsa: grounded=true ama score düşük olur
- Skor 0.0 - 1.0 arası

SADECE şu JSON formatında dön, başka hiçbir şey yazma:
{
  "grounded": true veya false,
  "score": 0.0 ile 1.0 arası,
  "gerekce": "kısa açıklama",
  "desteklenmeyen_iddialar": ["...", "..."]
}
"""


def _kaynaklari_formatla(pages, max_chars=3000):
    text = ""
    for i, p in enumerate(pages, 1):
        content = str(p.get("content", ""))[:max_chars]
        text += f"\n--- KAYNAK {i} ---\n"
        text += f"Başlık: {p.get('title', '')}\n"
        text += f"URL: {p.get('url', '')}\n"
        text += f"İçerik: {content}\n"
    return text


def dogrula(soru, cevap, pages):
    """
    Cevabın kaynaklarla uyumunu kontrol eder.
    """
    kaynak_metni = _kaynaklari_formatla(pages)

    user_prompt = f"""
Soru:
{soru}

Üretilen Cevap:
{cevap}

Kaynaklar:
{kaynak_metni}

Cevabı değerlendir ve SADECE JSON dön.
"""

    try:
        response = client.chat.completions.create(
            model=JUDGE_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content
        return json.loads(raw)

    except Exception as e:
        # Hata olursa güvenli tarafta kal
        return {
            "grounded": False,
            "score": 0.0,
            "gerekce": f"Doğrulayıcı hata: {e}",
            "desteklenmeyen_iddialar": []
        }