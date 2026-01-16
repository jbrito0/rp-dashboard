import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)
def load_google_sheet_public(csv_url):
    """
    Load a published Google Sheet CSV as a DataFrame
    and calculate initial percentage columns.
    """
    # Convert /pubhtml to CSV export
    csv_export_url = csv_url.replace("/pubhtml", "/pub?output=csv")
    df = pd.read_csv(csv_export_url)

    # Ensure numeric columns
    numeric_cols = [
        "meta mensual volumen",
        "meta compras 2026",
        "meta compra mensual",
        "volumen enero",
        "compras enero",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Calculate percentages
    df["% Meta Volumen"] = (df["volumen enero"] / df["meta mensual volumen"] * 100).round(2)
    df["% Meta Compras"] = (df["compras enero"] / df["meta compra mensual"] * 100).round(2)

    # Define sales & purchase columns
    sales_cols = ["volumen enero", "meta mensual volumen", "% Meta Volumen"]
    purchase_cols = ["compras enero", "meta compra mensual", "% Meta Compras"]

    return df, sales_cols, purchase_cols

def filter_data(df, level=None):
    """Filter by Nivel if provided"""
    if level:
        df = df[df["nivel"].isin(level)]
    return df
