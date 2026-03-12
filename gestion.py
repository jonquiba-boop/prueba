import streamlit as st
import pandas as pd
import os

# Configuración básica
st.set_page_config(page_title="Sistema de Gestión", layout="wide")

# Forzar la ruta del archivo Excel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_EXCEL = os.path.join(BASE_DIR, 'base_datos.xlsx')

st.title("🚀 Sistema de Gestión de Cartera")

# Intentar cargar los datos
try:
    if os.path.exists(ARCHIVO_EXCEL):
        df = pd.read_excel(ARCHIVO_EXCEL)
        st.success("Base de datos cargada correctamente")
        
        # Buscador sencillo
        busqueda = st.text_input("Buscar cliente por nombre:")
        if busqueda:
            resultado = df[df.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)]
            st.dataframe(resultado)
    else:
        st.error(f"No encuentro el archivo: {ARCHIVO_EXCEL}. Asegúrate de que se llame exactamente así en GitHub.")
except Exception as e:
    st.error(f"Error al leer el Excel: {e}")
