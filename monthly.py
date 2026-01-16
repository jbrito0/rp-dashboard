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

def render(df, sales_cols, purchase_cols, volume_cols, purchase_cols_list):
    # Apply custom CSS
    st.markdown(shadow_css, unsafe_allow_html=True)
    
    st.title("📆 Ventas Mensuales")

    # --- Filter by Nivel and Select Month ---
    col1, col2 = st.columns(2)
    with col1:
        niveles = df["nivel"].unique().tolist()
        selected_niveles = st.multiselect("Seleccionar Nivel", niveles, default=niveles)
    with col2:
        available_months = [col.replace("volumen ", "") for col in volume_cols]
        selected_month = st.selectbox("Seleccionar Mes", available_months, index=0)
    
    df_filtered = df[df["nivel"].isin(selected_niveles)]
    selected_volume_col = f"volumen {selected_month}"
    selected_purchase_col = f"compras {selected_month}"

    # --- Ventas por Vendedor ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"🏆 Ventas por Vendedor - {selected_month.capitalize()}")
    all_sellers = df_filtered.sort_values(by=selected_volume_col, ascending=False).copy()
    
    # Create horizontal bar chart
    fig = px.bar(
        all_sellers, 
        x=selected_volume_col, 
        y="nombre", 
        orientation='h',
        text=selected_volume_col,
        title="",
        labels={selected_volume_col: f"Volumen {selected_month.capitalize()}", "nombre": "Vendedor"}
    )
    fig.update_traces(texttemplate='$%{text:,.2f}', textposition='outside', textfont=dict(color='black'))
    fig.update_layout(
        yaxis={'categoryorder':'total ascending', 'tickfont': {'color': 'black'}},
        margin=dict(l=20, r=20, t=20, b=20),
        height=max(400, len(all_sellers) * 20)  # Adjust height based on number of sellers
    )
    st.plotly_chart(fig, width='stretch')

    # --- Gráfico de Tendencia Mensual ---
    st.subheader("📈 Tendencia Mensual")
    
    # Calculate total monthly volume for all available months
    monthly_totals = [df_filtered[col].sum() for col in volume_cols]
    months_cap = [month.capitalize() for month in available_months]
    
    # Create time series data
    import pandas as pd
    trend_data = pd.DataFrame({
        'Mes': months_cap,
        'Volumen Total': monthly_totals,
        'Fecha': pd.to_datetime([f"2024-{i+1:02d}-01" for i in range(len(available_months))])
    })
    
    # Create line plot with markers
    fig = px.line(trend_data, x='Fecha', y='Volumen Total', 
                  title="",
                  markers=True,
                  line_shape='linear')
    
    # Format the x-axis to show month names
    fig.update_xaxes(
        tickformat="%B",
        tickmode='array',
        tickvals=trend_data['Fecha'],
        ticktext=months_cap
    )
    
    # Add data labels on the points
    fig.update_traces(
        mode='lines+markers+text',
        text=[f"${v:,.0f}" for v in monthly_totals],
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
    
    # Calculate percentages for selected month
    df_filtered = df_filtered.copy()
    df_filtered[f"% Meta Volumen {selected_month}"] = (df_filtered[selected_volume_col] / df_filtered["meta mensual volumen"] * 100).round(2)
    df_filtered[f"% Meta Compras {selected_month}"] = (df_filtered[selected_purchase_col] / df_filtered["meta compra mensual"] * 100).round(2)
    
    # Create formatted dataframe for display
    table_df = df_filtered[["nombre", "nivel", 
                           "meta mensual volumen", selected_volume_col, f"% Meta Volumen {selected_month}",
                           "meta compra mensual", selected_purchase_col, f"% Meta Compras {selected_month}"]].copy()
    
    # Format monetary columns with $ sign
    table_df["meta mensual volumen"] = table_df["meta mensual volumen"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    table_df[selected_volume_col] = table_df[selected_volume_col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    table_df["meta compra mensual"] = table_df["meta compra mensual"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    table_df[selected_purchase_col] = table_df[selected_purchase_col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else x)
    
    # Format percentage columns with % sign
    table_df[f"% Meta Volumen {selected_month}"] = table_df[f"% Meta Volumen {selected_month}"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else x)
    table_df[f"% Meta Compras {selected_month}"] = table_df[f"% Meta Compras {selected_month}"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else x)
    
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
    styled_df = table_df.style.applymap(style_percentages, subset=[f"% Meta Volumen {selected_month}", f"% Meta Compras {selected_month}"])
    
    st.dataframe(styled_df)
