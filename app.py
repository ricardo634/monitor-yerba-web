import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monitor Yerba Mate", layout="wide")

# Título de la Web
st.title("🌿 Monitor Satelital - Cooperativa Liebig")

def cargar_datos():
    # Usamos tu llave
    JSON_FILE = 'tu-credencial.json' 
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(JSON_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    
    # Abrimos tu Excel
    sheet = client.open("yerbatero").sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # Renombramos columnas para el gráfico
    # Asumimos el orden: Fecha, Coop, Lote, NDVI, Estado...
    df.columns = ['fecha', 'coop', 'lote', 'ndvi', 'estado', 'detalle']
    # Convertimos NDVI a número (por si tiene comas)
    df['ndvi'] = df['ndvi'].astype(str).str.replace(',', '.').astype(float)
    return df

try:
    df = cargar_datos()
    
    # Buscador lateral
    lote_sel = st.sidebar.selectbox("Seleccione el Lote:", df['lote'].unique())
    
    # Filtramos datos del lote elegido
    datos_lote = df[df['lote'] == lote_sel]
    ultimo = datos_lote.iloc[-1]
    
    # Mostrar métricas principales
    col1, col2 = st.columns(2)
    col1.metric("Salud Actual (NDVI)", ultimo['ndvi'])
    col2.info(f"📅 Última actualización: {ultimo['fecha']}")
    
    st.subheader(f"📊 Histórico de Vigor - {lote_sel}")
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(datos_lote['fecha'], datos_lote['ndvi'], marker='o', color='green', linewidth=2)
    ax.set_ylabel("Valor NDVI")
    plt.xticks(rotation=45)
    st.pyplot(fig)

except Exception as e:
    st.error(f"Esperando datos del sistema... ({e})")
