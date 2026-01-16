import streamlit as st
from data_processing import load_google_sheet_public
import importlib

# --- Hide Streamlit menu and footer ---
st.set_page_config(
    page_title="📊 Dashboard de Ventas", 
    layout="wide",
    initial_sidebar_state="collapsed"
)
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Session state for page navigation ---
if "page" not in st.session_state:
    st.session_state.page = "Overview"

# --- Google Sheet URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSQYwheQSWRk8pWFIPHegbpeHGoF3-S5zgkenfq35X1wAC_XBntUgpNkZyOdoZMczJ0wh5CbU7LD-Od/pubhtml"

# --- Load data ---
df, sales_cols, purchase_cols, volume_cols, purchase_cols_dup = load_google_sheet_public(sheet_url)

# --- Botón Actualizar Datos y Navegación ---
col_refresh, col_overview, col_monthly, col_yearly = st.columns([1, 1, 1, 1])
with col_refresh:
    if st.button("🔄 Actualizar Datos"):
        st.cache_data.clear()
        st.rerun()
with col_overview:
    if st.button("📌 Resumen"):
        st.session_state.page = "Overview"
with col_monthly:
    if st.button("📆 Mensual"):
        st.session_state.page = "Monthly"
with col_yearly:
    if st.button("📈 Anual"):
        st.session_state.page = "Yearly"

st.markdown("---")

# --- Import pages dynamically (top-level files now) ---
overview = importlib.import_module("overview")
monthly = importlib.import_module("monthly")
yearly = importlib.import_module("yearly")

# --- Render selected page ---
if st.session_state.page == "Overview":
    overview.render(df, sales_cols, purchase_cols, volume_cols, purchase_cols)
elif st.session_state.page == "Monthly":
    monthly.render(df, sales_cols, purchase_cols, volume_cols, purchase_cols)
elif st.session_state.page == "Yearly":
    yearly.render(df, sales_cols, purchase_cols, volume_cols, purchase_cols)
