import streamlit as st
import pandas as pd

col1, col2 = st.columns(2)
with col1:
    file_path = "source/plantilla_cursos.xlsx"
    with open(file_path, "rb") as file:
        file_bytes = file.read()
    
    st.download_button(
        label="Descargar plantilla",
        data=file_bytes,
        file_name="plantilla_cursos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col2:
    uploaded_file = st.file_uploader("Subir archivo", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Detectar el tipo de archivo y convertirlo en un DataFrame
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        st.write("Vista previa del archivo:")
        st.dataframe(df)  # Mostrar el DataFrame
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
