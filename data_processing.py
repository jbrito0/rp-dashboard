import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_google_sheet_public(csv_url):
    """
    Load a published Google Sheet CSV as a DataFrame
    Args:
        csv_url (str): Published CSV link of Google Sheet
    Returns:
        pd.DataFrame: Sheet data with 'Mes' column added
    """
    # Convert the /pubhtml link to CSV export URL
    csv_export_url = csv_url.replace("/pubhtml", "/pub?output=csv")
    
    df = pd.read_csv(csv_export_url)
    
    # Clean & add Month column
    df = df.dropna(subset=["Fecha"])  # Drop rows without Fecha
    df["Mes"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m")
    
    return df

def filter_data(df, month, level):
    """Filter DataFrame by month and Nivel"""
    if month != "Todos":
        df = df[df["Mes"] == month]
    if level:
        df = df[df["Nivel"].isin(level)]
    return df
