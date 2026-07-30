"""
Terminal Chatbot
"""

from rag.llm import cevap_uret
from database import APPLICATION_NAME, yeni_session

def main():

    print("=" * 60)
    print(f"{APPLICATION_NAME} Piyasa Görünümü Asistanı")
    print("Çıkmak için q yazınız.")
    print("=" * 60)
    session_id = yeni_session()

    while True:

        soru = input("\nSoru : ")

        if soru.lower() in ["q", "quit", "exit"]:
            break

        print("\nCevap:\n")

        cevap = cevap_uret(
        session_id,
        soru
        )

        print(cevap)

if __name__ == "__main__":

    main() 