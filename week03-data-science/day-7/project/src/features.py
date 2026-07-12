# features.py

def create_features(df):

    df["Year"] = df["Order Date"].dt.year

    df["Month"] = df["Order Date"].dt.month_name()

    df["Profit Margin"] = (
        df["Profit"] / df["Sales"]
    )

    return df
