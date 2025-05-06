import streamlit as st
import pandas as pd
import os
from datetime import datetime
import shutil
import subprocess
import unicodedata

# Configurar diseño general
st.set_page_config(page_title="Monitoreo Emocional Recover", page_icon="🎧", layout="wide")

# Mostrar logo
st.image("assets/logo.png", width=250)

st.title("🎧 Plataforma de Monitoreo Emocional - Recover")
st.markdown("Analiza llamadas automáticamente y detecta emociones y riesgos potenciales.")

# Función para limpiar nombres de archivo
def limpiar_nombre(nombre):
    nombre = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("utf-8")
    nombre = nombre.replace(" ", "_").replace(",", "").lower()
    return nombre

# Sección 1 - Carga de audios
st.header("🔽 1. Cargar grabaciones")
uploaded_files = st.file_uploader(
    "Sube tus audios .mp3 o .wav aquí:",
    accept_multiple_files=True,
    type=["mp3", "wav"]
)

if uploaded_files:
    if not os.path.exists("data"):
        os.makedirs("data")
    guardados = 0
    for file in uploaded_files:
        nombre_limpio = limpiar_nombre(file.name)
        if not nombre_limpio.endswith((".mp3", ".wav")):
            st.warning(f"❌ El archivo '{file.name}' tiene una extensión no válida.")
            continue
        with open(os.path.join("data", nombre_limpio), "wb") as f:
            f.write(file.getbuffer())
            guardados += 1
    st.success(f"✅ Se cargaron {guardados} archivo(s) correctamente.")

# Sección 2 - Análisis automático
st.header("⚙️ 2. Ejecutar análisis automático")
if st.button("🚀 Iniciar análisis de audios"):
    with st.spinner("Procesando llamadas... esto puede tardar unos minutos..."):
        resultado = subprocess.run(["venv\\Scripts\\python.exe", "analizar_lote.py"], capture_output=True, text=True)
        if resultado.returncode == 0:
            st.success("✅ Análisis finalizado correctamente.")
        else:
            st.error("❌ Ocurrió un error durante el análisis.")
            st.text(resultado.stderr)

# Sección 3 - Visualización del reporte
st.header("📊 3. Ver reporte de resultados")

csv_path = "data/resultados.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)

    # Filtros
    st.subheader("📂 Filtros")
    emocion_sel = st.multiselect("Filtrar por emoción", options=df["emocion"].unique(), default=df["emocion"].unique())
    riesgo_sel = st.selectbox("¿Filtrar por riesgo?", ["Todos", "Sí", "No"])

    df_filtrado = df[df["emocion"].isin(emocion_sel)]
    if riesgo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["riesgo"] == riesgo_sel]

    st.write(f"🎯 Mostrando {len(df_filtrado)} llamadas analizadas")

    # Vista general
    st.subheader("📄 Resumen de análisis")
    resumen = df_filtrado[["fecha", "archivo", "emocion", "polaridad", "riesgo"]].copy()
    resumen["polaridad"] = resumen["polaridad"].round(2)
    st.dataframe(resumen, use_container_width=True)

    # Detalle individual
    st.subheader("🔍 Detalle de llamadas")
    for _, fila in df_filtrado.iterrows():
        with st.expander(f"{fila['fecha']} - {fila['archivo']} ({fila['emocion']} | Riesgo: {fila['riesgo']})"):
            st.markdown(f"**Polaridad:** `{fila['polaridad']}`")
            st.markdown("**Transcripción completa:**")
            st.write(fila["transcripcion"])
            ruta_audio = os.path.join("data", fila["archivo"])
            if os.path.exists(ruta_audio):
                st.audio(ruta_audio)

    # Estadísticas gráficas
    st.subheader("📈 Distribución de emociones")
    st.bar_chart(df_filtrado["emocion"].value_counts())

    st.subheader("🚨 Llamadas con riesgo")
    st.bar_chart(df_filtrado["riesgo"].value_counts())

    # Botón para descargar CSV
    st.download_button("⬇️ Descargar resultados CSV", data=df.to_csv(index=False), file_name="resultados.csv", mime="text/csv")

    # Opción para limpiar resultados
    if st.button("🧹 Reiniciar y limpiar reporte"):
        os.remove(csv_path)
        st.warning("📁 Archivo resultados.csv eliminado. Reinicia el análisis para empezar desde cero.")

else:
    st.info("🔎 No hay resultados aún. Sube audios y ejecuta el análisis.")
