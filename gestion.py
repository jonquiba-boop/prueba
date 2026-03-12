import streamlit as st
import pandas as pd
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Free Management - Gestor de Cartera", layout="wide")

st.title("⚖️ Sistema de Gestión de Cartera - BBVA")
st.markdown("---")

# --- 1. CARGADOR DE ARCHIVO ---
st.sidebar.header("📁 Configuración de Base de Datos")
archivo_subido = st.sidebar.file_saver = st.sidebar.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])

# Usamos una función para procesar el archivo, ya sea el subido o el de GitHub
def cargar_datos():
    if archivo_subido is not None:
        return pd.ExcelFile(archivo_subido)
    elif os.path.exists('BASE CONSOLIDADA BBVA.xlsx'):
        return pd.ExcelFile('BASE CONSOLIDADA BBVA.xlsx')
    return None

import os
excel_data = cargar_datos()

# --- 2. LÓGICA DE HISTORIAL ---
def mostrar_historial_bloque(excel, cedula_cliente):
    try:
        # Intentamos leer la segunda pestaña (índice 1)
        if len(excel.sheet_names) < 2:
            st.warning("⚠️ El archivo cargado solo tiene una pestaña. El historial debe estar en la segunda hoja.")
            return

        df_hist = excel.parse(sheet_name=1)
        
        # Limpieza de columnas
        df_hist.columns = [str(c).strip().upper() for c in df_hist.columns]
        
        # Identificamos la columna de cédula (normalmente la 2da, índice 1)
        col_id = df_hist.columns[1]
        
        # Normalización para el match
        df_hist[col_id] = df_hist[col_id].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        cedula_target = str(cedula_cliente).strip().replace('.0', '')
        
        pasado = df_hist[df_hist[col_id] == cedula_target]
        
        if not pasado.empty:
            st.divider()
            st.subheader("📜 Historial de Gestiones (Columnas C a L)")
            # Mostramos de la C a la L (índices 2 al 11)
            st.dataframe(pasado.iloc[:, 2:12], use_container_width=True, hide_index=True)
        else:
            st.info(f"Sin registros previos para la cédula {cedula_target}.")
    except Exception as e:
        st.error(f"Error al procesar historial: {e}")

# --- 3. INTERFAZ PRINCIPAL ---
if excel_data:
    # Cargamos la primera pestaña para la búsqueda
    df_principal = excel_data.parse(sheet_name=0)
    
    busqueda = st.text_input("🔍 Buscar deudor (Cédula o Nombre):")
    
    if busqueda:
        mask = df_principal.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)
        resultados = df_principal[mask]
        
        if not resultados.empty:
            idx = st.selectbox("Seleccione el cliente:", resultados.index)
            cliente_sel = df_principal.loc[idx]
            
            # Buscamos la cédula (ajusta el nombre si es distinto en tu base principal)
            cedula_id = cliente_sel.get('No cedula', cliente_sel.get('CEDULA', cliente_sel[0]))
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📋 Información del Cliente")
                st.write(cliente_sel)
            with c2:
                st.subheader("✍️ Registro de Gestión")
                st.text_area("Observaciones de la gestión actual")
                if st.button("💾 Registrar"):
                    st.balloons()
                    st.success("Gestión visualizada correctamente.")
            
            # Mostramos el historial desde el objeto excel_data
            mostrar_historial_bloque(excel_data, cedula_id)
        else:
            st.error("No se encontró el deudor.")
else:
    st.info("👋 Bienvenido. Por favor, sube tu archivo Excel en la barra lateral para comenzar.")
