import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

st.set_page_config(page_title="Gestión BBVA - Profesional", layout="wide")

def mostrar_historial_real(cedula_cliente):
    try:
        # Cargamos la SEGUNDA pestaña (índice 1) sin importar el nombre
        df_hist = pd.read_excel(ARCHIVO_EXCEL, sheet_name=1)
        
        # Limpiamos nombres de columnas y datos
        df_hist.columns = [str(c).strip().upper() for c in df_hist.columns]
        
        # Buscamos la columna de cédula (que en tu historial es la segunda, índice 1)
        col_cedula_hist = df_hist.columns[1] 
        
        df_hist[col_cedula_hist] = df_hist[col_cedula_hist].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        cedula_target = str(cedula_cliente).strip().replace('.0', '')
        
        pasado = df_hist[df_hist[col_cedula_hist] == cedula_target]
        
        if not pasado.empty:
            st.divider()
            st.subheader("📜 Historial de Gestiones (Columnas C a L)")
            # Seleccionamos de la C a la L (índices 2 al 11)
            detalle = pasado.iloc[:, 2:12] 
            st.dataframe(detalle, use_container_width=True, hide_index=True)
        else:
            st.info(f"No hay historial para la cédula {cedula_target} en la segunda pestaña.")
    except Exception as e:
        st.error(f"Error al leer la segunda pestaña del Excel: {e}")

# --- INTERFAZ ---
st.title("⚖️ Sistema de Gestión de Cartera BBVA")

if os.path.exists(ARCHIVO_EXCEL):
    # Cargamos la PRIMERA pestaña (índice 0)
    df_cartera = pd.read_excel(ARCHIVO_EXCEL, sheet_name=0)
    
    busqueda = st.text_input("🔍 Buscar por Cédula o Nombre:")
    
    if busqueda:
        mask = df_cartera.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)
        resultados = df_cartera[mask]
        
        if not resultados.empty:
            idx = st.selectbox("Seleccione el registro:", resultados.index)
            cliente_sel = df_cartera.loc[idx]
            
            # Buscamos la cédula en la base principal (columna 'No cedula')
            cedula_id = cliente_sel['No cedula']
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📋 Datos del Cliente")
                st.write(cliente_sel)
            with col2:
                st.subheader("✍️ Registrar Gestión")
                st.text_area("Nueva Observación")
                st.button("💾 Guardar")
            
            # Ejecutamos el historial
            mostrar_historial_real(cedula_id)
        else:
            st.warning("No se encontraron resultados.")
else:
    st.error(f"No se encuentra el archivo '{ARCHIVO_EXCEL}' en GitHub.")
