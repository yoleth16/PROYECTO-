import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# Cargar imagen de fondo
try:
    image = Image.open("image/protein_background.jpg")
except FileNotFoundError:
    image = None

# Función para cargar datos desde el archivo CSV
def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {str(e)}")
        return None

# Función para analizar los datos de proteínas
def analyze_protein_data(data):
    if data is None or data.empty:
        st.warning("No se pudo cargar los datos del archivo CSV.")
        return None
    
    protein_types = data.columns.tolist()
    protein_column = next((col for col in protein_types if 'type' in col.lower()), None)
    
    if protein_column is None:
        st.warning("No se encontró una columna con 'type' o similar.")
        return None
    
    protein_counts = data[protein_column].value_counts()
    return {
        'protein_column': protein_column,
        'protein_types': protein_counts.index.tolist(),
        'counts': protein_counts.values.tolist()
    }

# Función para crear indicadores avanzados
def create_indicators(data):
    indicators = {}
    if 'Molecular Weight' in data.columns:
        indicators.update({
            'Peso Molecular Promedio': round(data['Molecular Weight'].mean(), 2),
            'Peso Molecular Mínimo': round(data['Molecular Weight'].min(), 2),
            'Peso Molecular Máximo': round(data['Molecular Weight'].max(), 2)
        })
    if 'Protein Concentration' in data.columns:
        indicators.update({
            'Concentración Promedio': round(data['Protein Concentration'].mean(), 2),
            'Concentración Máxima': round(data['Protein Concentration'].max(), 2),
        })
    return indicators

# Función para mostrar gráficos de análisis
def display_results(data, results, indicators):
    st.subheader("Análisis de Proteínas")
    
    if results:
        # Gráfico de barras para tipos de proteínas
        fig1 = px.bar(
            x=results['protein_types'],
            y=results['counts'],
            labels={'x': 'Tipo de Proteína', 'y': 'Cantidad'},
            title=f"Distribución de {results['protein_column']}",
            color=results['counts'],
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig1)
    
    if 'Molecular Weight' in data.columns:
        # Histograma del peso molecular
        fig2 = px.histogram(
            data, 
            x='Molecular Weight',
            nbins=20,
            title='Distribución del Peso Molecular',
            labels={'Molecular Weight': 'Peso Molecular'},
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig2)
    
    if indicators:
        st.write("### Indicadores Clave")
        st.table(indicators)

# Título y descripción de la app
st.title("Análisis Interactivo de Proteínas")
st.markdown("""
Esta aplicación permite analizar datos de proteínas desde un archivo CSV. 
Sube tu archivo y descubre indicadores clave y visualizaciones interactivas.
""")

# Mostrar imagen de fondo
if image:
    st.image(image, caption="Análisis de Proteínas", use_column_width=True)

# Carga del archivo CSV
uploaded_file = st.file_uploader("Subir un archivo CSV", type="csv")
if uploaded_file:
    data = load_data(uploaded_file)
    if data is not None:
        results = analyze_protein_data(data)
        indicators = create_indicators(data)
        display_results(data, results, indicators)
    else:
        st.warning("No se pudo cargar el archivo CSV correctamente.")
