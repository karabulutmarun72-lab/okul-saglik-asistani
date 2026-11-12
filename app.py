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
      f"""<div style="background-color:#edf2f7; padding:10px; border-radius:6px; font-size:13px; color:#4a5568;"><b>💊 İlaç / Malzeme Lokasyonu:</b> {aktif_ogrenci['lokasyon']}</div>""",
      unsafe_allow_html=True,
  )

# --- 2. SENARYO: REHBER ÖĞRETMEN YÖNETİM VE GÜNCELLEME PANELİ ---
else:
  st.markdown(
      '<div class="mobile-header">🔐 REHBER ÖĞRETMEN & İDARE GÜNCELLEME'
      ' PANELİ</div>',
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
              "Kan Grubu", KAN_GRUPLARI, index=kan_index
          )

          yeni_tel1 = st.text_input("1. Veli Tel", ogrenci["veli_tel_1"])
          yeni_tel2 = st.text_input("2. Veli Tel", ogrenci["veli_tel_2"])
          yeni_lokasyon = st.text_input("İlaç Lokasyonu", ogrenci["lokasyon"])

          kaydet_btn = st.form_submit_button("Bilgileri Güncelle")

          if kaydet_btn:
            veritabani[ogrenci_sec]["ad_soyad_kod"] = yeni_ad
            veritabani[ogrenci_sec]["hastalik"] = yeni_hastalik
            veritabani[ogrenci_sec]["kan_grubu"] = yeni_kan
            veritabani[ogrenci_sec]["veli_tel_1"] = yeni_tel1
            veritabani[ogrenci_sec]["veli_tel_2"] = yeni_tel2
            veritabani[ogrenci_sec]["lokasyon"] = yeni_lokasyon
            veritabanini_kaydet(veritabani)
            st.success("🎉 Bilgiler başarıyla güncellendi!")

    elif secilen_islem == "Yeni Öğrenci Ekle & QR Oluştur":
      with st.form("yeni_ekle_form"):
        st.subheader("Yeni Öğrenci Tanımla")
        yeni_id = st.text_input(
            "Özgün QR ID Kodu (Örn: MAI-5C-05)", placeholder="MAI-..."
        )
        yeni_ad = st.text_input("Öğrenci Kodu / Adı (Örn: Öğrenci #05 (5/C))")
        yeni_hastalik = st.text_input("Sağlık Durumu / Rahatsızlık")
        yeni_kan = st.selectbox("Kan Grubu", KAN_GRUPLARI)
        yeni_protokol = st.text_area(
            "Acil Müdahale Protokolü (HTML destekli)"
        )
        yeni_lokasyon = st.text_input("İlaç / Malzeme Nerede?")
        yeni_tel1 = st.text_input("1. Veli Telefonu")
        yeni_ad1 = st.text_input("1. Veli Adı ve Yakınlığı")
        yeni_tel2 = st.text_input("2. Veli Telefonu")
        yeni_ad2 = st.text_input("2. Veli Adı ve Yakınlığı")

        ekle_btn = st.form_submit_button("Sisteme Kaydet ve QR Üret")

        if ekle_btn and yeni_id:
          veritabani[yeni_id] = {
              "ad_soyad_kod": yeni_ad,
              "hastalik": yeni_hastalik,
              "kategori_renk": "#e53e3e",
              "kan_grubu": yeni_kan,
              "protokol": yeni_protokol,
              "lokasyon": yeni_lokasyon,
              "veli_tel_1": yeni_tel1,
              "veli_ad_1": yeni_ad1,
              "veli_tel_2": yeni_tel2,
              "veli_ad_2": yeni_ad2,
          }
          veritabanini_kaydet(veritabani)
          st.success(
              f"🎉 {yeni_id} kodlu yeni öğrenci başarıyla sisteme eklendi!"
          )

  elif sifre != "":
    st.error("❌ Hatalı şifre!")
  else:
    st.info(
        "ℹ️ Öğrenci sağlık verilerini güncellemek veya QR kod indirmek için"
        " lütfen şifrenizi giriniz."
    )

st.markdown(
    "<p style='text-align:center; font-size:11px; color:#a0aec0;"
    " margin-top:30px;'>Mehmet Akif İnan Ortaokulu • Dinamik Sağlık Modülü</p>",
    unsafe_allow_html=True,
)
