import matplotlib.pyplot as plt

import numpy as np

import streamlit as st

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')


bill = st.slider(
    "Maximum Bill",
    min_value=10,
    max_value=60,
    value=60
)


day = st.selectbox(
    "Choose Day",
    ["All","Thur","Fri","Sat","Sun"]
)

gender = st.multiselect(
    "Gender",
    ["Male","Female"],
    default=["Male","Female"]
)

show_data = st.checkbox("Show Dataset")

chart = st.radio(
    "Chart Type",
    ["Bar","Pie"]
)