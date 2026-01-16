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
    
    st.title("📆 Ventas Mensuales")

    # --- Filter by Nivel ---
    niveles = df["nivel"].unique().tolist()
    selected_niveles = st.multiselect("Seleccionar Nivel", niveles, default=niveles)
    df_filtered = df[df["nivel"].isin(selected_niveles)]

    # --- Top 10 ---
    st.subheader("🏆 Top 10 Ventas Mensuales")
    top10 = df_filtered.sort_values(by="volumen enero", ascending=False).head(10)
    st.dataframe(top10[["nombre", "nivel", "volumen enero", "% Meta Volumen"]].set_index("nombre"))

    # --- Gráfico de Tendencia Mensual ---
    st.subheader("📈 Tendencia Mensual")
    
    # Calculate total monthly volume for trend
    monthly_total = df_filtered["volumen enero"].sum()
    
    # Create time series data (currently only January, but structured for multiple months)
    import pandas as pd
    trend_data = pd.DataFrame({
        'Mes': ['Enero'],
        'Volumen Total': [monthly_total],
        'Fecha': pd.to_datetime(['2024-01-01'])  # Using a reference date for January
    })
    
    # Create line plot with markers
    fig = px.line(trend_data, x='Fecha', y='Volumen Total', 
                  title="",
                  markers=True,  # Show dots for each data point
                  line_shape='linear')  # Connect points with straight lines
    
    # Format the x-axis to show month names
    fig.update_xaxes(
        tickformat="%B",  # Show full month names
        tickmode='array',
        tickvals=trend_data['Fecha'],
        ticktext=['Enero']
    )
    
    # Add data labels on the points
    fig.update_traces(
        mode='lines+markers+text',
        text=[f"${monthly_total:,.0f}"],
        textposition="top center",
        textfont=dict(size=12)
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="",
        yaxis_title="Volumen Total",
        showlegend=False
    )
    
    st.plotly_chart(fig, width='stretch')

    # --- Goals Table ---
    st.markdown("### 📊 Rendimiento de Ventas y Compras")
    
    # Create formatted dataframe for display
    table_df = df_filtered[["nombre", "nivel", 
                           "meta mensual volumen", "volumen enero", "% Meta Volumen",
                           "meta compra mensual", "compras enero", "% Meta Compras"]].copy()
    
    # Format monetary columns with $ sign
    table_df["meta mensual volumen"] = table_df["meta mensual volumen"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    table_df["volumen enero"] = table_df["volumen enero"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    table_df["meta compra mensual"] = table_df["meta compra mensual"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    table_df["compras enero"] = table_df["compras enero"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    
    # Format percentage columns with % sign
    table_df["% Meta Volumen"] = table_df["% Meta Volumen"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else x)
    table_df["% Meta Compras"] = table_df["% Meta Compras"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else x)
    
    # Set index and display with styling
    table_df = table_df.set_index("nombre")
    
    # Apply conditional styling for percentage columns
    def style_percentages(val):
        if isinstance(val, str) and '%' in val:
            try:
                # Extract numeric value from percentage string
                pct = float(val.replace('%', ''))
                if pct < 50:
                    return 'background-color: #ffcccc'  # Light red
                elif pct < 100:
                    return 'background-color: #ffffcc'  # Light yellow
                else:
                    return 'background-color: #ccffcc'  # Light green
            except ValueError:
                return ''
        return ''
    
    # Apply styling to the dataframe
    styled_df = table_df.style.applymap(style_percentages, subset=["% Meta Volumen", "% Meta Compras"])
    
    st.dataframe(styled_df)
