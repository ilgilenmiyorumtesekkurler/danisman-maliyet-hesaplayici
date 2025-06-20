import streamlit as st

# Sabitler (Constants)
TAM_GUN_SAAT = 7.5
DAKIKA_BIR_SAATTE = 60

# --- Web Uygulama Arayüzü ---
st.set_page_config(
    page_title="BilgiGEN Danışman Maliyet Hesaplayıcı",
    page_icon="✅",
    layout="centered" # veya "wide"
)

st.title("✅ BilgiGEN Danışmanlık Maliyet Hesaplayıcı")
st.markdown("Danışmanların toplam harcadığı süre ve maliyetlerini kolayca hesaplayın.")

# Kullanıcı Giriş Alanları
st.header("1. Danışman ve Süre Bilgileri")

danisman_adi = st.text_input("Danışman Adı", placeholder="Örn: Semih ÖZBİLEN")
gunluk_ucret_dolar = st.number_input(
    f"{danisman_adi if danisman_adi else 'Danışman'} için 1 Adam/Günlük Anlaşılan Dolar Ücreti ($)",
    min_value=0.0,
    value=250.0, # Varsayılan değer
    step=10.0,
    format="%.2f",
    help="Danışmanın bir tam gün (7.5 saat) için aldığı dolar ücreti."
)
# Hata aldığınız satırın doğru hali:
toplam_sure_dakika = st.number_input(
    f"{danisman_adi if danisman_adi else 'Danışman'}'ın Toplam Harcadığı Süre (Dakika)", # BURAYA DİKKAT! İçteki tek tırnak ve dıştaki çift tırnak uyumu önemli.
    min_value=0.0,
    value=450.0, # Varsayılan değer (7.5 saat * 60 dakika)
    step=15.0,
    format="%.0f",
    help="Danışmanın proje için toplam harcadığı süreyi dakika cinsinden girin."
)

st.header("2. Kur Bilgisi")
dolar_kuru_tl = st.number_input(
    "Güncel Dolar Kuru (TL)",
    min_value=0.0,
    value=39.34, # Varsayılan değer (güncel kura göre güncelleyebileceğiniz alan burası)
    step=0.05,
    format="%.2f",
    help="1 Doların TL cinsinden karşılığını girin."
)

# Hesaplama Butonu
if st.button("Hesapla", type="primary"):
    # Giriş doğrulaması
    if not danisman_adi:
        st.error("Lütfen danışman adını girin.")
    elif gunluk_ucret_dolar <= 0 or toplam_sure_dakika <= 0 or dolar_kuru_tl <= 0:
        st.error("Lütfen tüm parasal ve süre alanlarına sıfırdan büyük geçerli sayılar girin.")
    else:
        # Hesaplamalar
        toplam_saat = toplam_sure_dakika / DAKIKA_BIR_SAATTE
        birim_saat_ucreti_dolar = gunluk_ucret_dolar / TAM_GUN_SAAT
        toplam_adam_gun = toplam_saat / TAM_GUN_SAAT
        toplam_maliyet_dolar = toplam_saat * birim_saat_ucreti_dolar
        toplam_maliyet_tl = toplam_maliyet_dolar * dolar_kuru_tl

        # Sonuçları Göster
        st.subheader("📊 Hesaplama Sonuçları")
        st.info(f"**Danışman Adı:** {danisman_adi}")
        st.write(f"**Toplam Harcanan Süre:** {int(toplam_sure_dakika)} dakika ({toplam_saat:.2f} saat)")
        st.write(f"**Bir Tam Adam Gün (7.5 Saat):** ${gunluk_ucret_dolar:.2f} / Gün")
        st.write(f"**Adam Saat Maliyeti:** ${birim_saat_ucreti_dolar:.2f} / Saat")


        col1, col2 = st.columns(2) # Sonuçları iki sütunda göstermek için bu alanı ekledim

        with col1:
            st.metric(label="Toplam Adam Gün", value=f"{toplam_adam_gun:.2f} gün")
            st.metric(label="Toplam Maliyet (Dolar)", value=f"${toplam_maliyet_dolar:.2f}")

        with col2:
            st.metric(label="Toplam Maliyet (TL)", value=f"{toplam_maliyet_tl:.2f} TL")
            # Güncel kur bilgisini de yanında gösteriyoruz.
            st.markdown(f"<small>(1 Dolar = {dolar_kuru_tl:.2f} TL üzerinden hesaplanmıştır)</small>", unsafe_allow_html=True)

        st.success("Hesaplama başarıyla tamamlanmıştır!")
