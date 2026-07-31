
from rag.verifier import dogrula
"""
llm.py

LLM katmanı

Hybrid Search -> Prompt -> GPT
"""
from google import genai
import os
from dotenv import load_dotenv
from openai import OpenAI
from rag.hybrid_search import hybrid_search
from rag.embedding_service import embeddingleri_yukle
from rag.prompt import build_prompt
from rag.verifier import dogrula
from database import (
    mesajlari_getir,
    mesaj_ekle
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-5-nano"


def cevap_uret(session_id, soru, top_k=3):

    history = mesajlari_getir(session_id)

    arama_sonuclari = hybrid_search(soru)

    embeddings = embeddingleri_yukle()

    pages = []

    for sonuc in arama_sonuclari[:top_k]:

        pid = sonuc["id"]

        if pid in embeddings:
            pages.append(embeddings[pid])

    system_prompt, user_prompt = build_prompt(
        soru,
        pages,
        history
    )

    response = client.chat.completions.create(

        model=MODEL,


        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    cevap = response.choices[0].message.content


 # --- Doğrulama katmanı ---
    dogrulama_sonucu = dogrula(soru, cevap, pages)
    print("[DOĞRULAMA]", dogrulama_sonucu)  # test için

    # Güvenli erişim - hatalı JSON gelmesine karşı
    grounded = dogrulama_sonucu.get("grounded", False)
    score = dogrulama_sonucu.get("score", 0.0)

    # String gelirse boolean'a çevir
    if isinstance(grounded, str):
        grounded = grounded.lower() == "true"

    # Score sayı değilse 0.0 kabul et
    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0.0

    if not grounded or score < 0.6:
        cevap = (
            "Bu konuya ilişkin veritabanında güvenilir bilgi "
            "bulunamadı. Lütfen soruyu farklı ifade edin."
        )

    mesaj_ekle(
        session_id,
        "user",
        soru
    )

    mesaj_ekle(
        session_id,
        "assistant",
        cevap
    )

    return cevap



