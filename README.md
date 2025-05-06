
# 🎧 Sistema de Monitoreo Emocional para Call Center - Recover

Este proyecto implementa una plataforma de inteligencia artificial para analizar automáticamente llamadas telefónicas, transcribirlas y detectar emociones, posibles riesgos o conflictos. Está diseñado como parte de un caso práctico de titulación para la Maestría en Inteligencia Artificial Aplicada.

---

## 🚀 ¿Qué hace esta plataforma?

- Transcribe llamadas de audio (MP3 o WAV) usando Whisper
- Analiza la carga emocional (positiva, negativa, neutra)
- Detecta palabras clave asociadas a riesgo o conflicto
- Genera reportes y dashboards interactivos con Streamlit
- Permite escuchar los audios y revisar cada transcripción

---

## 📁 Estructura del Proyecto

```
recover-nlp-monitoring/
│
├── app.py                   # Interfaz gráfica en Streamlit
├── analizar_lote.py         # Lógica de transcripción y análisis por lote
├── requirements.txt         # Dependencias del entorno
│
├── data/                    # Audios y resultados exportados
│   ├── audio1.mp3
│   ├── resultados.csv
│
├── assets/
│   └── logo.png             # Logo institucional
│
├── venv/                    # Entorno virtual Python (no subir a GitHub)
```

---

## 🧪 Requisitos

- Python 3.10 o 3.11
- ffmpeg instalado (y en PATH)
- Internet para descargar el modelo Whisper

---

## ⚙️ Instalación

```bash
# Clona el repositorio
git clone https://github.com/tuusuario/recover-nlp-monitoring.git
cd recover-nlp-monitoring

# Crea entorno virtual
python -m venv venv
venv\Scripts\activate   # En Windows

# Instala dependencias
pip install -r requirements.txt
```

---

## 🖥️ Ejecución

```bash
# Ejecuta la app
streamlit run app.py
```

Esto abrirá la plataforma web en tu navegador para subir audios y generar reportes.

---

## 🧹 Limpieza

Si deseas reiniciar desde cero y eliminar los resultados:

- Usa el botón **🧹 Reiniciar y limpiar reporte** en la app
- O borra manualmente el archivo: `data/resultados.csv`

---

## 👨‍💻 Autor

Carlos Padilla  
Recover - Ecuador  
Maestría en Inteligencia Artificial Aplicada  

---

## 📜 Licencia

Este proyecto es de uso académico y corporativo privado. No redistribuir sin autorización del autor.



---

## 📥 Clonar este repositorio

Puedes clonar este proyecto y ejecutarlo localmente así:

```bash
git clone https://github.com/cpadilla83/recover-nlp-monitoring.git
cd recover-nlp-monitoring
```

> Reemplaza `tu-usuario` por tu nombre de usuario real en GitHub.

---

## 🧪 Configuración rápida del entorno

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación web
streamlit run app.py
```

---

## 🗂️ Estructura importante

- `data/`: audios y resultados (se genera automáticamente)
- `assets/logo.png`: imagen del logo de Recover
- `app.py`: interfaz gráfica
- `analizar_lote.py`: script de análisis por lote

