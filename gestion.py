import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'
HOJA_HISTORIAL = 'Historico_Gestiones'

st.set_page_config(page_title="Gestión de Cartera Pro", layout="wide")

# --- FUNCIÓN PARA MOSTRAR HISTORIAL (COLUMNAS C A L) ---
def mostrar_historial_bloque(cedula_cliente):
    try:
        # Cargamos el historial
        df_hist = pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJA_HISTORIAL)
        
        # Limpieza estándar de la columna de búsqueda
        # Buscamos la columna 'CEDULA' (generalmente es la B, índice 1)
        # Forzamos a que todas las columnas sean comparables
        df_hist.columns = [str(c).strip().upper() for c in df_hist.columns]
        df_hist['CEDULA'] = df_hist['CEDULA'].astype(str)
        
        # Filtramos por el deudor actual
        pasado = df_hist[df_hist['CEDULA'] == str(cedula_cliente)]
        
        if not pasado.empty:
            st.divider()
            st.subheader("📜 Cronología de Gestiones Anteriores (Detalle Completo)")
            
            # SELECCIÓN POR POSICIÓN: Columna C (2) hasta la L (11)
            # El rango 2:12 en Python toma desde el índice 2 hasta el 11
            detalle = pasado.iloc[:, 2:12]
            
            # Mostramos el bloque con barra de desplazamiento si es necesario
            st.dataframe(detalle, use_container_width=True, hide_index=True)
        else:
            st.info("No se registran gestiones previas en el bloque C-L para este número de identificación.")
            
    except Exception as e:
        st.warning(f"Aviso: No se pudo cargar el bloque del historial. Verifique que la pestaña '{HOJA_HISTORIAL}' tenga datos.")

# --- INTERFAZ DE USUARIO ---
st.title("⚖️ Panel de Control Legal - BBVA")

if os.path.exists(ARCHIVO_EXCEL):
    df_principal = pd.read_excel(ARCHIVO_EXCEL)
    
    busqueda = st.text_input("🔍 Ingrese Cédula o Nombre del deudor:")
    
    if busqueda:
        # Filtro de búsqueda en la base principal
        mask = df_principal.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)
        resultados = df_principal[mask]
        
        if not resultados.empty:
            # Selector de registro
            idx = st.selectbox("Registros encontrados:", resultados.index)
            cliente_sel = df_principal.loc[idx]
            cedula_id = cliente_sel.get('CEDULA', cliente_sel[0])
            
            # Diseño en dos columnas para la gestión actual
            col_info, col_form = st.columns([1, 1])
            
            with col_info:
                st.info("📌 Datos del Perfil Seleccionado")
                st.write(cliente_sel)
            
            with col_form:
                st.success("✍️ Registro de Nueva Gestión")
                asesor = st.text_input("Asesor Responsable", value="Oficina Jurídica")
                obs_nueva = st.text_area("Observaciones de la llamada/trámite")
                f_seguimiento = st.date_input("Programar nuevo contacto")
                
                if st.button("💾 Finalizar y Guardar"):
                    st.toast("Gestión registrada localmente")
            
            # MOSTRAR EL BLOQUE C-L AL FINAL (ANCHO COMPLETO)
            mostrar_historial_bloque(cedula_id)
            
        else:
            st.error("No se encontró ningún deudor con esos datos.")
else:
    st.error(f"Error: El archivo '{ARCHIVO_EXCEL}' no se encuentra en el repositorio.")
