"""
llm.py

LLM katmanı - 4 Katmanlı Hibrit Doğrulama

Katman 1: Alaka kontrolü  (konu dışı sorular LLM'e gitmeden reddedilir)
Katman 2: Dürüst red tanıma  (LLM zaten "bilmiyorum" dediyse geç)
Katman 2.5: Hızlı string doğrulama  (kaynak eşleşmesi yeterse judge atlanır)
Katman 3: Judge LLM doğrulama  (halüsinasyon kontrolü)
"""
from google import genai
import os
from dotenv import load_dotenv
from openai import OpenAI
from rag.hybrid_search import hybrid_search
from rag.embedding_service import embeddingleri_yukle
from rag.prompt import build_prompt
from rag.verifier import dogrula, hizli_dogrulama
from database import mesajlari_getir, mesaj_ekle

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5-nano"

# ==========================================
# EŞİKLER
# ==========================================
ALAKA_ESIGI = 0.15            # Katman 1: Bunun ALTI konu dışı
HIZLI_DOGRULAMA_ESIGI = 0.7   # Katman 2.5: Bunun ÜSTÜ hızlı doğrulandı, judge atlanır
DOGRULAMA_ESIGI = 0.6         # Katman 3: Bunun ALTI reddedilir


def cevap_uret(session_id, soru, top_k=3):
    history = mesajlari_getir(session_id)
    arama_sonuclari = hybrid_search(soru)
    embeddings = embeddingleri_yukle()

    pages = []
    for sonuc in arama_sonuclari[:top_k]:
        pid = sonuc["id"]
        if pid in embeddings:
            pages.append(embeddings[pid])

    # ============================================
    # KATMAN 1: Alaka kontrolü
    # ============================================
    en_yuksek_skor = arama_sonuclari[0]["score"] if arama_sonuclari else 0

    if en_yuksek_skor < ALAKA_ESIGI:
        print(f"[KATMAN 1 - ALAKA REDDİ] Skor: {en_yuksek_skor:.3f}")
        cevap = (
            "Bu asistan yalnızca Ekofin Piyasa Görünümü içerikleri "
            "hakkında bilgi verir. Sorunuz kapsam dışı görünüyor. "
            "Lütfen Ekofin ile ilgili bir soru sorun."
        )
        mesaj_ekle(session_id, "user", soru)
        mesaj_ekle(session_id, "assistant", cevap)
        return cevap

    # ============================================
    # LLM cevap üretimi
    # ============================================
    system_prompt, user_prompt = build_prompt(soru, pages, history)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    cevap = response.choices[0].message.content

    # ============================================
    # KATMAN 2: Dürüst red tanıma
    # ============================================
    red_ifadeleri = [
        "bulunamadı", "bilgi yok", "kaynakta yok",
        "veri bulunmuyor", "bilgi bulunmuyor",
        "mevcut değil", "bilgim yok"
    ]
    cevap_lower = cevap.lower()

    if any(ifade in cevap_lower for ifade in red_ifadeleri):
        print("[KATMAN 2 - DÜRÜST RED] Doğrulama atlandı")
    else:
        # ============================================
        # KATMAN 2.5: Hızlı String Doğrulama
        # ============================================
        hizli_skor, hizli_detay = hizli_dogrulama(cevap, pages)
        print(f"[KATMAN 2.5 - HIZLI DOĞRULAMA] Skor: {hizli_skor:.2f} | {hizli_detay}")

        if hizli_skor >= HIZLI_DOGRULAMA_ESIGI:
            print(f"[KATMAN 2.5 - DOĞRULANDI] Judge atlandı ✓")
        else:
            # ============================================
            # KATMAN 3: Judge doğrulama (LLM-as-Judge)
            # ============================================
            dogrulama_sonucu = dogrula(soru, cevap, pages)
            print("[KATMAN 3 - JUDGE DOĞRULAMA]", dogrulama_sonucu)

            grounded = dogrulama_sonucu.get("grounded", False)
            score = dogrulama_sonucu.get("score", 0.0)

            # Güvenli tip dönüşümü
            if isinstance(grounded, str):
                grounded = grounded.lower() == "true"
            try:
                score = float(score)
            except (TypeError, ValueError):
                score = 0.0

            if not grounded or score < DOGRULAMA_ESIGI:
                cevap = (
                    "Bu konuya ilişkin veritabanında güvenilir bilgi "
                    "bulunamadı. Lütfen soruyu farklı ifade edin."
                )

    mesaj_ekle(session_id, "user", soru)
    mesaj_ekle(session_id, "assistant", cevap)
    return cevap
