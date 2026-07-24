"""
Terminal Chatbot
"""

from rag.llm import cevap_uret


def main():

    print("=" * 60)
    print("Ekofin Piyasa Görünümü Asistanı")
    print("Çıkmak için q yazınız.")
    print("=" * 60)

    while True:

        soru = input("\nSoru : ")

        if soru.lower() in ["q", "quit", "exit"]:

            break

        print("\nCevap:\n")

        cevap = cevap_uret(soru)

        print(cevap)

        print("\n" + "-" * 60)


if __name__ == "__main__":

    main() 