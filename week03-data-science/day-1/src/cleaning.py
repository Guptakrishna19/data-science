"""
cleaning.py

Reusable data cleaning functions for Day 15 - Deep Data Cleaning
"""

import pandas as pd  # type: ignore[import]


# --------------------------------------------------
# Missing Values
# --------------------------------------------------

def fill_missing(df):
    """
    Fill missing values.
    Numeric columns -> Median
    Object columns -> Mode
    """

    df = df.copy()

    for col in df.columns:

        if df[col].dtype in ["int64", "float64"]:
            df[col] = df[col].fillna(df[col].median())

        else:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    return df


# --------------------------------------------------
# Remove Duplicates
# --------------------------------------------------

def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates()


# --------------------------------------------------
# Convert Data Types
# --------------------------------------------------

def convert_types(df):
    """
    Convert Price, Quantity and Rating to numeric.
    Convert OrderDate to datetime.
    """

    df = df.copy()

    numeric_cols = ["Price", "Quantity", "Rating"]

    for col in numeric_cols:

        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("$", "", regex=False)
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "OrderDate" in df.columns:
        df["OrderDate"] = pd.to_datetime(
            df["OrderDate"],
            errors="coerce"
        )

    return df


# --------------------------------------------------
# Standardize Text
# --------------------------------------------------

def clean_text(df):
    """
    Remove extra spaces and standardize capitalization.
    """

    df = df.copy()

    object_cols = df.select_dtypes(include="object").columns

    for col in object_cols:

        df[col] = (
            df[col]
            .str.strip()
            .str.title()
        )

    return df


# --------------------------------------------------
# Standardize Categories
# --------------------------------------------------

def standardize_categories(df):

    df = df.copy()

    if "PaymentMethod" in df.columns:

        payment_map = {
            "Cash": "Cash",
            "cash": "Cash",
            "CASH": "Cash",
            "Card": "Card",
            "CARD": "Card",
            "card": "Card",
            "Upi": "UPI",
            "upi": "UPI"
        }

        df["PaymentMethod"] = df["PaymentMethod"].replace(payment_map)

    return df


# --------------------------------------------------
# Remove Outliers (IQR)
# --------------------------------------------------

def remove_outliers_iqr(df, column):

    df = df.copy()

    Q1 = df[column].quantile(0.25)

    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR

    upper = Q3 + 1.5 * IQR

    df = df[
        (df[column] >= lower) &
        (df[column] <= upper)
    ]

    return df


# --------------------------------------------------
# One Hot Encoding
# --------------------------------------------------

def one_hot_encode(df, columns):

    df = pd.get_dummies(
        df,
        columns=columns,
        dtype=int
    )

    return df


# --------------------------------------------------
# Label Encoding
# --------------------------------------------------

def label_encode(df, column):

    df = df.copy()

    df[column], _ = pd.factorize(df[column])

    return df


# --------------------------------------------------
# Quality Report
# --------------------------------------------------

def quality_report(df):

    report = pd.DataFrame({

        "Metric": [

            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows"

        ],

        "Value": [

            df.shape[0],
            df.shape[1],
            df.isnull().sum().sum(),
            df.duplicated().sum()

        ]

    })

    return report


# --------------------------------------------------
# Full Cleaning Pipeline
# --------------------------------------------------

def clean_dataset(df):

    df = convert_types(df)

    df = fill_missing(df)

    df = remove_duplicates(df)

    df = clean_text(df)

    df = standardize_categories(df)

    if "Price" in df.columns:
        df = remove_outliers_iqr(df, "Price")

    return df