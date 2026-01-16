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

    # Normalize column names to lowercase
    df.columns = df.columns.str.lower()

    # Ensure numeric columns (only those that exist)
    numeric_cols = [
        "meta mensual volumen",
        "meta compras 2026",
        "meta compra mensual",
        "volumen enero",
        "volumen febrero",
        "volumen marzo",
        "volumen abril",
        "volumen mayo",
        "volumen junio",
        "volumen julio",
        "volumen agosto",
        "volumen septiembre",
        "volumen octubre",
        "volumen noviembre",
        "volumen diciembre",
        "compras enero",
        "compras febrero",
        "compras marzo",
        "compras abril",
        "compras mayo",
        "compras junio",
        "compras julio",
        "compras agosto",
        "compras septiembre",
        "compras octubr",
        "compras noviembre",
        "compras diciembre",
    ]
    existing_numeric_cols = [col for col in numeric_cols if col in df.columns]
    for col in existing_numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Calculate percentages
    df["% Meta Volumen"] = (df["volumen enero"] / df["meta mensual volumen"] * 100).round(2)
    df["% Meta Compras"] = (df["compras enero"] / df["meta compra mensual"] * 100).round(2)

    # Calculate annual totals
    volume_cols = [col for col in df.columns if col.startswith("volumen ")]
    purchase_cols = [col for col in df.columns if col.startswith("compras ")]
    
    # Ensure volume and purchase columns are numeric
    df[volume_cols] = df[volume_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    df[purchase_cols] = df[purchase_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    
    df["total_volumen"] = df[volume_cols].sum(axis=1)
    df["total_compras"] = df[purchase_cols].sum(axis=1)
    
    df["% Meta Volumen Anual"] = (df["total_volumen"] / (df["meta mensual volumen"] * 12) * 100).round(2)
    df["% Meta Compras Anual"] = (df["total_compras"] / df["meta compras 2026"] * 100).round(2)

    # Define sales & purchase columns
    sales_cols = volume_cols + ["meta mensual volumen", "% Meta Volumen", "total_volumen", "% Meta Volumen Anual"]
    purchase_cols = purchase_cols + ["meta compra mensual", "% Meta Compras", "meta compras 2026", "total_compras", "% Meta Compras Anual"]

    return df, sales_cols, purchase_cols, volume_cols, purchase_cols

def filter_data(df, level=None):
    """Filter by Nivel if provided"""
    if level:
        df = df[df["nivel"].isin(level)]
    return df
