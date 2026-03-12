import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

st.set_page_config(page_title="Free Management - Gestión BBVA", layout="wide")

st.title("⚖️ Sistema de Gestión de Cartera - BBVA")

# Función mejorada para limpiar IDs
def limpiar_id(dato):
    if pd.isna(dato): return ""
    # Quita espacios, .0 al final y convierte a texto
    return str(dato).strip().split('.')[0]

if os.path.exists(ARCHIVO_EXCEL):
    try:
        excel_completo = pd.ExcelFile(ARCHIVO_EXCEL)
        df_principal = excel_completo.parse(0) # Hoja 1: Cartera
        
        # --- BUSCADOR ---
        busqueda = st.text_input("🔍 Ingrese Cédula del deudor:")
        
        if busqueda:
            busqueda_clean = limpiar_id(busqueda)
            
            # Buscamos en la columna 'No cedula' que es la de tu archivo
            # Si no la encuentra por nombre, busca en la segunda columna (índice 1)
            col_id_nombre = 'No cedula' if 'No cedula' in df_principal.columns else df_principal.columns[1]
            
            # Creamos una copia temporal de la columna limpia para comparar
            col_comparar = df_principal[col_id_nombre].apply(limpiar_id)
            
            # Filtramos
            resultados = df_principal[col_comparar == busqueda_clean]
            
            if not resultados.empty:
                idx = st.selectbox("Seleccione el deudor:", resultados.index)
                cliente = df_principal.loc[idx]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📋 Información del Cliente")
                    st.write(cliente)
                
                with col2:
                    st.subheader("✍️ Registro de Gestión")
                    st.text_area("Nueva Observación")
                    st.button("💾 Guardar")

                # --- HISTORIAL (Hoja 2) ---
                if len(excel_completo.sheet_names) > 1:
                    df_hist = excel_completo.parse(1)
                    # Limpiamos nombres de columnas
                    df_hist.columns = [str(c).strip() for c in df_hist.columns]
                    
                    # En el historial la columna se llama 'CEDULA' (es la segunda columna)
                    col_id_hist = 'CEDULA' if 'CEDULA' in df_hist.columns else df_hist.columns[1]
                    
                    hist_comparar = df_hist[col_id_hist].apply(limpiar_id)
                    pasado = df_hist[hist_comparar == busqueda_clean]
                    
                    if not pasado.empty:
                        st.divider()
                        st.subheader("📜 Historial de Gestiones (Columnas C a L)")
                        st.dataframe(pasado.iloc[:, 2:12], use_container_width=True, hide_index=True)
                    else:
                        st.info(f"Cédula {busqueda_clean} no tiene gestiones registradas en el historial.")
                else:
                    st.warning("El Excel no tiene pestaña de historial.")
            else:
                st.error(f"No se encontró el deudor con cédula: {busqueda_clean}")
                # Debug para el abogado: muestra qué columnas encontró
                # st.write("Columnas detectadas:", list(df_principal.columns))
                
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.error(f"No se encuentra el archivo '{ARCHIVO_EXCEL}' en GitHub.")
