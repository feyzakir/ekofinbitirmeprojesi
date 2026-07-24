from rag.llm import cevap_uret

sorular = [
    "BIST100 RSI kaç?",
    "MACD sinyali ne durumda?",
    "Bollinger Bant göstergesi ne söylüyor?",
    "Son halka arzlar hangileri?",
    "Hangi sektörler güçlü görünüyor?",
    "Orta vadeli takip listesinde hangi hisseler var?",
    "Piyasanın genel görünümü nasıl?"
]

with open("chat_test_sonuclari.txt", "w", encoding="utf-8") as f:

    for i, soru in enumerate(sorular, start=1):

        cevap = cevap_uret(soru)

        f.write("=" * 80 + "\n")
        f.write(f"SORU {i}\n")
        f.write(f"{soru}\n\n")
        f.write("CEVAP\n")
        f.write(f"{cevap}\n\n")

print("Test sonuçları chat_test_sonuclari.txt dosyasına kaydedildi.")