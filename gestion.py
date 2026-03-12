import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

st.set_page_config(page_title="Gestión BBVA - Profesional", layout="wide")

def mostrar_historial_real(cedula_cliente):
    try:
        # Cargamos la pestaña de historial (Hoja 2)
        df_hist = pd.read_excel(ARCHIVO_EXCEL, sheet_name='Historico_Gestiones')
        
        # Normalizamos la columna CEDULA en el historial
        df_hist['CEDULA'] = df_hist['CEDULA'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        cedula_target = str(cedula_cliente).strip().replace('.0', '')
        
        # Filtramos
        pasado = df_hist[df_hist['CEDULA'] == cedula_target]
        
        if not pasado.empty:
            st.divider()
            st.subheader("📜 Historial de Gestiones (Columnas C a L)")
            
            # Según tu archivo, de la C a la L son los resultados y observaciones
            # Seleccionamos las columnas por posición para no fallar por nombres
            detalle = pasado.iloc[:, 2:12] 
            
            st.dataframe(detalle, use_container_width=True, hide_index=True)
        else:
            st.info(f"No se encontraron gestiones previas para la cédula {cedula_target} en la base de datos.")
    except Exception as e:
        st.error("Asegúrate de que la pestaña se llame 'Historico_Gestiones' en tu Excel.")

# --- INTERFAZ ---
st.title("⚖️ Sistema de Gestión de Cartera BBVA")

if os.path.exists(ARCHIVO_EXCEL):
    # Cargamos Cartera (Hoja 1)
    df_cartera = pd.read_excel(ARCHIVO_EXCEL, sheet_name=0)
    
    busqueda = st.text_input("🔍 Buscar por Cédula o Nombre:")
    
    if busqueda:
        # Buscamos en toda la tabla
        mask = df_cartera.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)
        resultados = df_cartera[mask]
        
        if not resultados.empty:
            idx = st.selectbox("Seleccione el registro:", resultados.index)
            cliente_sel = df_cartera.loc[idx]
            
            # USAMOS EL NOMBRE REAL DE TU COLUMNA: 'No cedula'
            cedula_id = cliente_sel['No cedula']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Datos Actuales")
                st.write(cliente_sel)
            
            with col2:
                st.subheader("✍️ Registrar Gestión")
                obs = st.text_area("Nueva Observación")
                if st.button("💾 Guardar"):
                    st.success("Gestión registrada")
            
            # Mostramos el historial usando la cédula extraída
            mostrar_historial_real(cedula_id)
        else:
            st.warning("No se encontraron resultados.")
else:
    st.error("No se encontró el archivo 'BASE CONSOLIDADA BBVA.xlsx'.")
