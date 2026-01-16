import streamlit as st
import plotly.express as px
from datetime import datetime

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

/* Make sure main content has background */
.main {
    background-color: #f8f9fa !important;
}

.main .block-container {
    background-color: #f8f9fa !important;
    padding: 2rem 1rem;
}
    background-color: #f8f9fa !important;
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
    
    st.title("📊 Resumen")

    # Determine current month
    month_names = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    current_month = month_names[datetime.now().month - 1]
    current_volume_col = f"volumen {current_month}"

    # --- Top 3 Performers ---
    st.markdown("<h3 style='text-align: center; margin-top: 0;'>🏆 Top 3 Vendedores</h3>", unsafe_allow_html=True)
    
    # Get top 3 performers
    top3 = df.sort_values(by=current_volume_col, ascending=False).head(3).copy()
    top3["rank"] = [1, 2, 3]
    top3["medal"] = ["🥇", "🥈", "🥉"]
    
    # Create columns for top 3
    cols = st.columns(3)
    
    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            # Check if profile image exists (name.jpg, name.png, etc.)
            import os
            import base64
            
            image_html = ""
            name_clean = str(row['nombre']).replace(' ', '_').replace('/', '_').lower()
            
            # Check for common image formats
            for ext in ['.jpg', '.jpeg', '.png', '.gif', '.jfif']:
                potential_path = f"images/{name_clean}{ext}"
                if os.path.exists(potential_path):
                    # Convert image to base64 for HTML embedding
                    with open(potential_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode()
                        image_html = f'<img src="data:image/{ext.split(".")[-1]};base64,{encoded_string}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; margin: 15px 0;">'
                    break
            
            # If no image found, use placeholder
            if not image_html:
                image_html = f'<div style="font-size: 3em; margin: 15px 0;">👤</div>'
            
            # Create complete card with everything inside HTML
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0 30px 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                border: 2px solid {'#FFD700' if i == 0 else '#C0C0C0' if i == 1 else '#CD7F32'};
                min-height: 320px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            ">
                {image_html}
                <h4 style="margin: 10px 0; color: #333; font-size: 1.3em;">{row['nombre']}</h4>
                <p style="margin: 5px 0; font-weight: bold; color: #2E8B57; font-size: 1.5em;">
                    ${row[current_volume_col]:,.2f}
                </p>
                <p style="margin: 5px 0; font-size: 1em; color: #666;">
                    {row['nivel']}
                </p>
                <div style="font-size: 4em; margin-top: 15px;">{row['medal']}</div>
            </div>
            """, unsafe_allow_html=True)

    # --- Top 10 Sales ---
    st.markdown("<h3 style='text-align: center; margin-top: 0;'>🏆 Top 10 Vendedores</h3>", unsafe_allow_html=True)
    top10 = df.sort_values(by=current_volume_col, ascending=False).head(10).copy()
    
    # Add icons for top 3
    icons = ["🥇", "🥈", "🥉", "", "", "", "", "", "", ""]
    top10["rank"] = range(1, 11)
    top10["display_name"] = [f"{icons[i]} {name}" for i, name in enumerate(top10["nombre"])]
    
    # Create horizontal bar chart
    fig_top10 = px.bar(
        top10, 
        x=current_volume_col, 
        y="display_name", 
        orientation='h',
        text=current_volume_col,
        title="",
        labels={current_volume_col: f"Volumen {current_month.capitalize()}", "display_name": "Vendedor"}
    )
    fig_top10.update_traces(texttemplate='$%{text:,.2f}', textposition='outside', textfont=dict(color='black', size=14))
    fig_top10.update_layout(
        yaxis={'categoryorder':'total ascending', 'tickfont': {'color': 'black'}},
        margin=dict(l=20, r=20, t=20, b=20),
        height=600
    )
    st.plotly_chart(fig_top10, width='stretch')
