import streamlit as st
import pandas as pd
import os
from fpdf import FPDF # Librería para crear PDFs
from datetime import datetime

# --- CONFIGURACIÓN ---
ARCHIVO_EXCEL = 'BASE CONSOLIDADA BBVA.xlsx'

def generar_pdf(datos_cliente, gestion, tipificacion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Reporte de Gestión de Cobranza", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, txt=f"Cliente: {datos_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Resultado: {tipificacion}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Notas: {gestion}")
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ ---
st.set_page_config(page_title="Gestión BBVA Pro", layout="wide")

if os.path.exists(ARCHIVO_EXCEL):
    df = pd.read_excel(ARCHIVO_EXCEL)
    
    st.title("📊 Gestión y Seguimiento de Cartera")
    
    busqueda = st.text_input("🔍 Buscar cliente:")
    if busqueda:
        df_filtrado = df[df.astype(str).apply(lambda x: busqueda.lower() in x.str.lower().values, axis=1)]
        
        if not df_filtrado.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Datos del Deudor")
                idx = st.selectbox("Seleccionar:", df_filtrado.index)
                cliente = df.iloc[idx]
                st.write(cliente)
            
            with col2:
                st.subheader("📅 Agendar y Gestionar")
                # 1. Calendario de seguimiento
                fecha_seguimiento = st.date_input("Próximo contacto:", datetime.now())
                
                # 2. Tipificación
                tipo = st.selectbox("Estado:", ["Compromiso de Pago", "Ilocalizable", "Cita Programada"])
                notas = st.text_area("Comentarios de la gestión")
                
                if st.button("💾 Guardar y Generar Ficha"):
                    # Generar el PDF en memoria
                    pdf_bytes = generar_pdf(str(cliente[0]), notas, tipo)
                    
                    st.download_button(
                        label="📥 Descargar PDF de Gestión",
                        data=pdf_bytes,
                        file_name=f"Gestion_{cliente[0]}.pdf",
                        mime="application/pdf"
                    )
                    st.success(f"Gestión agendada para el {fecha_seguimiento}")
