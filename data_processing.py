import pandas as pd

def load_data(file):
    """Loads data from an Excel file."""
    df = pd.read_excel(file)
    df["Mes"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m")  # Extract month-year
    return df

def filter_data(df, month, level):
    """Filters data by month and sales level."""
    return df[(df["Mes"] == month) & (df["Nivel"].isin(level))]
