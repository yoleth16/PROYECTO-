import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Secuencias Biológicas",
    page_icon="🔬",
    layout="wide"
)

# Título principal
st.title("🔬 Análisis de Secuencias Biológicas")
st.markdown("""
**Bienvenido al Dashboard de Análisis de Secuencias Biológicas.**  
Sube un archivo FASTA o CSV para explorar herramientas avanzadas y visualizaciones interactivas.
""")

# Barra lateral
st.sidebar.title("📂 Subir y Configurar Archivo")
uploaded_file = st.sidebar.file_uploader(
    "Sube tu archivo FASTA o CSV",
    type=["fasta", "csv"],
    help="Puedes cargar archivos de secuencias biológicas (FASTA) o datos tabulares (CSV)."
)

# Progreso y estado
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# Procesar archivo cargado
if uploaded_file:
    # Actualizar barra de progreso
    progress_bar.progress(20)

    if uploaded_file.name.endswith(".fasta"):
        status_text.text("Procesando archivo FASTA...")
        fasta_content = uploaded_file.getvalue().decode("utf-8").splitlines()

        # Procesar secuencias FASTA
        sequences = {}
        current_header = None
        for line in fasta_content:
            line = line.strip()
            if line.startswith(">"):
                current_header = line[1:]
                sequences[current_header] = ""
            elif current_header:
                sequences[current_header] += line

        progress_bar.progress(60)
        st.sidebar.success("Archivo FASTA cargado exitosamente")
        st.write(f"### Número de secuencias cargadas: {len(sequences)}")
        st.json({header: seq[:50] + "..." for header, seq in list(sequences.items())[:5]})
        progress_bar.progress(100)

    elif uploaded_file.name.endswith(".csv"):
        status_text.text("Procesando archivo CSV...")
        try:
            data = pd.read_csv(uploaded_file)
            st.sidebar.success("Archivo CSV cargado exitosamente")
            st.write("### Vista previa de los datos")
            st.dataframe(data.head())
            progress_bar.progress(100)
        except Exception as e:
            st.error(f"Error al cargar el archivo CSV: {str(e)}")

# Indicadores clave
st.header("📊 Indicadores Clave de Análisis")
if uploaded_file:
    col1, col2, col3 = st.columns(3)
    if uploaded_file.name.endswith(".fasta"):
        sequence_lengths = [len(seq) for seq in sequences.values()]
        with col1:
            st.metric(label="🔗 Secuencias Cargadas", value=len(sequences))
        with col2:
            st.metric(label="📏 Longitud Promedio", value=f"{np.mean(sequence_lengths):.2f}")
        with col3:
            st.metric(label="📈 Longitud Máxima", value=max(sequence_lengths))
    elif uploaded_file.name.endswith(".csv"):
        with col1:
            st.metric(label="🔢 Columnas Numéricas", value=len(data.select_dtypes(include='number').columns))
        with col2:
            st.metric(label="🔍 Filas Totales", value=len(data))
        with col3:
            st.metric(label="📊 Columnas Totales", value=len(data.columns))

# Visualizaciones
st.header("📈 Visualizaciones Interactivas")

if uploaded_file:
    # Pestañas para diferentes análisis
    tab1, tab2, tab3 = st.tabs(["🔍 Estadísticas", "📊 Gráficos", "🧬 Herramientas Interactivas"])

    with tab1:
        st.subheader("🔍 Estadísticas Descriptivas")
        if uploaded_file.name.endswith(".csv"):
            st.write("**Estadísticas del archivo CSV:**")
            st.dataframe(data.describe())
        elif uploaded_file.name.endswith(".fasta"):
            st.write("**Estadísticas de secuencias FASTA:**")
            sequence_lengths = [len(seq) for seq in sequences.values()]
            st.write(f"- Longitud mínima: {min(sequence_lengths)}")
            st.write(f"- Longitud promedio: {np.mean(sequence_lengths):.2f}")
            st.write(f"- Longitud máxima: {max(sequence_lengths)}")

    with tab2:
        st.subheader("📊 Gráficos Interactivos")
        if uploaded_file.name.endswith(".csv"):
            numeric_columns = data.select_dtypes(include="number").columns
            if numeric_columns.any():
                selected_column = st.selectbox(
                    "Selecciona una columna numérica para visualizar:",
                    numeric_columns
                )
                fig = px.histogram(
                    data,
                    x=selected_column,
                    title=f"Distribución de {selected_column}",
                    color_discrete_sequence=["#FFA07A"]
                )
                st.plotly_chart(fig)
            else:
                st.warning("No hay columnas numéricas disponibles.")
        elif uploaded_file.name.endswith(".fasta"):
            fig = px.histogram(
                x=sequence_lengths,
                nbins=20,
                labels={"x": "Longitud de Secuencia", "y": "Frecuencia"},
                title="Distribución de Longitudes de Secuencia",
                color_discrete_sequence=["#66CDAA"]
            )
            st.plotly_chart(fig)

    with tab3:
        st.subheader("🧬 Herramientas Interactivas")
        if uploaded_file.name.endswith(".fasta"):
            selected_tool = st.selectbox(
                "Selecciona una herramienta para analizar tus secuencias:",
                ["Alineación", "Predicción de Estructuras", "Búsqueda de Motivos"]
            )
            if selected_tool == "Búsqueda de Motivos":
                motivos = ["ATG", "TATA", "CCGG"]
                frecuencias = {motivo: sum(seq.count(motivo) for seq in sequences.values()) for motivo in motivos}
                st.write("**Resultados de búsqueda:**")
                st.table(pd.DataFrame(frecuencias.items(), columns=["Motivo", "Frecuencia"]))

st.sidebar.markdown("---")
st.sidebar.write("💻 Desarrollado por [Yoleth Barrios y Lucero Ramos]")
