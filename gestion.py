import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'
HOJA_HISTORIAL = 'Historico_Gestiones'

st.set_page_config(page_title="Gestión de Cartera Pro", layout="wide")

# --- FUNCIÓN DE HISTORIAL CON LIMPIEZA DE DATOS ---
def mostrar_historial_bloque(cedula_cliente):
    try:
        # 1. Leer historial
        df_hist = pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJA_HISTORIAL)
        
        # 2. Limpieza de nombres de columnas (quitar espacios y poner en mayúsculas)
        df_hist.columns = [str(c).strip().upper() for c in df_hist.columns]
        
        # 3. Normalización de Cédulas (Crucial para que el match funcione)
        # Convertimos ambas a string, quitamos decimales (.0) y espacios
        df_hist['CEDULA'] = df_hist['CEDULA'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        cedula_target = str(cedula_cliente).replace('.0', '').strip()
        
        # 4. Filtrar
        pasado = df_hist[df_hist['CEDULA'] == cedula_target]
        
        if not pasado.empty:
            st.divider()
            st.subheader(f"📜 Historial Detallado (Columnas C a L)")
            # Seleccionamos columnas de la 3ra (índice 2) a la 12va (índice 11)
            detalle = pasado.iloc[:, 2:12]
            st.dataframe(detalle, use_container_width=True, hide_index=True)
        else:
            st.info(f"No se encontró historial para la cédula: {cedula_target}")
            # Línea de depuración opcional para que veas qué hay en el Excel:
            # st.write("Primeras 5 cédulas en historial:", df_hist['CEDULA'].head().tolist())
            
    except Exception as e:
        st.warning(f"Aviso: Verifica que la pestaña se llame '{HOJA_HISTORIAL}'. Error: {e}")

# --- INTERFAZ ---
st.title("⚖️ Panel de Gestión de Cartera - BBVA")

if os.path.exists(ARCHIVO_EXCEL):
    df_principal = pd.read_excel(ARCHIVO_EXCEL)
    
    busqueda = st.text_input("🔍 Buscar por Cédula o Nombre:")
    
    if busqueda:
        mask = df_principal.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)
        resultados = df_principal[mask]
        
        if not resultados.empty:
            idx = st.selectbox("Seleccione el registro:", resultados.index)
            cliente_sel = df_principal.loc[idx]
            
            # Extraer cédula de la base principal
            cedula_id = cliente_sel.get('No cedula', cliente_sel.get('CEDULA', cliente_sel[0]))
            
            col_info, col_form = st.columns([1, 1])
            
            with col_info:
                st.subheader("📋 Datos del Cliente")
                st.write(cliente_sel)
            
            with col_form:
                st.subheader("✍️ Nueva Gestión")
                # Formulario simplificado para probar
                obs = st.text_area("OBSERVACION")
                if st.button("💾 Guardar en Historial"):
                    st.success("Gestión registrada")
            
            # MOSTRAR EL HISTORIAL AL FINAL
            mostrar_historial_bloque(cedula_id)
        else:
            st.error("No se encontraron coincidencias.")
else:
    st.error("Archivo Excel no encontrado en el repositorio.")
