"""
embedding_service.py

Pages tablosundaki içerikleri embedding'e dönüştürür
ve diskte cache olarak saklar.

Kişi 2 - RAG Katmanı
"""
import os
import pickle
import hashlib
from dotenv import load_dotenv
from openai import OpenAI

from database import tum_sayfalari_getir

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"

CACHE_PATH = "rag/embeddings.pkl"


def metin_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sayfa_metni(page):
    """
    Embedding üretilecek metin.
    """

    return f"""
Başlık:
{page['title']}

Kategori:
{page['category']}

Anahtar Kelimeler:
{page['keywords']}

İçerik:
{page['content']}
"""


def embedding_olustur(text):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def cache_yukle():

    if os.path.exists(CACHE_PATH):

        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)

    return {}


def cache_kaydet(cache):

    with open(CACHE_PATH, "wb") as f:
        pickle.dump(cache, f)


def embedding_index_olustur():

    pages = tum_sayfalari_getir()

    eski_cache = cache_yukle()

    yeni_cache = {}

    print(f"{len(pages)} sayfa bulundu.\n")

    for page in pages:

        pid = page["id"]

        text = sayfa_metni(page)

        current_hash = metin_hash(text)

        if (
            pid in eski_cache and
            eski_cache[pid]["hash"] == current_hash
        ):

            print(f"✓ Cache kullanıldı -> {page['title']}")

            yeni_cache[pid] = eski_cache[pid]

            continue

        print(f"Embedding oluşturuluyor -> {page['title']}")

        embedding = embedding_olustur(text)

        yeni_cache[pid] = {

            "id": page["id"],

            "title": page["title"],

            "url": page["url"],

            "category": page["category"],

            "keywords": page["keywords"],

            "content": page["content"],

            "embedding": embedding,

            "hash": current_hash

        }

    cache_kaydet(yeni_cache)

    print("\nEmbedding index hazır.")


def embeddingleri_yukle():

    return cache_yukle()


if __name__ == "__main__":

    embedding_index_olustur()