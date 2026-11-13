import io
import json
import os
import qrcode
import streamlit as st

# Sayfa Yapılandırması (Mobil öncelikli görünüm)
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
            "veli_sifre": "1234",
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

# --- MOBİL APK UYUMLU ÖZEL CSS TASARIMI ---
st.markdown(
    """
    <style>
    .stApp { background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .mobile-header {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white; padding: 22px 15px; border-radius: 0 0 18px 18px;
        text-align: center; font-weight: 700; font-size: 20px; margin: -60px -20px 20px -20px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
    }
    .card-box {
        background-color: #ffffff; padding: 18px; border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06); margin-bottom: 15px; border-left: 6px solid #3b82f6;
    }
    .call-btn-1 {
        background-color: #2563eb; color: white !important; padding: 15px; border-radius: 12px;
        text-align: center; font-weight: 600; font-size: 16px; display: block;
        text-decoration: none; margin-bottom: 12px; box-shadow: 0 3px 6px rgba(37, 99, 235, 0.3);
    }
    .call-btn-112 {
        background-color: #dc2626; color: white !important; padding: 16px; border-radius: 12px;
        text-align: center; font-weight: 700; font-size: 18px; display: block;
        text-decoration: none; box-shadow: 0 4px 10px rgba(220, 38, 38, 0.4);
    }
    .stButton button { width: 100%; border-radius: 10px; font-weight: 600; padding: 10px; }
    </style>
""",
    unsafe_allow_html=True,
)

temel_url = "https://okul-saglik-asistani-spuk5zx9pxaeqiumqtcra9.streamlit.app"

query_params = st.query_params
ogrenci_id = query_params.get("id", None)

