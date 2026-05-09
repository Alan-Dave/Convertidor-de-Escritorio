# Media Hub (Versión 1.2)

Aplicación de escritorio modular hecha en Python (PyQt6) que agrupa múltiples herramientas de conversión y edición impulsadas por Inteligencia Artificial y utilidades multimedia avanzadas. Diseñada para ser rápida, privada (todo el procesamiento es local) y libre de anuncios.

## 🚀 Herramientas Incluidas

### 1. Multimedia Converter
- **Audio:** Conversión profesional entre formatos `mp3`, `wav`, `flac`, `ogg`, `m4a`.
- **Video:** Conversión de video de alta calidad (`mp4`, `mkv`, `avi`, `mov`, `webm`). 
- **Extracción de Audio:** Permite convertir videos directamente a **MP3**.
- **Imágenes:** Conversión masiva de formatos de imagen.
- **Reescalador:** Redimensiona imágenes por píxeles o porcentaje manteniendo la relación de aspecto y calidad.

### 2. Link Converter (Downloader Inteligente)
- **Multi-plataforma:** Descarga contenido de YouTube, TikTok, Instagram, Twitter (X), Facebook y cientos de sitios más.
- **Detección Automática:** El sistema identifica la plataforma al pegar el enlace.
- **Opciones de Descarga:** Elige entre descargar el video completo (MP4) o solo el audio (MP3).
- **Potencia:** Basado en `yt-dlp` para garantizar descargas rápidas y estables.

### 3. Document Converter
- **Office a PDF:** Convierte documentos de Word (`docx`) a PDF con alta fidelidad (requiere MS Word).
- **PDF a Word:** Convierte archivos PDF a documentos editables de Word (`docx`).
- **Procesamiento por Lotes:** Convierte múltiples documentos simultáneamente.

### 4. Background Eraser (IA)
- Eliminación de fondos impulsada por Inteligencia Artificial (`rembg`).
- Procesa sujetos y objetos complejos con un solo clic.
- Salida automática en `.png` con transparencia optimizada.

### 5. Quality Enhancer (IA - Real-ESRGAN)
- **Súper Resolución:** Aumenta el tamaño de tus imágenes x4 sin perder nitidez.
- **Restauración:** Elimina el ruido y los artefactos de compresión (ideal para fotos antiguas o de baja resolución).
- Utiliza el motor **Real-ESRGAN** para resultados de grado profesional.

## 🛠️ Requisitos Técnicos

- **Python 3.11+**
- **FFmpeg:** Esencial para todas las tareas de audio y video.
- **Microsoft Word:** Necesario para la conversión nativa de Word a PDF.
- **Conexión a Internet:** Solo necesaria la primera vez para descargar los modelos de IA y para el Link Converter.

## 📦 Instalación

1. **Clonar el repositorio:**
   ```powershell
   git clone https://github.com/tu-usuario/media-hub.git
   cd media-hub
   ```

2. **Crear y activar entorno virtual:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Instalar FFmpeg (Recomendado en Windows):**
   ```powershell
   winget install "FFmpeg (Essentials Build)"
   ```

## 🎮 Ejecución

Para iniciar el Hub principal:
```powershell
python main.py
```

## 💡 Notas Adicionales

- **Modelos de IA:** La primera vez que abras el *Quality Enhancer* o el *Background Eraser*, el sistema descargará automáticamente los modelos (aprox. 180MB). Esto ocurre solo una vez.
- **Privacidad:** Todo el procesamiento (excepto la descarga de links) se realiza de forma local en tu computadora. Tus archivos nunca suben a la nube.
- **FFmpeg:** Si el sistema no reconoce FFmpeg, puedes definir la ruta manualmente en las variables de entorno o crear una variable `FFMPEG_PATH`.
