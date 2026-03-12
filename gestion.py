import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Free Management - Gestión BBVA", layout="wide")
COLOR_CORP = "#17891e"
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

# Estilo CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f8f9fa; }}
    div.stButton > button:first-child {{
        background-color: {COLOR_CORP};
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }}
    h1, h2, h3 {{ color: {COLOR_CORP}; }}
    .info-card {{
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_CORP};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

def limpiar_id(dato):
    if pd.isna(dato): return ""
    return str(dato).strip().split('.')[0]

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_base_completa():
    if os.path.exists(ARCHIVO_EXCEL):
        excel = pd.ExcelFile(ARCHIVO_EXCEL)
        cartera = excel.parse(0)
        historial = excel.parse(1) if len(excel.sheet_names) > 1 else pd.DataFrame()
        return cartera, historial
    return None, None

df_cartera, df_historial_base = cargar_base_completa()

# Inicializar historial en la sesión para que sea "escribible"
if 'historial_dinamico' not in st.session_state and df_historial_base is not None:
    st.session_state.historial_dinamico = df_historial_base

# --- ENCABEZADO ---
st.markdown(f'<div style="background-color:{COLOR_CORP};padding:15px;border-radius:10px;text-align:center"><h1 style="color:white;margin:0">FREE MANAGEMENT S.A.S.</h1></div>', unsafe_allow_html=True)

if df_cartera is not None:
    busqueda = st.text_input("🔍 Buscar Cédula:", placeholder="Ingrese identificación...")

    if busqueda:
        busqueda_clean = limpiar_id(busqueda)
        col_id_cartera = 'No cedula' if 'No cedula' in df_cartera.columns else df_cartera.columns[1]
        
        resultado = df_cartera[df_cartera[col_id_cartera].apply(limpiar_id) == busqueda_clean]

        if not resultado.empty:
            cliente = resultado.iloc[0]
            
            col_info, col_gest = st.columns([1, 1])
            
            with col_info:
                st.markdown("### 📋 Datos del Deudor")
                st.markdown(f"""<div class="info-card">
                    <b>Nombre:</b> {cliente.get('Nombre Completo', 'N/A')}<br>
                    <b>Cédula:</b> {cliente.get('No cedula', 'N/A')}<br>
                    <b>Saldo:</b> ${cliente.get('SALDO TOTAL', 0):,.0f}<br>
                    <b>Días Mora:</b> {cliente.get('DIAS DE MORA', 'N/A')}
                </div>""", unsafe_allow_html=True)

            with col_gest:
                st.markdown("### ✍️ Nueva Gestión")
                nueva_obs = st.text_area("Observaciones:", height=80)
                adjunto = st.file_uploader("Adjuntar soporte", type=['pdf','jpg','png'])
                
                if st.button("💾 Registrar Gestión"):
                    # Crear nueva fila para el historial
                    nueva_fila = {
                        'CEDULA': busqueda_clean,
                        'FECHA': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'OBSERVACION': nueva_obs,
                        'ASESOR': "Gestor Actual", # Aquí puedes poner el nombre del abogado
                        'CALIFICACION1': "GESTIONADO"
                    }
                    # Insertar al principio del historial de la sesión
                    st.session_state.historial_dinamico = pd.concat([pd.DataFrame([nueva_fila]), st.session_state.historial_dinamico], ignore_index=True)
                    st.success("✅ Gestión añadida al historial local.")

            # --- HISTORIAL (Ordenado por lo más reciente) ---
            st.markdown("---")
            st.markdown("### 📜 Historial de Gestiones (Más reciente primero)")
            
            hist_temp = st.session_state.historial_dinamico
            col_id_hist = hist_temp.columns[1] # CEDULA
            
            # Filtrar historial por el cliente actual
            mask_hist = hist_temp[col_id_hist].apply(limpiar_id) == busqueda_clean
            final_hist = hist_temp[mask_hist]

            if not final_hist.empty:
                # Mostramos columnas de interés (C a L o similares)
                # Usamos .reset_index(drop=True) para que se vea limpio
                st.dataframe(final_hist.iloc[:, 0:12], use_container_width=True, hide_index=True)
            else:
                st.info("No hay gestiones previas registradas.")

else:
    st.error("No se pudo cargar la base de datos.")
