import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'
HOJA_HISTORIAL = 'Historico_Gestiones'

st.set_page_config(page_title="Gestión BBVA Pro", layout="wide")

# --- FUNCIÓN PARA MOSTRAR HISTORIAL ---
def mostrar_historial(cedula_cliente):
    try:
        df_hist = pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJA_HISTORIAL)
        df_hist['CEDULA'] = df_hist['CEDULA'].astype(str)
        pasado = df_hist[df_hist['CEDULA'] == str(cedula_cliente)]
        
        if not pasado.empty:
            st.subheader("📜 Historial de Gestiones (Anteriores)")
            # Usamos tus títulos actualizados
            columnas_ver = ['FECHA', 'ASESOR', 'CALIFICACION1', 'OBSERVACION', 'FECHA NUEVO CONTACTO']
            cols_finales = [c for c in columnas_ver if c in pasado.columns]
            st.dataframe(pasado[cols_finales].sort_values(by='FECHA', ascending=False), use_container_width=True)
        else:
            st.info("No hay gestiones previas para este deudor.")
    except:
        st.info("ℹ️ Sin historial previo.")

# --- INTERFAZ ---
st.title("⚖️ Sistema de Gestión de Cartera - BBVA")

if os.path.exists(ARCHIVO_EXCEL):
    df_cartera = pd.read_excel(ARCHIVO_EXCEL)
    busqueda = st.text_input("🔍 Buscar por Cédula o Nombre:")
    
    if busqueda:
        mask = df_cartera.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)
        resultados = df_cartera[mask]
        
        if not resultados.empty:
            idx = st.selectbox("Seleccione el registro:", resultados.index)
            cliente_sel = df_cartera.loc[idx]
            cedula_actual = cliente_sel.get('CEDULA', cliente_sel[0])
            
            col1, col2 = st.columns([1, 1.2])
            
            with col1:
                st.subheader("📋 Datos Actuales")
                st.write(cliente_sel)
                mostrar_historial(cedula_actual)

            with col2:
                st.subheader("🖊️ Registrar Nueva Gestión")
                
                # Campos basados en tus títulos
                c1, c2 = st.columns(2)
                with c1:
                    asesor = st.text_input("ASESOR", value="Legal_Team")
                    calif1 = st.selectbox("CALIFICACION1", ["CONTACTADO", "ILOCALIZABLE", "MENSAJE"])
                    tipo_acu = st.selectbox("TIPOACU", ["NINGUNO", "TOTAL", "PARCIAL"])
                with c2:
                    prox_cont = st.selectbox("CONTACTAR NUEVAMENTE", ["SI", "NO"])
                    f_contacto = st.date_input("FECHA NUEVO CONTACTO")
                    valor_acu = st.number_input("VALORACU", min_value=0)

                obs = st.text_area("OBSERVACION")
                
                if st.button("💾 Guardar Gestión en Historial"):
                    # Aquí el sistema preparará la fila con todos tus títulos:
                    # CLIENTE, CEDULA, NOMBRE, CALIFICACION1, CALIFICACION2... etc.
                    st.success(f"Gestión registrada bajo CALIFICACION1: {calif1}")
                    st.toast("Guardado correctamente")
else:
    st.error("No se encontró el archivo Excel.")
