# app.py
import html
import streamlit as st

from api.geocoding import geocode_location
from api.marine import get_marine_forecast
from api.weather import weather_forecast
from services.forecast import ForecastService

# SETUP 
st.set_page_config(page_title="Surf Forecast PT", page_icon="🌊", layout="wide")

# ===== Tema (Light/Dark.) =====
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"  # default

def use_theme(mode: str):
    """Aplica CSS e retorna o template do Plotly e cores úteis."""
    mode = (mode or "light").lower()
    is_dark = mode == "dark"

    # CSS global
    if is_dark:
        st.markdown("""
            <style>
              .stApp { background-color:#0f1115 !important; color:#e5e7eb !important; }
              section.main > div { color:#e5e7eb !important; }
              .block-container { padding-top: 1.2rem; }
            </style>
        """, unsafe_allow_html=True)
        plotly_template = "plotly_dark"
        wg_th_bg = "#1f2937"  # cabeçalho da WG table
        text_color = "#e5e7eb"
    else:
        st.markdown("""
            <style>
              .stApp { background-color:#ffffff !important; color:#000000 !important; }
              .block-container { padding-top: 1.2rem; color:#000000 !important; }
              section.main .block-container,
              section.main p, section.main li, section.main div,
              section.main pre, section.main span { color:#000000 !important; }
              .stMarkdown, .stMarkdown * { color:#000000 !important; }
              [data-testid="stMarkdown"], [data-testid="stMarkdown"] * { color:#000000 !important; }
              [data-testid="stText"], [data-testid="stText"] * { color:#000000 !important; }
              pre, code, .stCodeBlock { color:#000000 !important; }
            </style>
        """, unsafe_allow_html=True)
        plotly_template = "plotly_white"
        wg_th_bg = "#111"     # igual já usado antes
        text_color = "#111827"

    return plotly_template, wg_th_bg, text_color

# Botão de alternância (na barra superior)
c_theme1, c_theme2 = st.columns([0.82, 0.18])
with c_theme2:
    label = "🌙 Dark" if st.session_state.theme_mode == "light" else "☀️ Light"
    if st.button(label, use_container_width=True):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"

PLOTLY_TEMPLATE, WG_TH_BG, _TEXT = use_theme(st.session_state.theme_mode)

st.title("🌊 Surf Forecast")
st.caption("Dados: Open-Meteo (Marine + Forecast) + Geocoding (Nominatim)")
fs = None
ts = None
spots_to_show = []

# ---------------------------- SIDEBAR CONTROLS ----------------------------
st.sidebar.header("Localização")
city_query = st.sidebar.text_input("Cidade (ex: Carcavelos, Portugal)", value="", help="Digite e pressione Enter")
if not city_query.strip():
    st.info("Digite uma cidade na barra lateral para ver a previsão.")
    st.stop()
try:
    lat, lon, full_name = geocode_location(city_query.strip())
    st.success(f"Localização: {full_name} ({lat:.4f}, {lon:.4f})")
    marine_data = get_marine_forecast(lat, lon)
    weather_data = weather_forecast(lat, lon)
    forecast = ForecastService.parse_forecast_data(
        marine_data, weather_data, full_name, lat, lon
    )
    st.subheader(full_name)
    text = forecast.to_llm_context()
    st.markdown(
        f'<pre style="color:#000000 !important; background:transparent !important; white-space:pre-wrap; font-family:inherit; font-size:1rem; line-height:1.5;">{html.escape(text)}</pre>',
        unsafe_allow_html=True,
    )
    st.stop()
except Exception as e:
    st.error(f"Erro ao obter previsão: {e}")
    st.stop()
