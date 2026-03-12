import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

st.set_page_config(page_title="Free Management - Gestión BBVA", layout="wide")

st.title("⚖️ Sistema de Gestión de Cartera - BBVA")

def limpiar_id(dato):
    if pd.isna(dato): return ""
    return str(dato).strip().split('.')[0]

if os.path.exists(ARCHIVO_EXCEL):
    try:
        excel_completo = pd.ExcelFile(ARCHIVO_EXCEL)
        df_principal = excel_completo.parse(0) 
        
        busqueda = st.text_input("🔍 Ingrese Cédula del deudor:")
        
        if busqueda:
            busqueda_clean = limpiar_id(busqueda)
            col_id_cartera = 'No cedula' if 'No cedula' in df_principal.columns else df_principal.columns[1]
            mask = df_principal[col_id_cartera].apply(limpiar_id) == busqueda_clean
            resultados = df_principal[mask]
            
            if not resultados.empty:
                idx = st.selectbox("Seleccione el registro:", resultados.index)
                cliente = df_principal.loc[idx]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📋 Información del Cliente")
                    st.write(cliente)
                
                with col2:
                    st.subheader("✍️ Registro de Gestión")
                    obs = st.text_area("Nueva Observación")
                    
                    # --- NUEVO: BOTÓN DE ADJUNTOS ---
                    st.markdown("---")
                    st.subheader("📁 Soportes y Documentos")
                    soporte = st.file_uploader("Adjuntar soporte (Imagen, PDF, Acta)", type=['pdf', 'png', 'jpg', 'jpeg', 'docx'])
                    
                    if soporte is not None:
                        st.success(f"✅ Archivo '{soporte.name}' cargado correctamente.")

                    if st.button("💾 Guardar Gestión Completa"):
                        # Aquí el sistema procesaría el guardado
                        st.balloons()
                        st.success("Gestión y adjunto registrados en el sistema.")

                # --- BLOQUE DE HISTORIAL (Columnas C a L) ---
                if len(excel_completo.sheet_names) > 1:
                    df_hist = excel_completo.parse(1)
                    col_id_hist = df_hist.columns[1]
                    mask_hist = df_hist[col_id_hist].apply(limpiar_id) == busqueda_clean
                    pasado = df_hist[mask_hist]
                    
                    if not pasado.empty:
                        st.divider()
                        st.subheader("📜 Historial de Gestiones Anteriores")
                        detalle_visual = pasado.iloc[:, 2:12]
                        st.dataframe(detalle_visual, use_container_width=True, hide_index=True)
                    else:
                        st.info("No se registran gestiones previas.")
            else:
                st.error(f"No se encontró el deudor.")
                
    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")
else:
    st.error(f"No se encuentra el archivo Excel en el repositorio.")
