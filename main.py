import streamlit as st

file_path = "source/plantilla_cursos.xlsx"

with open(file_path, "rb") as file:
    file_bytes = file.read()

# Botón de plantilla
st.download_button(
    label="Descargar plantilla",
    data=file_bytes,
    file_name="plantilla_cursos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
