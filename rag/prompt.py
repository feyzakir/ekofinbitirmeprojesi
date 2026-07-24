"""
prompt.py

Hybrid Search sonucunu LLM'in anlayacağı
tek bir prompt haline getirir.
"""

import json


SYSTEM_PROMPT = """
Sen Ekofin Piyasa Görünümü Asistanısın.

Kurallar:

1. SADECE verilen kaynakları kullan.

2. Bilgi kaynakta yoksa
"Buna ilişkin güncel bilgi bulunamadı."
de.

3. Tahmin yapma.

4. Finansal tavsiye verme.

5. Cevabı kısa, net ve profesyonel yaz.

6. Mümkünse maddeler halinde cevap ver.

7. Cevabın sonunda ilgili sayfanın URL'sini yaz.
"""


def sayfa_context(page):
    """
    Sayfayı GPT'nin okuyabileceği
    hale getirir.
    """

    try:
        content = json.loads(page["content"])

        content = json.dumps(
            content,
            ensure_ascii=False,
            indent=2
        )

    except Exception:

        content = page["content"]

    return f"""
========================================

Başlık:
{page["title"]}

Kategori:
{page["category"]}

URL:
{page["url"]}

Anahtar Kelimeler:
{page["keywords"]}

İçerik:

{content}

========================================
"""


def build_prompt(question, pages):
    """
    pages:
        database'den gelen ilk 3 kayıt
    """

    context = ""

    for page in pages:

        context += sayfa_context(page)

    user_prompt = f"""
Kullanıcı Sorusu:

{question}


Aşağıdaki bilgilerden yararlanarak cevap ver.

{context}
"""

    return SYSTEM_PROMPT, user_prompt