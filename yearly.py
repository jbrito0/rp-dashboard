import streamlit as st
import plotly.express as px

# Custom CSS for shadows and styling
shadow_css = """
<style>
/* Aggressive background color application */
html, body, #root, .stApp, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
    background-color: #e9ecef !important;
    background: #e9ecef !important;
}

/* Override any Streamlit default backgrounds */
.stApp > * {
    background-color: transparent !important;
}

/* Light gray background for the main container */
.main .block-container {
    background-color: #e9ecef !important;
    padding: 2rem 1rem;
}

/* Shadow effects for different sections */
[data-testid="stVerticalBlock"] > [data-testid="column"] {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04);
    padding: 20px;
    margin: 10px 0;
    border: 1px solid #e9ecef;
}

[data-testid="stVerticalBlock"] > div:has([data-testid="stMarkdownContainer"]) + div:has([data-testid="stPlotlyChart"]) {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04);
    padding: 20px;
    margin: 15px 0;
    border: 1px solid #e9ecef;
}

[data-testid="stDataFrame"] {
    background-color: white !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04) !important;
    border: 1px solid #e9ecef !important;
    overflow: hidden !important;
}

[data-testid="stPlotlyChart"] > div {
    background-color: white !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04) !important;
    border: 1px solid #e9ecef !important;
}

/* Metric cards styling */
[data-testid="stMetric"] {
    background-color: white !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    padding: 15px !important;
    margin: 8px !important;
    border: 1px solid #e9ecef !important;
}

/* Title styling */
h1, h2, h3 {
    color: #2c3e50 !important;
    font-weight: 600 !important;
}
</style>
"""

def render(df, sales_cols, purchase_cols):
    # Apply custom CSS
    st.markdown(shadow_css, unsafe_allow_html=True)
    
    st.title("📈 Resumen Anual")

    # --- Filter by Nivel ---
    niveles = df["nivel"].unique().tolist()
    selected_niveles = st.multiselect("Seleccionar Nivel", niveles, default=niveles)
    df_filtered = df[df["nivel"].isin(selected_niveles)]

    # --- Sales by Nivel ---
    st.subheader("💰 Ventas por Nivel")
    df_grouped = df_filtered.groupby("nivel")["volumen enero"].sum().reset_index()
    fig = px.bar(df_grouped, x="nivel", y="volumen enero", text="volumen enero", title="")
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, width='stretch')

    # --- Goals vs Actual ---
    st.subheader("🎯 Metas y %")
    st.dataframe(df_filtered[["nombre", "nivel", "meta mensual volumen", "volumen enero", "% Meta Volumen"]].set_index("nombre"))
