import whisper
import ffmpeg
import os
import pandas as pd
from textblob import TextBlob
from datetime import datetime
import time

# Verificar y crear carpeta /data si no existe
carpeta = "data/"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)
    print("[INFO] Carpeta 'data/' creada automáticamente.")

# Función para mejorar audio
def mejorar_audio(path_original):
    path_temp = path_original.replace(".wav", "_tmp.wav").replace(".mp3", "_tmp.wav")
    ffmpeg.input(path_original).output(path_temp, ar=16000).run(overwrite_output=True)
    os.replace(path_temp, path_original)

# Función para eliminar texto repetido
def eliminar_repeticiones(texto):
    lineas = texto.split('.')
    texto_filtrado = []
    anteriores = set()
    for linea in lineas:
        frase = linea.strip()
        if frase and frase not in anteriores:
            texto_filtrado.append(frase)
            anteriores.add(frase)
    return '. '.join(texto_filtrado)

# Cargar modelo Whisper
print("[INFO] Cargando modelo 'tiny' de Whisper...")
model = whisper.load_model("tiny")

# Lista de palabras clave de riesgo
palabras_riesgo = [
    "demanda", "abogado", "denuncia", "fraude", "ilegal", "amenaza", "acoso", "hostigamiento",
    "superintendencia", "defensoría", "queja", "reclamo", "mala atención", "irrespetuoso", "estafa",
    "engaño", "falsedad", "mentira", "me colgaron", "no me ayudan", "buro", "demandar", "proceso legal",
    "denunciar", "maltrato", "mala gestión", "trato inadecuado", "trato grosero", "insistencia", 
    "violación de derechos", "no autorizo", "sin consentimiento", "violaron mis derechos", 
    "me ofendieron", "incómodo", "molesto", "desagradable", "intimidan", "presionan", "extorsión", 
    "retención", "trato inhumano", "no corresponde", "me están cobrando demás", 
    "no debo nada", "ya pagué", "me están acosando", "no llamen más", "abusivos", "acosadores"
]

# Archivos de audio en /data
archivos_audio = [f for f in os.listdir(carpeta) if f.endswith((".wav", ".mp3"))]

# Salida CSV
csv_path = os.path.join(carpeta, "resultados.csv")
resultados = []

print(f"[INFO] Se encontraron {len(archivos_audio)} archivos de audio para procesar.")

for nombre in archivos_audio:
    ruta = os.path.join(carpeta, nombre)
    print(f"\n[PROCESANDO] {nombre}")

    try:
        mejorar_audio(ruta)
        print("[OK] Audio mejorado a 16kHz.")

        inicio = time.time()
        result = model.transcribe(ruta, language="es", fp16=False)
        duracion = round(time.time() - inicio, 2)
        print(f"[OK] Transcripción completada en {duracion} segundos.")

        texto = eliminar_repeticiones(result["text"])
        blob = TextBlob(texto)
        polaridad = blob.sentiment.polarity

        if polaridad > 0.1:
            emocion = "POSITIVA"
        elif polaridad < -0.1:
            emocion = "NEGATIVA"
        else:
            emocion = "NEUTRA"

        riesgo = any(palabra in texto.lower() for palabra in palabras_riesgo) or polaridad < -0.3

        fila = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "archivo": nombre,
            "transcripcion": texto,
            "polaridad": round(polaridad, 3),
            "emocion": emocion,
            "riesgo": "Sí" if riesgo else "No"
        }

        resultados.append(fila)
        print("[OK] Análisis completado y registrado.")

    except Exception as e:
        print(f"[ERROR] No se pudo procesar {nombre}: {e}")

# Guardar CSV
df_nuevo = pd.DataFrame(resultados)
if os.path.exists(csv_path):
    df_nuevo.to_csv(csv_path, mode="a", header=False, index=False)
else:
    df_nuevo.to_csv(csv_path, index=False)

print(f"\n[FINALIZADO] Todos los resultados fueron guardados en {csv_path}")
