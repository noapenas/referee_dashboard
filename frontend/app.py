import streamlit as st

# Configuração global da página (tem de ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Referee Dashboard",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Referee Dashboard")
st.markdown("Bem-vindo ao teu portefólio centralizado de arbitragem.")

st.info("👈 Usa o menu lateral para navegares pelas diferentes secções (Upload Garmin, Dados FPF, etc).")

st.markdown("""
### Estado do Sistema
* **Base de Dados:** PostgreSQL (Multi-tenant ativo)
* **Motor de GPS:** PostGIS / Fitparse
* **Integração FPF:** (Em breve)
""")