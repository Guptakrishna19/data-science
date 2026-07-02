import pandas as pd  # type: ignore[import]
import numpy as np  # type: ignore[import]

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().copy()  # <-- .copy() removes the ambiguity

    if "City" in df.columns:
        df["City"] = df["City"].astype("str")
    if "Sub-Category" in df.columns:
        df["Sub-Category"] = df["Sub-Category"].astype("category")
    if "Category" in df.columns:
        df["Category"] = df["Category"].astype("category")

    return df

def cap_outliers_iqr(df: pd.DataFrame, column: str, verbose: bool = True) -> pd.DataFrame:
    if column not in df.columns:
        return df

    df = df.copy()
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers_count = ((df[column] < lower_bound) | (df[column] > upper_bound)).sum()
    if verbose:
        print(f"Outliers in '{column}' column: {outliers_count}")

    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    return df

def treat_all_outliers(df: pd.DataFrame, columns=None) -> pd.DataFrame:
    if columns is None:
        columns = ["Quantity", "Sales", "Price", "Discount"]
    for col in columns:
        df = cap_outliers_iqr(df, col)
    return df

def _profit_tier_slow(df: pd.DataFrame) -> pd.Series:
    def classify(row):
        margin = row["Profit"] / row["Sales"] if row["Sales"] else 0
        if margin > 0.2:
            return "high"
        elif margin > 0:
            return "low"
        else:
            return "loss"
    return df.apply(classify, axis=1)

def add_profit_tier(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    margin = np.where(df["Sales"] != 0, df["Profit"] / df["Sales"], 0)

    conditions = [margin > 0.2, margin > 0]
    choices = ["high", "low"]
    df["Profit_Tier"] = np.select(conditions, choices, default="loss")
    return df