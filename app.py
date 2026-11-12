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

DB_FILE = "veritabani.json"

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
            "veli_sifre": "1234",  # Veli şifresi
        }
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
      json.dump(varsayilan_veri, f, ensure_ascii=False, indent=4)

  with open(DB_FILE, "r", encoding="utf-8") as f:
    return json.load(f)


def veritabanini_kaydet(veri):
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=4)


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

temel_url = "https://okul-saglik-asistani-spuk5zx9pxaeqiumqtcra9.streamlit.app"

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
  veli_sifre = aktif_ogrenci.get("veli_sifre", "1234")

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

  # --- VELİ GİRİŞİ İLE BİLGİ GÜNCELLEME ALANI ---
  st.markdown("---")
  with st.expander("🔐 Veli Girişi ile Bilgi Güncelle"):
    girilen_veli_sifre = st.text_input(
        "Veli Şifrenizi Giriniz:",
        type="password",
        placeholder="Veli şifresi...",
        key="veli_giris_sifre",
    )

    if girilen_veli_sifre == veli_sifre:
      st.success("✅ Veli yetkisi doğrulandı. Bilgileri güncelleyebilirsiniz:")
      with st.form("veli_guncelle_form"):
        yeni_hastalik = st.text_input(
            "Sağlık Durumu / Rahatsızlık", aktif_ogrenci["hastalik"]
        )
        yeni_tel1 = st.text_input("1. Veli Tel", aktif_ogrenci["veli_tel_1"])
        yeni_ad1 = st.text_input(
            "1. Veli Adı ve Yakınlığı", aktif_ogrenci["veli_ad_1"]
        )
        yeni_tel2 = st.text_input("2. Veli Tel", aktif_ogrenci["veli_tel_2"])
        yeni_ad2 = st.text_input(
            "2. Veli Adı ve Yakınlığı", aktif_ogrenci["veli_ad_2"]
        )
        yeni_lokasyon = st.text_input(
            "İlaç / Malzeme Lokasyonu", aktif_ogrenci["lokasyon"]
        )

        veli_kaydet_btn = st.form_submit_button(
            "Bilgilerimi Güncelle ve Kaydet"
        )

        if veli_kaydet_btn:
          veritabani[ogrenci_id]["hastalik"] = yeni_hastalik
          veritabani[ogrenci_id]["veli_tel_1"] = yeni_tel1
          veritabani[ogrenci_id]["veli_ad_1"] = yeni_ad1
          veritabani[ogrenci_id]["veli_tel_2"] = yeni_tel2
          veritabani[ogrenci_id]["veli_ad_2"] = yeni_ad2
          veritabani[ogrenci_id]["lokasyon"] = yeni_lokasyon
          veritabanini_kaydet(veritabani)
          st.success(
              "🎉 Sağlık ve iletişim bilgileriniz başarıyla güncellendi!"
          )
    elif girilen_veli_sifre != "":
      st.error("❌ Hatalı veli şifresi!")

  # --- İDARE / REHBER ÖĞRETMEN GEÇİŞİ ---
  with st.expander("🔐 İdare & Rehber Öğretmen Paneli Geçişi"):
    acil_yonetici_sifre = st.text_input(
        "Yönetici Şifresini Giriniz:",
        type="password",
        placeholder="Şifre...",
        key="acil_yonetici_sifre_giris",
    )
    if acil_yonetici_sifre == "MAI2026":
      st.success("✅ Şifre doğrulandı!")
      st.markdown(
          f"👉 Yönetim Paneline gitmek için tıklayın: **[{temel_url}]({temel_url})**"
      )
    elif acil_yonetici_sifre != "":
      st.error("❌ Hatalı şifre!")

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
            "Mevcut Öğrenciyi Güncelle & Veli Şifresi Belirle",
            "Yeni Öğrenci Ekle & QR Oluştur",
        ],
    )

    if secilen_islem == "Mevcut Öğrenciyi Güncelle & Veli Şifresi Belirle":
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
          yeni_kan = st.selectbox("Kan Grubu", KAN_GRUPLARI, index=kan_index)

          yeni_tel1 = st.text_input("1. Veli Tel", ogrenci["veli_tel_1"])
          yeni_tel2 = st.text_input("2. Veli Tel", ogrenci["veli_tel_2"])
          yeni_lokasyon = st.text_input("İlaç Lokasyonu", ogrenci["lokasyon"])
          yeni_veli_sifre = st.text_input(
              "Veli Giriş Şifresi", ogrenci.get("veli_sifre", "1234")
          )

          kaydet_btn = st.form_submit_button("Bilgileri Güncelle")

          if kaydet_btn:
            veritabani[ogrenci_sec]["ad_soyad_kod"] = yeni_ad
            veritabani[ogrenci_sec]["hastalik"] = yeni_hastalik
            veritabani[ogrenci_sec]["kan_grubu"] = yeni_kan
            veritabani[ogrenci_sec]["veli_tel_1"] = yeni_tel1
            veritabani[ogrenci_sec]["veli_tel_2"] = yeni_tel2
            veritabani[ogrenci_sec]["lokasyon"] = yeni_lokasyon
            veritabani[ogrenci_sec]["veli_sifre"] = yeni_veli_sifre
            veritabanini_kaydet(veritabani)
            st.success("🎉 Bilgiler ve Veli şifresi başarıyla güncellendi!")

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
        yeni_veli_sifre = st.text_input(
            "Veli Giriş Şifresi Belirle", value="1234"
        )

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
              "veli_sifre": yeni_veli_sifre,
          }
          veritabanini_kaydet(veritabani)
          st.success(
              f"🎉 {yeni_id} kodlu yeni öğrenci ve veli şifresi başarıyla"
              " oluşturuldu!"
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
