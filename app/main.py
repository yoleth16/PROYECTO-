import streamlit as st
import pandas as pd
from Bio import SeqIO
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import base64
import io
import uuid
import os

# Función para cargar datos del archivo FASTA
def load_fasta(file):
    try:
        # Lee el contenido del archivo como string
        content = file.getvalue().decode("utf-8")
        
        # Escribe el contenido a un archivo temporal
        temp_filepath = f"/tmp/{uuid.uuid4()}.fasta"
        with open(temp_filepath, "w") as f:
            f.write(content)
        
        # Lee el archivo temporal usando Bio.SeqIO
        sequences = list(SeqIO.parse(temp_filepath, "fasta"))
        
        # Elimina el archivo temporal
        os.remove(temp_filepath)
        
        return sequences
    except Exception as e:
        st.error(f"Error al cargar el archivo FASTA: {str(e)}")
        return None

# Función para calcular indicadores de secuencia
def calculate_sequence_indicators(sequence):
    if sequence is None or len(sequence) == 0:
        return None
    
    length = len(sequence.seq)
    gc_content = (sequence.seq.count('G') + sequence.seq.count('C')) / length * 100
    at_content = (sequence.seq.count('A') + sequence.seq.count('T')) / length * 100
    gc_ratio = gc_content / 100
    at_ratio = at_content / 100
    
    return {
        'length': length,
        'gc_content': gc_content,
        'at_content': at_content,
        'gc_ratio': gc_ratio,
        'at_ratio': at_ratio
    }

# Función para crear gráfico de contenido GC y AT
def plot_gc_at_content(indicators):
    if indicators is None:
        return
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x=['GC', 'AT'], y=[indicators['gc_ratio'] * 100, indicators['at_ratio'] * 100], ax=ax)
    
    ax.set_title('Contenido de GC y AT')
    ax.set_xlabel('Tipo de nucleótido')
    ax.set_ylabel('Porcentaje')
    
    st.pyplot(fig)

# Función para crear gráfico de longitud de secuencia
def plot_sequence_length(indicators):
    if indicators is None:
        return
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=[indicators['length']], kde=True, ax=ax)
    
    ax.set_title('Longitud de la secuencia')
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Frecuencia')
    
    st.pyplot(fig)

# Función para mostrar los resultados
def display_results(sequences, indicators):
    st.subheader("Análisis de Secuencias")
    
    if sequences is None:
        st.warning("No se pudieron cargar las secuencias del archivo FASTA.")
        return
    
    # Mostrar información general de las secuencias
    st.write("# Información General de las Secuencias")
    st.write(f"Total de secuencias: {len(sequences)}")
    
    # Calcular indicadores para cada secuencia
    sequence_indicators = [calculate_sequence_indicators(seq) for seq in sequences]
    
    # Crear DataFrame con los indicadores
    df = pd.DataFrame(sequence_indicators)
    
    # Mostrar datos en una tabla
    st.dataframe(df)
    
    # Permitir al usuario elegir qué gráficos ver
    graph_options = ['Gráfico de contenido GC y AT', 'Gráfico de longitud de secuencia']
    selected_graphs = st.multiselect("Elegir gráficos para visualizar", graph_options)
    
    if 'Gráfico de contenido GC y AT' in selected_graphs:
        plot_gc_at_content(df.iloc[0])
    
    if 'Gráfico de longitud de secuencia' in selected_graphs:
        plot_sequence_length(df.iloc[0])

# Título de la aplicación
st.title("Análisis de Secuencias FASTA")

# Subir archivo FASTA
uploaded_file = st.file_uploader("Subir un archivo FASTA", type="fasta")

if uploaded_file is not None:
    sequences = load_fasta(uploaded_file)

    if sequences is not None:
        indicators = calculate_sequence_indicators(sequences[0])
        
        display_results(sequences, indicators)
    else:
        st.warning("No se pudo cargar el archivo FASTA.")

# Mostrar indicadores en una tabla si hay datos
if indicators is not None:
    st.write("# Indicadores")
    st.dataframe(pd.DataFrame([indicators]))
