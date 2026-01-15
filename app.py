import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing import load_google_sheet_public, filter_data

# --- Configure Streamlit page ---
st.set_page_config(page_title="📊 Dashboard de Ventas", layout="wide")

# --- Sidebar: Published Google Sheet ---
st.sidebar.header("📂 Conectar con Google Sheets (Público)")
sheet_url = st.sidebar.text_input(
    "URL del Google Sheet publicado",
    value="https://docs.google.com/spreadsheets/d/e/2PACX-1vSQYwheQSWRk8pWFIPHegbpeHGoF3-S5zgkenfq35X1wAC_XBntUgpNkZyOdoZMczJ0wh5CbU7LD-Od/pubhtml"
)

if sheet_url:
    df = load_google_sheet_public(sheet_url)

    # --- Sidebar: Meta Input ---
    meta = st.sidebar.number_input("🎯 Meta de Ventas", min_value=0, value=50000, step=500)

    # --- Dashboard Title ---
    st.title("📊 Dashboard de Ventas")

    # --- Metrics Row ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_ventas = df["Ventas"].sum()
        st.metric(label="💰 Ventas Totales", value=f"${total_ventas:,.2f}")

    with col2:
        faltante = max(0, meta - total_ventas)
        st.metric(label="📉 Faltante para la Meta", value=f"${faltante:,.2f}")

    with col3:
        promedio_ventas = df["Ventas"].mean()
        st.metric(label="📊 Promedio de Ventas", value=f"${promedio_ventas:,.2f}")

    # --- Filters Row ---
    col4, col5 = st.columns([2, 2])
    with col4:
        meses_disponibles = df["Mes"].unique().tolist()
        meses_opciones = ["Todos"] + meses_disponibles
        mes_seleccionado = st.selectbox("📅 Seleccionar Mes", meses_opciones)

    with col5:
        niveles_seleccionados = st.multiselect(
            "🔍 Seleccionar Nivel", df["Nivel"].unique(), default=df["Nivel"].unique()
        )

    # --- Apply Filters ---
    df_filtered = filter_data(df, mes_seleccionado, niveles_seleccionados)

    # --- Graphs Row - Ventas por Vendedor ---
    col6, _ = st.columns([3, 1])
    df_sorted = df_filtered.sort_values(by="Ventas", ascending=False)
    with col6:
        fig_bar = px.bar(
            df_sorted,
            y="Nombre",
            x="Ventas",
            color="Nivel",
            title="💼 Ventas por Vendedor",
            orientation="h",
            text="Ventas",
        )
        fig_bar.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_bar.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Second Graphs Row ---
    st.subheader("📈 Tendencia de Ventas en el Tiempo")
    col7, col8 = st.columns([2, 2])

    with col7:
        df_trend = df.groupby("Mes")["Ventas"].sum().reset_index()
        fig_line = px.line(df_trend, x="Mes", y="Ventas", markers=True, title="📈 Tendencia de Ventas")
        fig_line.update_xaxes(type='category')
        st.plotly_chart(fig_line, use_container_width=True)

    with col8:
        fig_pie = px.pie(df_filtered, names="Nivel", values="Ventas", title="📊 Contribución por Nivel")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Sales Table Section ---
    st.subheader("📋 Datos de Vendedores")
    col9, _ = st.columns([1, 3])
    with col9:
        buscar_vendedor = st.text_input("🔍 Buscar Vendedor")

    if buscar_vendedor:
        df_filtered = df_filtered[df_filtered["Nombre"].str.contains(buscar_vendedor, case=False)]

    df_table = df_filtered[["Nombre", "Ventas", "Nivel", "Invitaciones", "Presentaciones"]].sort_values(
        by="Ventas", ascending=False
    )
    df_table = df_table.set_index("Nombre")
    st.dataframe(df_table, use_container_width=True)

else:
    st.info("🔹 Ingresa la URL publicada del Google Sheet para cargar los datos públicamente.")

if st.sidebar.button("🔄 Actualizar Datos"):
    st.cache_data.clear()
