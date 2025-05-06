import whisper
from textblob import TextBlob

# Paso 1: Cargar modelo Whisper
model = whisper.load_model("base")

# Paso 2: Ruta al audio
audio_path = "../data/audio1.mp3"  # Cambia el nombre si usas .mp3

# Paso 3: Transcribir
print("🔁 Transcribiendo...")
result = model.transcribe(audio_path)
texto = result["text"]

# Paso 4: Análisis emocional
blob = TextBlob(texto)
polaridad = blob.sentiment.polarity

# Clasificación simple
if polaridad > 0.1:
    emocion = "POSITIVA"
elif polaridad < -0.1:
    emocion = "NEGATIVA"
else:
    emocion = "NEUTRA"

# Paso 5: Mostrar resultados
print("\n🎧 Transcripción:")
print(texto)

print("\n🔍 Análisis de Sentimiento:")
print(f"Polaridad: {polaridad}")
print(f"Emoción detectada: {emocion}")
