import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image

image = Image.open(image/protein_background.jpg)

def load_data(file):
    return pd.read_csv(file)

def analyze_protein_data(data):
    protein_types = data['Type'].unique()
    protein_counts = data['Type'].value_counts()
    
    results = {
        'protein_types': protein_types.tolist(),
        'counts': protein_counts.tolist()
    }
    return results

def create_indicators(data):
    avg_molecular_weight = data['Molecular Weight'].mean()
    min_molecular_weight = data['Molecular Weight'].min()
    max_molecular_weight = data['Molecular Weight'].max()
    
    indicators = {
        'avg_mw': round(avg_molecular_weight, 2),
        'min_mw': round(min_molecular_weight, 2),
        'max_mw': round(max_molecular_weight, 2)
    }
    return indicators

def display_results(results, indicators):
    st.subheader("Análisis de Proteínas")
    
    fig1 = px.bar(results['protein_types'], results['counts'])
    st.plotly_chart(fig1)
    
    st.write("# Indicadores")
    st.dataframe(pd.DataFrame([indicators]))

st.title("Análisis de Proteínas")
st.markdown("<h3 style='text-align: center; color: white;'>Bienvenido al Análisis de Proteínas</h3>", unsafe_allow_html=True)

st.image(image, caption="Proteínas", use_column_width=True)

uploaded_file = st.file_uploader("Subir un archivo CSV", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)

    results = analyze_protein_data(data)

    indicators = create_indicators(data)

    display_results(results, indicators)
