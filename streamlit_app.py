import streamlit as st
from datetime import datetime
from database import (
    yeni_session,
    sessionlari_getir,
    session_mesajlarini_getir
)
from chatbot import cevap_uret

# ---------------------------------------------------
# SAYFA AYARLARI
# ---------------------------------------------------

st.set_page_config(
    page_title="Ekofin AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
if "session_id" not in st.session_state:
    st.session_state.session_id = yeni_session()

# ---------------------------------------------------
# CSS
# ---------------------------------------------------

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:1rem;
padding-bottom:1rem;
}

.user-box{
background:#2563eb;
padding:14px;
border-radius:12px;
margin-top:8px;
margin-bottom:8px;
color:white;
}

.bot-box{
background:#f4f4f4;
padding:14px;
border-radius:12px;
margin-top:8px;
margin-bottom:8px;
color:black;
border:1px solid #dddddd;
}

.title{
font-size:34px;
font-weight:700;
color:#2563eb;
}

.subtitle{
font-size:16px;
color:#777777;
margin-bottom:15px;
}

hr{
margin-top:8px;
margin-bottom:8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "Yeni Sohbet"

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("📈 Ekofin AI")

    st.write("")

    if st.button("➕ Yeni Sohbet", use_container_width=True):

        st.session_state.messages = []
        st.session_state.session_id = yeni_session()
        st.rerun()

    st.divider()

st.subheader("Geçmiş Sohbetler")

oturumlar = sessionlari_getir()

if len(oturumlar) == 0:

    st.caption("Henüz sohbet bulunmuyor.")

else:

    for oturum in oturumlar:

        if st.button(

            oturum["title"],

            key=oturum["session_id"],

            use_container_width=True

        ):

            st.session_state.session_id = oturum["session_id"]

            st.session_state.messages = session_mesajlarini_getir(

                oturum["session_id"]

            )

            st.rerun()

    st.divider()

    st.subheader("Hakkında")

    st.caption("""
Bu chatbot Ekofin verilerini kullanarak
sorularınızı cevaplar.

Yanıtlar SQL üzerinde bulunan
güncel içeriklerden oluşturulur.
""")

# ---------------------------------------------------
# BAŞLIK
# ---------------------------------------------------

st.markdown(
    "<div class='title'>📈 Ekofin AI Asistanı</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Piyasa Görünümü ve Ekofin verileri üzerinde çalışan yapay zekâ asistanı</div>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------------------------
# MESAJLAR
# ---------------------------------------------------

for mesaj in st.session_state.messages:

    if mesaj["role"]=="user":

        st.markdown(
            f"""
<div class="user-box">

👤 <b>Siz</b><br><br>

{mesaj["content"]}

</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
<div class="bot-box">

🤖 <b>Ekofin AI</b><br><br>

{mesaj["content"]}

</div>
""",
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# MESAJ KUTUSU
# ---------------------------------------------------

soru = st.chat_input(
    "Ekofin'e bir soru sorun..."
)

if soru:

    # Kullanıcı mesajı
    st.session_state.messages.append(
        {
            "role": "user",
            "content": soru
        }
    )

    with st.chat_message("user"):
        st.markdown(soru)

    # Yapay zekâ cevabı
    with st.chat_message("assistant"):

        with st.spinner("Ekofin düşünüyor..."):

            try:

                cevap = cevap_uret(
                    st.session_state.session_id,
                    soru
                    )
                # ---------------------------------------------------
                # chatbot.py string döndürüyorsa
                # ---------------------------------------------------

                if isinstance(cevap, str):

                    cevap_metni = cevap
                    kaynaklar = None

                # ---------------------------------------------------
                # chatbot.py dict döndürüyorsa
                # ---------------------------------------------------

                elif isinstance(cevap, dict):

                    cevap_metni = cevap.get(
                        "answer",
                        "Cevap bulunamadı."
                    )

                    kaynaklar = cevap.get(
                        "sources",
                        None
                    )

                else:

                    cevap_metni = str(cevap)
                    kaynaklar = None

            except Exception as hata:

                cevap_metni = (
                    "❌ Bir hata oluştu.\n\n"
                    + str(hata)
                )

                kaynaklar = None

        st.markdown(cevap_metni)

        # ---------------------------------------------------
        # Kaynaklar
        # ---------------------------------------------------

        if kaynaklar:

            st.divider()

            st.caption("📚 Kullanılan Kaynaklar")

            for kaynak in kaynaklar:

                if isinstance(kaynak, dict):

                    baslik = kaynak.get(
                        "title",
                        "-"
                    )

                    url = kaynak.get(
                        "url",
                        ""
                    )

                    st.markdown(
                        f"- **{baslik}**\n\n{url}"
                    )

                else:

                    st.markdown(f"- {kaynak}")

    # Sohbet geçmişine ekle

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": cevap_metni
        }
    )

    st.rerun() 