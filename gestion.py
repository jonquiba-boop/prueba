import streamlit as st
import pandas as pd
import os

# CONFIGURACIÓN DEL NOMBRE EXACTO
# Debe ser idéntico al que subiste a GitHub
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

st.set_page_config(page_title="Gestión BBVA", layout="wide")

st.title("📊 Sistema de Gestión - Base BBVA")

if os.path.exists(ARCHIVO_EXCEL):
    try:
        # Cargamos el Excel
        df = pd.read_excel(ARCHIVO_EXCEL)
        st.success("✅ Base de datos conectada con éxito")
        
        # Buscador por cédula o nombre
        busqueda = st.text_input("🔍 Buscar en la base consolidada:")
        if busqueda:
            # Filtramos en todas las columnas
            mask = df.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)
            df_filtrado = df[mask]
            st.dataframe(df_filtrado)
        else:
            st.write("Escribe un nombre o identificación para empezar.")
            
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.error(f"⚠️ No se encontró el archivo '{ARCHIVO_EXCEL}'. Verifica el nombre en GitHub.")