# --- 1. SENARYO: QR KOD OKUTULDUĞUNDA VEYA SEÇİLDİĞİNDE ACİL DURUM EKRANI ---
if ogrenci_id and ogrenci_id in veritabani:
  aktif_ogrenci = veritabani[ogrenci_id]

  st.markdown(
      '<div class="mobile-header">🚨 ACİL SAĞLIK & İLK MÜDAHALE</div>',
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
      f"<h3 style='margin-top:0; color:#1e293b; font-size:18px;'>🆔 Kayıt:"
      f" <b>{ogrenci_kod}</b></h3>"
      f"<p style='margin:6px 0; font-size:16px;'><b>⚠️ Sağlık Durumu:</b>"
      f" <span style='color: {kategori_renk}; font-weight:"
      f" 700;'>{hastalik}</span></p>"
      f"<p style='margin:4px 0; color:#475569;'><b>Kan Grubu:</b>"
      f" {kan_grubu}</p></div>"
  )
  st.markdown(card_html, unsafe_allow_html=True)

  with st.expander(
      "🚨 KRİTİK İLK MÜDAHALE REHBERİ (Dokun / Aç)", expanded=True
  ):
    proto_html = (
        f"<div style='background-color:#fef2f2; border-left: 5px solid"
        f" {kategori_renk}; padding: 14px; border-radius: 8px; color:"
        f" #991b1b; font-size: 15px; line-height: 1.5;'>{protokol}</div>"
    )
    st.markdown(proto_html, unsafe_allow_html=True)

  st.markdown(
      "<h4 style='color:#1e293b; font-size:16px; margin-top:20px;'>📞 Hızlı"
      " İletişim Hatları</h4>",
      unsafe_allow_html=True,
  )
  btn1_html = (
      f"<a href='tel:{tel1}' class='call-btn-1'>📞 {ad1} Ara ({tel1})</a>"
  )
  st.markdown(btn1_html, unsafe_allow_html=True)

  btn2_html = (
      f"<a href='tel:{tel2}' class='call-btn-1'>📞 {ad2} Ara ({tel2})</a>"
  )
  st.markdown(btn2_html, unsafe_allow_html=True)

  st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
  st.markdown(
      "<a href='tel:112' class='call-btn-112'>🚨 112 ACİL ÇAĞRI MERKEZİNİ"
      " BAĞLAN</a>",
      unsafe_allow_html=True,
  )

  st.markdown("---")
  loc_html = (
      "<div style='background-color:#f1f5f9; padding:12px; border-radius:10px;"
      f" font-size:14px; color:#334155;'><b>💊 İlaç / Malzeme Lokasyonu:</b>"
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

  # --- ANA SAYFAYA / İDARE PANELİNE DÖNÜŞ ---
  st.markdown("---")
  if st.button("🏠 Ana Menüye / İdare Paneline Dön"):
    st.query_params.clear()
    st.rerun()

# --- 2. SENARYO: ANA EKRAN (QR Okut / ID Gir / İdare Paneli) ---
else:
  st.markdown(
      '<div class="mobile-header">🔐 REHBER ÖĞRETMEN & İDARE PANELİ</div>',
      unsafe_allow_html=True,
  )

  # --- EKLENEN ÖZELLİK: QR KOD OKUT / ID İLE ACİL DURUM GÖRÜNTÜLE ---
  with st.expander(
      "📸 Karekod Okut / QR ID Kodu ile Acil Durum Görüntüle", expanded=True
  ):
    st.info(
        "Öğrencinin karekodunu okutarak veya ID kodunu girerek kısıtlı acil"
        " durum ekranına anında ulaşabilirsiniz:"
    )

    # Manuel ID / QR Kodu Giriş Alanı
    girilen_qr_id = st.text_input(
        "Karekod ID Kodunu Girin veya Okutun (Örn: MAI-5A-14)",
        placeholder="MAI-...",
        key="manuel_qr_giris",
    )
    if st.button("🚨 Karekod / ID ile Acil Ekranını Aç"):
      if girilen_qr_id.strip() in veritabani:
        st.query_params["id"] = girilen_qr_id.strip()
        st.rerun()
      elif girilen_qr_id.strip() != "":
        st.error("❌ Bu ID koduna ait sistemde kayıtlı öğrenci bulunamadı!")

    st.markdown("---")
    st.markdown(
        "Veya listeden hızlıca seçerek acil ekranını açabilirsiniz:"
    )
    if len(veritabani) > 0:
      secilen_hizli_ogrenci = st.selectbox(
          "Kayıtlı Öğrenci Listesi:",
          list(veritabani.keys()),
          format_func=lambda x: (
              f"{veritabani[x]['ad_soyad_kod']} ({x})"
          ),
      )
      if st.button("🚨 Seçilen Öğrencinin Acil Ekranını Aç"):
        st.query_params["id"] = secilen_hizli_ogrenci
        st.rerun()
    else:
      st.warning("Sistemde henüz kayıtlı öğrenci bulunmuyor.")

  st.markdown("---")

  sifre = st.text_input(
      "Yönetici Şifresini Giriniz:", type="password", placeholder="Şifre..."
  )

  if sifre == "MAI2026":
    st.success(
        "✅ Yetki doğrulandı. Öğrenci bilgilerini güncelleyebilir, yeni"
        " öğrenci ekleyebilir veya silebilirsiniz."
    )

    st.markdown("---")
    secilen_islem = st.radio(
        "İşlem Seçin:",
        [
            "Mevcut Öğrenciyi Güncelle & Veli Şifresi Belirle",
            "Yeni Öğrenci Ekle & QR Oluştur",
            "Öğrenci Kaydı Sil",
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
              "veli_sifre": yeni_veli_s_ifre
              if "yeni_veli_sifre" in locals()
              else "1234",
          }
          # Düzeltilmiş anahtar ataması
          veritabani[yeni_id]["veli_sifre"] = yeni_veli_sifre
          veritabanini_kaydet(veritabani)
          st.success(
              f"🎉 {yeni_id} kodlu yeni öğrenci ve veli şifresi başarıyla"
              " oluşturuldu!"
          )

    elif secilen_islem == "Öğrenci Kaydı Sil":
      st.subheader("🗑️ Öğrenci Kaydı Sil")
      if len(veritabani) > 0:
        silinecek_secim = st.selectbox(
            "Silinecek Öğrenciyi Seçin:", list(veritabani.keys())
        )
        st.warning(
            f"⚠️ Dikkat: **{silinecek_secim}** ID'li öğrenci kaydı kalıcı olarak"
            " silinecektir!"
        )
        if st.button("Seçilen Öğrenciyi Kalıcı Olarak Sil"):
          if silinecek_secim in veritabani:
            del veritabani[silinecek_secim]
            veritabanini_kaydet(veritabani)
            st.success(
                f"🗑️ {silinecek_secim} kodlu öğrenci başarıyla silindi! Lütfen"
                " sayfayı yenileyin."
            )
      else:
        st.info("Sistemde silinecek kayıt bulunmamaktadır.")

  elif sifre != "":
    st.error("❌ Hatalı şifre!")
  else:
    st.info(
        "ℹ️ Öğrenci sağlık verilerini güncellemek veya QR kod indirmek için"
        " lütfen şifrenizi giriniz."
    )

st.markdown(
    "<p style='text-align:center; font-size:11px; color:#94a3b8;"
    " margin-top:30px;'>Mehmet Akif İnan Ortaokulu • Mobil Sağlık Modülü</p>",
    unsafe_allow_html=True,
)
