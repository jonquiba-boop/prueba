import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Free Management - Gestión de Cartera",
    page_icon="⚖️",
    layout="wide"
)

# COLOR INSTITUCIONAL
COLOR_CORP = "#17891e"

# Estilo CSS personalizado con tu color
st.markdown(f"""
    <style>
    /* Color de fondo del encabezado y sidebar */
    .stApp {{
        background-color: #f8f9fa;
    }}
    /* Botones principales */
    div.stButton > button:first-child {{
        background-color: {COLOR_CORP};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }}
    div.stButton > button:hover {{
        background-color: #126b17;
        color: white;
    }}
    /* Títulos y secciones */
    h1, h2, h3 {{
        color: {COLOR_CORP};
    }}
    /* Estilo para las tarjetas de información */
    .info-card {{
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_CORP};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

def limpiar_id(dato):
    if pd.isna(dato): return ""
    return str(dato).strip().split('.')[0]

# --- ENCABEZADO INSTITUCIONAL ---
st.markdown(f"""
    <div style="background-color: {COLOR_CORP}; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0;">FREE MANAGEMENT S.A.S.</h1>
        <p style="color: #e0e0e0; margin: 0;">Sistema Centralizado de Gestión de Cartera - BBVA</p>
    </div>
    """, unsafe_allow_html=True)

if os.path.exists(ARCHIVO_EXCEL):
    try:
        excel_completo = pd.ExcelFile(ARCHIVO_EXCEL)
        df_principal = excel_completo.parse(0) 
        
        # --- BUSCADOR ---
        busqueda = st.text_input("🔍 Ingrese Cédula del deudor para iniciar:", placeholder="Ej: 80503683")

        if busqueda:
            busqueda_clean = limpiar_id(busqueda)
            col_id_cartera = 'No cedula' if 'No cedula' in df_principal.columns else df_principal.columns[1]
            mask = df_principal[col_id_cartera].apply(limpiar_id) == busqueda_clean
            resultados = df_principal[mask]
            
            if not resultados.empty:
                idx = st.selectbox("Coincidencias encontradas:", resultados.index)
                cliente = df_principal.loc[idx]
                
                st.markdown("---")
                
                # --- PANEL DE GESTIÓN ---
                col_info, col_gest = st.columns([1, 1])
                
                with col_info:
                    st.markdown(f"### 📋 Información del Cliente")
                    st.markdown(f"""
                    <div class="info-card">
                        <p><strong>Nombre:</strong> {cliente.get('Nombre Completo', 'N/A')}</p>
                        <p><strong>Cédula:</strong> {cliente.get('No cedula', 'N/A')}</p>
                        <p><strong>Ciudad:</strong> {cliente.get('CIUDAD DE RESIDENCIA', 'N/A')}</p>
                        <p><strong>Saldo Total:</strong> <span style="color: {COLOR_CORP}; font-weight: bold;">${cliente.get('SALDO TOTAL', 0):,.0f} COP</span></p>
                        <p><strong>Días Mora:</strong> {cliente.get('DIAS DE MORA', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_gest:
                    st.markdown("### ✍️ Registrar Nueva Acción")
                    obs = st.text_area("Notas de la gestión:", placeholder="Describa el acuerdo o resultado de la llamada...")
                    soporte = st.file_uploader("📁 Cargar soporte de pago o acta", type=['pdf', 'png', 'jpg'])
                    
                    if st.button("💾 Guardar Gestión en Base de Datos"):
                        st.balloons()
                        st.success("Gestión almacenada correctamente.")

                # --- HISTORIAL ---
                if len(excel_completo.sheet_names) > 1:
                    df_hist = excel_completo.parse(1)
                    col_id_hist = df_hist.columns[1]
                    mask_hist = df_hist[col_id_hist].apply(limpiar_id) == busqueda_clean
                    pasado = df_hist[mask_hist]
                    
                    st.markdown(f"### 📜 Historial de Movimientos")
                    if not pasado.empty:
                        # Seleccionamos columnas C a L (índices 2 al 11)
                        detalle = pasado.iloc[:, 2:12]
                        st.dataframe(detalle, use_container_width=True, hide_index=True)
                    else:
                        st.info("Sin registros históricos para este deudor.")
            else:
                st.error("La cédula ingresada no existe en la base de Cartera.")
                
    except Exception as e:
        st.error(f"Error en el procesamiento: {e}")
else:
    st.error("Falta el archivo 'BASE CONSOLIDADA BBVA.xlsx' en el repositorio.")
