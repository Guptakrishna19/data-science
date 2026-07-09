
import matplotlib.pyplot as plt

import numpy as np

import streamlit as st

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

@st.cache_data
def load_data():
    return pd.read_csv("data/tips.csv")

df = load_data()