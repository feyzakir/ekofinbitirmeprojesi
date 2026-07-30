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
from database import (
    mesajlari_getir,
    mesaj_ekle
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4.1"


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

        temperature=0.2,

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



