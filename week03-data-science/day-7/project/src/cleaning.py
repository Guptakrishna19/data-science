# cleaning.py

import pandas as pd

def clean_data(df):

    df = df.copy()

    df.drop_duplicates(inplace=True)

    df.fillna(0, inplace=True)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df

