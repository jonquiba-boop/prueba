import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

st.set_page_config(page_title="Free Management - Gestión BBVA", layout="wide")

st.title("⚖️ Sistema de Gestión de Cartera - BBVA")

# Función para limpiar cédulas (el problema de los .0)
def limpiar_id(dato):
    return str(dato).strip().replace('.0', '')

# --- PROCESO PRINCIPAL ---
if os.path.exists(ARCHIVO_EXCEL):
    # Intentamos cargar el archivo completo
    try:
        excel_completo = pd.ExcelFile(ARCHIVO_EXCEL)
        
        # Cargamos la Cartera (Hoja 1)
        df_principal = excel_completo.parse(0)
        
        busqueda = st.text_input("🔍 Ingrese Cédula para buscar:")
        
        if busqueda:
            # Limpiamos la búsqueda del usuario
            busqueda_clean = limpiar_id(busqueda)
            
            # Buscamos en todas las columnas por si acaso
            mask = df_principal.astype(str).apply(lambda x: busqueda_clean in x.str.strip().values, axis=1)
            resultados = df_principal[mask]
            
            if not resultados.empty:
                idx = st.selectbox("Seleccione el deudor:", resultados.index)
                cliente = df_principal.loc[idx]
                
                # Identificamos la cédula del cliente seleccionado
                # Probamos con los nombres de columna que tienes en tu Excel
                cedula_cliente = cliente.get('No cedula', cliente.get('CEDULA', cliente[0]))
                cedula_cliente_clean = limpiar_id(cedula_cliente)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📋 Información Actual")
                    st.write(cliente)
                
                with col2:
                    st.subheader("✍️ Registro de Gestión")
                    st.text_area("Observaciones")
                    st.button("💾 Guardar Gestión")

                # --- MOSTRAR HISTORIAL (Hoja 2) ---
                if len(excel_completo.sheet_names) > 1:
                    df_hist = excel_completo.parse(1)
                    # Limpiamos nombres de columnas del historial
                    df_hist.columns = [str(c).strip().upper() for c in df_hist.columns]
                    
                    # Buscamos la columna de cédula en el historial (suele ser la 2da)
                    col_id_hist = df_hist.columns[1]
                    df_hist[col_id_hist] = df_hist[col_id_hist].apply(limpiar_id)
                    
                    pasado = df_hist[df_hist[col_id_hist] == cedula_cliente_clean]
                    
                    if not pasado.empty:
                        st.divider()
                        st.subheader("📜 Historial de Gestiones Anteriores (C a L)")
                        st.dataframe(pasado.iloc[:, 2:12], use_container_width=True, hide_index=True)
                    else:
                        st.info("No se encontró historial previo para esta cédula.")
                else:
                    st.warning("El archivo Excel solo tiene una pestaña. No se puede mostrar el historial.")
            else:
                st.error("No se encontró ningún deudor con esa cédula.")
                
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.error(f"No se encuentra el archivo '{ARCHIVO_EXCEL}' en GitHub. Por favor, súbelo.")
