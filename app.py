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
                "1. Bilinç Yerindeyse: Panik yapmayın. Hemen glikoz jeli veya"
                " 1 bardak şekerli su verin.<br>2. Bilinç Kapalıysa: ASLA"
                " ağızdan sıvı vermeyin, yan yatırın."
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

# Canlı ve Doğru Web Adresiniz
temel_url = "https://okul-saglik-asistani-spuk5zx9pxaeqiumqtcra9.streamlit.app"

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

  kategori_renk = aktif_ogrenci["kategori_renk"]
  ogrenci_kod = aktif_ogrenci["ad_soyad_kod"]
  hastalik = aktif_ogrenci["hastalik"]
  kan_grubu = aktif_ogrenci["kan_grubu"]
  protokol = aktif_ogrenci["protokol"]
  lokasyon = aktif_ogrenci["lokasyon"]
  tel1 = aktif_ogrenci["veli_tel_1"]
  ad1 = aktif_ogrenci["veli_ad_1"]
  tel2 = aktif_ogrenci["veli_tel_2"]
  ad2 = aktif_ogrenci["veli_ad_2"]

  card_html = (
      f"<div class='card-box' style='border-left-color: {kategori_renk};'>"
      f"<h3 style='margin-top:0; color:#2d3748; font-size:18px;'>🆔 Kayıt:"
      f" <b>{ogrenci_kod}</b></h3>"
      f"<p style='margin:4px 0; font-size:16px;'><b>⚠️ Sağlık Durumu:</b>"
      f" <span style='color: {kategori_renk}; font-weight:"
      f" bold;'>{hastalik}</span></p>"
      f"<p style='margin:4px 0; color:#4a5568;'><b>Kan Grubu:</b>"
      f" {kan_grubu}</p></div>"
  )
  st.markdown(card_html, unsafe_allow_html=True)

  with st.expander(
      "🚨 KRİTİK İLK MÜDAHALE REHBERİ (Tıkla / Aç)", expanded=True
  ):
    proto_html = (
        f"<div style='background-color:#fff5f5; border-left: 6px solid"
        f" {kategori_renk}; padding: 15px; border-radius: 8px;'>"
        f"{protokol}</div>"
    )
    st.markdown(proto_html, unsafe_allow_html=True)

  st.markdown("### 📞 Hızlı İletişim Hatları")
  btn1_html = (
      f"<a href='tel:{tel1}' class='call-btn-1'>📞 {ad1} Ara ({tel1})</a>"
  )
  st.markdown(btn1_html, unsafe_allow_html=True)

  btn2_html = (
      f"<a href='tel:{tel2}' class='call-btn-1'>📞 {ad2} Ara ({tel2})</a>"
  )
  st.markdown(btn2_html, unsafe_allow_html=True)

  st.markdown("")
  st.markdown(
      "<a href='tel:112' class='call-btn-112'>🚨 112 ACİL ÇAĞRI MERKEZİNİ"
      " BAĞLAN</a>",
      unsafe_allow_html=True,
  )

  st.markdown("---")
  loc_html = (
      "<div style='background-color:#edf2f7; padding:10px; border-radius:6px;"
      f" font-size:13px; color:#4a5568;'><b>💊 İlaç / Malzeme Lokasyonu:</b>"
      f" {lokasyon}</div>"
  )
  st.markdown(loc_html, unsafe_allow_html=True)

# --- 2. SENARYO: REHBER ÖĞRETMEN YÖNETİM VE GÜNCELLEME PANELİ ---
else:
  st.markdown(
      '<div class="mobile-header">🔐 REHBER ÖĞRETMEN & İDARE GÜNCELLEME'
      " PANELİ</div>",
      unsafe_allow_html=True,
  )

  sifre = st.text_input(
      "Yönetici Şifresini Giriniz:", type="password", placeholder="Şifre..."
  )

  if sifre == "MAI2026":
    st.success(
        "✅ Yetki doğrulandı. Öğrenci bilgilerini güncelleyebilir, yeni"
        " öğrenci ekleyebilir ve QR kodlarını indirebilirsiniz."
    )

    st.markdown("---")
    secilen_islem = st.radio(
        "İşlem Seçin:",
        [
            "Mevcut Öğrenciyi Güncelle & QR İndir",
            "Yeni Öğrenci Ekle & QR Oluştur",
        ],
    )

    if secilen_islem == "Mevcut Öğrenciyi Güncelle & QR İndir":
      ogrenci_sec = st.selectbox(
          "İşlem Yapılacak Öğrenciyi Seçin:", list(veritabani.keys())
      )

      if ogrenci_sec:
        ogrenci = veritabani[ogrenci_sec]

        ogrenci_hedef_url = f"{temel_url}/?id={ogrenci_sec}"
        qr_byte = qr_kod_uret(ogrenci_hedef_url)

        col1, col2 = st.columns([1, 2])
        with col1:
          st.image(
              qr_byte,
              caption=f"QR: {ogrenci_sec}",
              use_container_width=True,
          )
          st.download_button(
              label="📥 QR Kodu İndir (PNG)",
              data=qr_byte,
              file_name=f"karekod_{ogrenci_sec}.png",
              mime="image/png",
          )
        with col2:
          st.info(
              f"**Hedef Bağlantı:** `{ogrenci_hedef_url}`\n\nYandaki butona"
              " basarak bu öğrencinin kartına basılacak QR görselini"
              " indirebilirsiniz."
          )

        st.markdown("---")
        with st.form("guncelle_form"):
          st.subheader(f"Düzenlenen Kayıt: {ogrenci_sec}")
          yeni_ad = st.text_input("Öğrenci Adı / Kodu", ogrenci["ad_soyad_kod"])
          yeni_hastalik = st.text_input("Sağlık Durumu", ogrenci["hastalik"])

          mevcut_kan = (
              ogrenci["kan_grubu"]
              if ogrenci["kan_grubu"] in KAN_GRUPLARI
              else KAN_GRUPLARI[0]
          )
          kan_index = KAN_GRUPLARI.index(mevcut_kan)
          yeni_kan = st.selectbox(
              "Kan Grubu", KAN_GRUPLARI, index=kan_
