import streamlit as st
import pandas as pd
import plotly.express as px

# Configure Streamlit page
st.set_page_config(page_title="📊 Dashboard de Ventas", layout="wide")

# Sidebar - File Upload
st.sidebar.header("📂 Cargar Datos")
uploaded_file = st.sidebar.file_uploader("Sube un archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Ensure data consistency
    df["Mes"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m")  # Extract month-year

    # Sidebar - Meta Input
    meta = st.sidebar.number_input("🎯 Meta de Ventas", min_value=0, value=50000, step=500)

    # Dashboard Title
    st.title("📊 Dashboard de Ventas")

    # Metrics Row
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

    # Filters Row (Mes & Nivel on the same line)
    col4, col5 = st.columns([2, 2])

    with col4:
        # Add "Todos" option to the month filter
        meses_disponibles = df["Mes"].unique().tolist()
        meses_opciones = ["Todos"] + meses_disponibles
        mes_seleccionado = st.selectbox("📅 Seleccionar Mes", meses_opciones)

    with col5:
        niveles_seleccionados = st.multiselect("🔍 Seleccionar Nivel", df["Nivel"].unique(), default=df["Nivel"].unique())

    # Apply Filters
    df_filtered = df if mes_seleccionado == "Todos" else df[df["Mes"] == mes_seleccionado]
    df_filtered = df_filtered[df_filtered["Nivel"].isin(niveles_seleccionados)]

    # Graphs Row - Made "Ventas por Vendedor" Wider ✅
    col6, _ = st.columns([3, 1])  # ✅ Increased width of Ventas por Vendedor graph

    # Sort data for graphs
    df_sorted = df_filtered.sort_values(by="Ventas", ascending=False)

    with col6:
        fig_bar = px.bar(df_sorted, 
                         y="Nombre", 
                         x="Ventas", 
                         color="Nivel", 
                         title="💼 Ventas por Vendedor", 
                         orientation="h",
                         text="Ventas")  # Keeps number amount
        fig_bar.update_traces(texttemplate='%{text:,.0f}', textposition='outside')  # Formatting numbers
        fig_bar.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Second Graphs Row - "Tendencia de Ventas" & "Contribución por Nivel"
    st.subheader("📈 Tendencia de Ventas en el Tiempo")

    col7, col8 = st.columns([2, 2])  # Keeping both graphs aligned

    with col7:
        df_trend = df.groupby("Mes")["Ventas"].sum().reset_index()
        fig_line = px.line(df_trend, x="Mes", y="Ventas", markers=True, title="📈 Tendencia de Ventas")
        fig_line.update_xaxes(type='category')  # Ensure months are categorical
        st.plotly_chart(fig_line, use_container_width=True)

    with col8:
        fig_pie = px.pie(df_filtered, 
                         names="Nivel", 
                         values="Ventas", 
                         title="📊 Contribución por Nivel")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Sales Table Section
    st.subheader("📋 Datos de Vendedores")

    # Smaller Search Box for Vendor ✅
    col9, _ = st.columns([1, 3])  # Adjust column width to make the search box smaller

    with col9:
        buscar_vendedor = st.text_input("🔍 Buscar Vendedor")

    if buscar_vendedor:
        df_filtered = df_filtered[df_filtered["Nombre"].str.contains(buscar_vendedor, case=False)]

    # Remove unnamed first column & reorder columns
    df_table = df_filtered[["Nombre", "Ventas", "Nivel", "Invitaciones", "Presentaciones"]].sort_values(by="Ventas", ascending=False)
    
    # Display Table
    df_table = df_table.set_index("Nombre")  # Set "Nombre" as the index (removes number column)
    st.dataframe(df_table, use_container_width=True)
