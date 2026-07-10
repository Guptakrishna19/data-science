import matplotlib.pyplot as plt

import numpy as np

import streamlit as st
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("tips_200.csv")


st.sidebar.header("Filters")

col1,col2,col3 = st.columns(3)

with st.expander("Dataset"):
    st.dataframe(df)