"""
Hybrid Search

Keyword + Embedding Search

Kişi 2
"""

import re
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from openai import OpenAI
from dotenv import load_dotenv

import os

from database import keyword_ara
from rag.embedding_service import (
    embeddingleri_yukle,
    embedding_olustur
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ---------------------------------------------------
# Türkçe normalize
# ---------------------------------------------------

def normalize(text):

    text = text.lower()

    text = text.replace("ı", "i")
    text = text.replace("ğ", "g")
    text = text.replace("ü", "u")
    text = text.replace("ş", "s")
    text = text.replace("ö", "o")
    text = text.replace("ç", "c")

    text = re.sub(r"[^\w\s]", " ", text)

    return text


# ---------------------------------------------------
# Keyword Score
# ---------------------------------------------------

def keyword_score(question):

    sonuc = {}

    kelimeler = normalize(question).split()

    for kelime in kelimeler:

        pages = keyword_ara(kelime)

        for page in pages:

            pid = page["id"]

            if pid not in sonuc:

                sonuc[pid] = 0

            sonuc[pid] += 1

            if kelime in normalize(page["title"]):

                sonuc[pid] += 3

            if kelime in normalize(page["category"]):

                sonuc[pid] += 2

    return sonuc


# ---------------------------------------------------
# Embedding Search
# ---------------------------------------------------

def embedding_score(question):

    query_embedding = embedding_olustur(question)

    embeddings = embeddingleri_yukle()

    skorlar = {}

    for pid, page in embeddings.items():

        score = cosine_similarity(

            np.array(query_embedding).reshape(1, -1),

            np.array(page["embedding"]).reshape(1, -1)

        )[0][0]

        skorlar[pid] = score

    return skorlar


# ---------------------------------------------------
# Hybrid
# ---------------------------------------------------

def hybrid_search(question):

    keyword = keyword_score(question)

    semantic = embedding_score(question)

    embeddings = embeddingleri_yukle()

    final = []

    for pid, page in embeddings.items():

        semantic_score = semantic.get(pid, 0)

        keyword_bonus = keyword.get(pid, 0)

        score = (
            semantic_score * 0.75
            +
            keyword_bonus * 0.25
        )

        final.append({

            "id": pid,

            "title": page["title"],

            "url": page["url"],

            "category": page["category"],

            "score": score

        })

    final.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return final


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    soru = input("Soru : ")

    sonuc = hybrid_search(soru)

    print()

    for i in sonuc[:5]:

        print(i)