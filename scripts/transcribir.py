import whisper
import ffmpeg
import os
from textblob import TextBlob
import pandas as pd
from datetime import datetime

# Configuración
nombre_audio = "audio2.wav"
entrada = f"../data/{nombre_audio}"
temporal = f"../data/temp.wav"

# Paso 0: Mejorar calidad del audio WAV
print("🎧 Mejorando calidad de audio...")
ffmpeg.input(entrada).output(temporal, ar=16000).run(overwrite_output=True)
os.replace(temporal, entrada)
print("✅ Audio optimizado.")

# Paso 1: Cargar modelo Whisper (más rápido)
print("📦 Cargando modelo Whisper 'small'...")
model = whisper.load_model("small")

# Paso 2: Transcribir (forzando español y sin fp16 para CPU)
print("🔁 Transcribiendo...")
result = model.transcribe(entrada, language="es", fp16=False)

# Eliminar repeticiones simples
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

texto = eliminar_repeticiones(result["text"])

# Paso 3: Análisis de sentimiento
blob = TextBlob(texto)
polaridad = blob.sentiment.polarity

if polaridad > 0.1:
    emocion = "POSITIVA"
elif polaridad < -0.1:
    emocion = "NEGATIVA"
else:
    emocion = "NEUTRA"

# Paso 4: Detección de palabras de riesgo
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
riesgo = any(palabra in texto.lower() for palabra in palabras_riesgo) or polaridad < -0.3

# Paso 5: Mostrar resultados
print("\n🎧 Transcripción:")
print(texto)

print("\n🔍 Sentimiento:")
print(f"Polaridad: {polaridad}")
print(f"Emoción detectada: {emocion}")

print("\n🚨 Riesgo:")
print("⚠️ ALERTA DE RIESGO ⚠️" if riesgo else "✅ Sin riesgo detectado")

# Paso 6: Guardar en CSV
csv_path = "../data/resultados.csv"

nueva_fila = pd.DataFrame([{
    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "archivo": nombre_audio,
    "transcripcion": texto,
    "polaridad": round(polaridad, 3),
    "emocion": emocion,
    "riesgo": "Sí" if riesgo else "No"
}])

# Agregar sin sobrescribir si ya existe
if os.path.exists(csv_path):
    nueva_fila.to_csv(csv_path, mode="a", header=False, index=False)
else:
    nueva_fila.to_csv(csv_path, index=False)

print("\n📁 Resultados guardados en resultados.csv")
