import io
import json
import os
import qrcode
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Okul Sağlık ve Acil Müdahale Asistanı",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Dosya tabanlı veritabanı yolu
DB_FILE = "veritabani.json"

# Standart Kan Grubu Listesi
KAN_GRUPLARI = [
    "0 Rh(-)",
    "0 Rh(+)",
    "A Rh(-)",
    "A Rh(+)",
    "B Rh(-)",
    "B Rh(+)",
    "AB Rh(-)",
    "AB Rh(+)",
]


# Varsayılan veritabanı oluşturma
def veritabanini_yukle():
  if not os.path.exists(DB_FILE):
    varsayilan_veri = {
        "MAI-5A-14": {
            "ad_soyad_kod": "Öğrenci #14 (5/A)",
            "hastalik": "Tip 1 Diyabet (İnsülin Bağımlı)",
            "kategori_renk": "#e53e3e",
            "kan_grubu": "A Rh(+)",
            "protokol": (
                "<b>1. Bilinç Yerindeyse:</b> Panik yapmayın. Hemen"
                " glikoz jeli veya 1 bardak şekerli su verin.<br><b>2. Bilinç"
                " Kapalıysa:</b> ASLA ağızdan sıvı vermeyin, yan yatırın."
            ),
            "lokasyon": "Yedek insülin hemşireliktedir.",
            "veli_tel_1": "+905551234567",
            "veli_ad_1": "Ahmet Bey (Baba)",
            "veli_tel_2": "+905429876543",
            "veli_ad_2": "Fatma Hanım (Anne)",
        }
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
      json.dump(varsayilan_veri, f, ensure_ascii=False, indent=4)

  with open(DB_FILE, "r", encoding="utf-8") as f:
    return json.load(f)


def veritabanini_kaydet(veri):
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=4)


# QR Kod Üreten Fonksiyon
def qr_kod_uret(veri_metni):
  qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_H,
      box_size=10,
      border=2,
  )
  qr.add_data(veri_metni)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  buf = io.BytesIO()
  img.save(buf, format="PNG")
  return buf.getvalue()


veritabani = veritabanini_yukle()

# Mobil Uyumlu Özel Tasarım CSS
st.markdown(
    """
    <style>
    .stApp { background-color: #f7fafc; }
    .mobile-header {
        background: linear-gradient(135deg, #2b6cb0, #2c5282);
        color: white; padding: 20px; border-radius: 12px;
        text-align: center; font-weight: bold; font-size: 19px; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-box {
        background-color: #ffffff; padding: 18px; border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px; border-left: 6px solid #3182ce;
    }
    .call-btn-1 {
        background-color: #3182ce; color: white; padding: 14px; border-radius: 10px;
        text-align: center; font-weight: bold; font-size: 16px; display: block;
        text-decoration: none; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(49,130,206,0.3);
    }
    .call-btn-112 {
        background-color: #e53e3e; color: white; padding: 16px; border-radius: 10px;
        text-align: center; font-weight: bold; font-size: 18px; display: block;
        text-decoration: none; box-shadow: 0 4px 6px rgba(229,62,62,0.4);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Canlı web adresiniz
temel_url = "https://okul-saglik-asistani.streamlit.app"

# URL parametresinden öğrenci ID'sini alma
query_params = st.query_params
ogrenci_id = query_params.get("id", None)

# --- 1. SENARYO: QR KOD OKUTULDUĞUNDA ACİL DURUM EKRANI ---
if ogrenci_id and ogrenci_id in veritabani:
  aktif_ogrenci = veritabani[ogrenci_id]

  st.markdown(
      '<div class="mobile-header">🚨 ACİL SAĞLIK & İLK MÜDAHALE'
      ' EKRANI</div>',
      unsafe_allow_html=True,
  )

  st.markdown(
      f"""
    <div class="card-box" style="border-left-color: {aktif_ogrenci['kategori_renk']};">
        <h3 style="margin-top:0; color:#2d3748; font-size:18px;">🆔 Kayıt: <b>{aktif_ogrenci['ad_soyad_kod']}</b></h3>
        <p style="margin:4px 0; font-size:16px;"><b>⚠️ Sağlık Durumu:</b> <span style="color: {aktif_ogrenci['kategori_renk']}; font-weight: bold;">{aktif_ogrenci['hastalik']}</span></p>
        <p style="margin:4px 0; color:#4a5568;"><b>Kan Grubu:</b> {aktif_ogrenci['kan_grubu']}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  with st.expander(
      "🚨 KRİTİK İLK MÜDAHALE REHBERİ (Tıkla / Aç)", expanded=True
  ):
    st.markdown(
        f"""
        <div style="background-color:#fff5f5; border-left: 6px solid {aktif_ogrenci['kategori_renk']}; padding: 15px; border-radius: 8px;">
            {aktif_ogrenci['protokol']}
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("### 📞 Hızlı İletişim Hatları")
  st.markdown(
      f"""<a href="tel:{aktif_ogrenci['veli_tel_1']}" class="call-btn-1">📞 {aktif_ogrenci['veli_ad_1']} Ara ({aktif_ogrenci['veli_tel_1']})</a>""",
      unsafe_allow_html=True,
  )
  st.markdown(
      f"""<a href="tel:{aktif_ogrenci['veli_tel_2']}" class="call-btn-1">📞 {aktif_ogrenci['veli_ad_2']} Ara ({aktif_ogrenci['veli_tel_2']})</a>""",
      unsafe_allow_html=True,
  )
  st.markdown("")
  st.markdown(
      """<a href="tel:112" class="call-btn-112">🚨 112 ACİL ÇAĞRI MERKEZİNİ BAĞLAN</a>""",
      unsafe_allow_html=True,
  )

  st.markdown("---")
  st.markdown(
      f
