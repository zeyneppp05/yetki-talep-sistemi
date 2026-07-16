import streamlit as st
import pandas as pd
import json
from datetime import datetime
from ai_analyzer import analiz_et

st.set_page_config(page_title="Yetki Talep Sistemi", layout="centered")
st.title("Akıllı Yetki Talep Sistemi")

if "gecmis" not in st.session_state:
    st.session_state.gecmis = []

with st.form("talep_formu"):
    departman = st.selectbox("Departman", ["Trading", "Finans", "Operasyon", "Satış", "Lojistik"])
    sistem = st.selectbox("Talep edilen sistem", ["Raporlama Paneli", "Trader/IA Sistemi", "Finansal Veritabanı", "CRM", "Yönetici Paneli"])
    gerekce = st.text_area("Talep gerekçesi")
    sure = st.selectbox("Süre", ["1 hafta", "1 ay", "Süresiz"])
    gonder = st.form_submit_button("Talebi analiz et")

if gonder:
    with st.spinner("AI talebi analiz ediyor..."):
        sonuc_metni = analiz_et(departman, sistem, gerekce, sure)
        try:
            temiz_metin = sonuc_metni.replace("```json", "").replace("```", "").strip()
            sonuc = json.loads(temiz_metin)
        except:
            sonuc = {"risk_seviyesi": "bilinmiyor", "karar": "manuel inceleme", "aciklama": sonuc_metni}

    st.session_state.gecmis.append({
        "Zaman": datetime.now().strftime("%H:%M"),
        "Departman": departman,
        "Sistem": sistem,
        "Risk": sonuc["risk_seviyesi"],
        "Karar": sonuc["karar"]
    })

    if sonuc["risk_seviyesi"] == "düşük":
        st.success(f"{sonuc['karar']} — {sonuc['aciklama']}")
    elif sonuc["risk_seviyesi"] == "orta":
        st.warning(f"{sonuc['karar']} — {sonuc['aciklama']}")
    else:
        st.error(f"{sonuc['karar']} — {sonuc['aciklama']}")

if st.session_state.gecmis:
    st.subheader("Geçmiş talepler")
    st.dataframe(pd.DataFrame(st.session_state.gecmis))
