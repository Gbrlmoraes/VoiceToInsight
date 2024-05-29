import streamlit as st
import pandas as pd
import os

os.chdir(r'J:\Estudo\Projetos\VoiceToInsight')

st.title("VoiceToInsight🎧")

# Loading the data
@st.cache_data
def load_data():
    return pd.read_csv(r'data\sample.csv')

df = load_data()