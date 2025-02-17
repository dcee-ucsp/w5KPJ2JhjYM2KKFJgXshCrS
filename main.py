import streamlit as st
import pandas as pd
from datetime import datetime, time

st.title("Coincidencias de horarios")

col1, col2 = st.columns(2)
with col1:
    file_path = "source/plantilla_cursos.xlsx"
    with open(file_path, "rb") as file:
        file_bytes = file.read()
    
    st.download_button(
        label="Descargar plantilla de base de cursos",
        data=file_bytes,
        file_name="plantilla_cursos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col2:
    uploaded_file = st.file_uploader("Subir base de cursos", type=["xlsx", "csv"])

df = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        expected_columns = ['Materia', 'Grupo', 'Docente', 'Dia', 'Inicia', 'Fin']
        if not all(col in df.columns for col in expected_columns):
            st.error("El archivo cargado no tiene las columnas requeridas. Por favor, sube el archivo con la plantilla adecuada.")
            df = None  # Reiniciar df para no permitir continuar

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

def convertir_hora(hora):
    try:
        return datetime.strptime(hora, "%I:%M %p").time()
    except ValueError:
        return datetime.strptime(hora, "%H:%M").time()

def superposicion_horas(inicio_clase, fin_clase, inicio_filtro, fin_filtro):
    return not (fin_clase < inicio_filtro or inicio_clase > fin_filtro)

def dentro_del_rango(inicio_clase, fin_clase, inicio_filtro, fin_filtro):
    return inicio_clase >= inicio_filtro and fin_clase <= fin_filtro

def aplicar_filtro(df, hora_inicio, hora_fin, dias_seleccionados):
    df['Inicia'] = df['Inicia'].apply(convertir_hora)
    df['Fin'] = df['Fin'].apply(convertir_hora)
    
    hora_inicio = time(hora_inicio, 0)
    hora_fin = time(hora_fin, 0)
    
    df['Rango horas'] = df.apply(lambda row: 'Dentro del rango' if dentro_del_rango(row['Inicia'], row['Fin'], hora_inicio, hora_fin) else 'Fuera del rango', axis=1)
    df_filtrado = df[(df['Dia'].isin(dias_seleccionados)) & 
                      (df.apply(lambda row: superposicion_horas(row['Inicia'], row['Fin'], hora_inicio, hora_fin), axis=1))]
    df_filtrado = df_filtrado.sort_values(by=['Rango horas'])
    df_filtrado['Curso y grupo'] = df_filtrado['Materia'] + ' - ' + df_filtrado['Grupo']
    return df_filtrado

if df is not None:
    st.title("Filtro de Horarios")
    dias_seleccionados = st.multiselect("Selecciona los días", dias_opciones)
    hora_inicio = st.slider("Hora de inicio", 0, 7)
    hora_fin = st.slider("Hora de fin", 0, 22)

    if st.button("Filtrar Horarios"):
        df_resultado = aplicar_filtro(df, hora_inicio, hora_fin, dias_seleccionados)
        df_copia = df_resultado.copy()

        df_copia['correo'] = False
        df_copia['Curso y grupo'] = df_copia['Materia'] + ' - ' + df_copia['Grupo']
        df_copia['Docente'] = df_copia['Docente']
        df_copia['Rango horas'] = df_copia['Rango horas']
        df_copia['Día'] = df_copia['Dia']
        df_copia['Inicia'] = df_copia['Inicia']
        df_copia['Fin'] = df_copia['Fin']

        df_copia = df_copia[['correo', 'Curso y grupo', 'Docente', 'Rango horas', 'Día', 'Inicia', 'Fin']]

        st.data_editor(
            df_copia,
            column_config={
                "correo": st.column_config.CheckboxColumn(
                    "Correo",
                    help="Seleccionar para plantilla de correos",
                    default=False,
                )
            },
            disabled=["widgets"],
            hide_index=True,
        )
