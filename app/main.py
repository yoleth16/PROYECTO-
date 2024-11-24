import streamlit as st
import pandas as pd
from PIL import Image
import os
import plotly.express as px

# Cargar imagen de fondo
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/protein_background.jpg")
image = Image.open(image_path)

def load_data(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {str(e)}")
        return None

def analyze_protein_data(data):
    if data is None or data.empty:
        st.warning("No se pudo cargar los datos del archivo CSV.")
        return None
    
    protein_types = data.columns.get_list()
    protein_column = next((col for col in protein_types if 'type' in col.lower()), None)
    
    if protein_column is None:
        st.warning("No se encontró una columna con 'type' o similar.")
        return None
    
    protein_counts = data[protein_column].value_counts()
    
    results = {
        'protein_types': protein_counts.index.tolist(),
        'counts': protein_counts.values.tolist()
    }
    return results

def create_indicators(data):
    if data is None or data.empty:
        st.warning("No se pueden calcular indicadores debido a un error previo.")
        return None
    
    avg_molecular_weight = data['Molecular Weight'].mean() if 'Molecular Weight' in data.columns else None
    min_molecular_weight = data['Molecular Weight'].min() if 'Molecular Weight' in data.columns else None
    max_molecular_weight = data['Molecular Weight'].max() if 'Molecular Weight' in data.columns else None
    
    indicators = {
        'avg_mw': round(avg_molecular_weight, 2) if avg_molecular_weight is not None else None,
        'min_mw': round(min_molecular_weight, 2) if min_molecular_weight is not None else None,
        'max_mmw': round(max_molecular_weight, 2) if max_molecular_weight is not None else None
    }
    return indicators

def display_image(image):
    if image is not None:
        st.image(image, caption="Proteínas", use_column_width=True)
    else:
        st.error("No se pudo cargar la imagen de fondo.")

def display_results(results, indicators):
    st.subheader("Análisis de Proteínas")
    
    if results is None:
        st.warning("No se pudieron obtener los resultados del análisis.")
        return
    
    # Mostrar gráfico de barras de tipos de proteínas
    fig1 = px.bar(results['protein_types'], results['counts'])
    st.plotly_chart(fig1)
    
    # Mostrar indicadores en una tabla
    st.write("# Indicadores")
    st.dataframe(pd.DataFrame([indicators]))

st.title("Análisis de Proteínas")
st.markdown("<h3 style='text-align: center; color: white;'>Bienvenido al Análisis de Proteínas</h3>", unsafe_allow_html=True)

display_image(image)

uploaded_file = st.file_uploader("Subir un archivo CSV", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)

    if data is not None:
        results = analyze_protein_data(data)
        
        if results is not None:
            indicators = create_indicators(data)
            
            display_results(results, indicators)
        else:
            st.warning("No se pudieron obtener los resultados del análisis.")
    else:
        st.warning("No se pudo cargar el archivo CSV.")

