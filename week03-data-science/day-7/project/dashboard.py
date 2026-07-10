import os
import sys
import warnings

import pandas as pd
import plotly.express as px
import streamlit as st

warnings.filterwarnings('ignore')

project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

DATA_FILE = os.path.join(project_dir, "data", "Sample - Superstore.xls")
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Could not find data file: {DATA_FILE}")

raw_df = pd.read_excel(DATA_FILE, engine='xlrd')


def main():
    from src.cleaning import clean_data
    from src.features import create_features
    from src.visualization import sales_chart

    df = clean_data(raw_df)
    df = create_features(df)

    st.plotly_chart(sales_chart(df))

    if "Sales" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Profit Margin"] = df["Profit"] / df["Sales"].replace(0, 1)

    if df.empty:
        st.warning("No data found.")


if __name__ == "__main__":
    main()


