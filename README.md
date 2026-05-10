# 🎛️ Media Hub — v1.4

Aplicación de escritorio modular hecha en Python (PyQt6) que agrupa múltiples herramientas de conversión y edición impulsadas por Inteligencia Artificial y utilidades multimedia avanzadas. Diseñada para ser **rápida, privada** (todo el procesamiento es local) y **libre de anuncios**.

---

## ✨ Novedades en v1.4

- 🌙 **Modo Oscuro Global** — Toggle en el Hub principal que aplica el tema a todas las micro-apps en tiempo real.
- ✂️ **Cortador de Audio Avanzado** — Editor multipista en tiempo real con previsualización dinámica de fades y saltos.
- 🖼️ **Descarga de imágenes** en el Link Converter — soporte para descargar imágenes directas y desde plataformas compatibles.
- 🔍 **Detección inteligente de contenido** — El Link Converter identifica automáticamente si un enlace apunta a video, audio o imagen, y bloquea las opciones incompatibles.

---

## 🚀 Herramientas Incluidas

### 1. 🎞️ Multimedia Converter
Conversión profesional de archivos multimedia en modo individual o por lotes.

| Módulo | Formatos soportados |
|---|---|
| **Audio** | `mp3`, `wav`, `flac`, `ogg`, `m4a` |
| **Video** | `mp4`, `mkv`, `avi`, `mov`, `webm` + extracción a `mp3` |
| **Imágenes** | `jpg`, `png`, `webp`, `gif`, `bmp`, `tiff` y más |
| **Reescalador** | Redimensión por píxeles o porcentaje, con opción de mantener relación de aspecto |

---

### 2. 🔗 Link Converter (Downloader Inteligente)
Descarga contenido multimedia desde redes sociales y URLs directas.

- **Plataformas soportadas:** YouTube, TikTok, Instagram, X (Twitter), Facebook, Twitch, Vimeo, SoundCloud y cientos más vía `yt-dlp`.
- **Detección automática de tipo de contenido:** Al pegar un enlace, el sistema identifica si es video, audio o imagen y activa solo las opciones compatibles.
  - URL de YouTube → habilita **Video** y **Audio** (deshabilita imagen)
  - URL de SoundCloud → habilita solo **Audio**
  - URL directa a `.jpg/.png/...` → habilita solo **Imagen**
  - Instagram / X → permite los tres tipos
- **Formatos de descarga:**
  - Video: `mp4`, `mkv`, `webm`, `avi`
  - Audio: `mp3`, `m4a`, `flac`, `ogg`, `wav`
  - Imagen: `jpg`, `png`, `webp`, `gif`, `bmp`
- **Selección de calidad de video:** Mejor disponible, 1080p, 720p, 480p, 360p.
- Motor basado en `yt-dlp` para video/audio y descarga directa `urllib` para imágenes.

---

### 3. 📄 Document Converter
- **Word → PDF:** Conversión con alta fidelidad usando Microsoft Word (requiere Word instalado).
- **PDF → Word:** Extrae y convierte contenido PDF a documentos editables `.docx`.
- **Procesamiento por lotes:** Convierte múltiples archivos de una vez.

---

### 4. 🤖 Background Eraser (IA)
- Eliminación de fondos impulsada por Inteligencia Artificial (`rembg` + `u2net`).
- Procesa sujetos y objetos complejos con un solo clic.
- Salida en `.png` con canal alfa (transparencia total).

---

### 5. ✨ Quality Enhancer — Real-ESRGAN (IA)
- **Súper Resolución 4x:** Amplía imágenes sin perder nitidez.
- **Restauración:** Elimina ruido y artefactos de compresión (ideal para fotos antiguas).
- Motor **Real-ESRGAN** para resultados de grado profesional.

---

### 6. ✂️ Advanced Audio Cut
- **Edición Profesional:** Corta o recorta archivos de audio visualizando su espectro (Waveform) interactivo.
- **Reproductor Integrado:** Previsualiza el resultado en tiempo real (con búsqueda via arrastre o clic derecho) sin necesidad de renderizar previamente.
- **Efectos Dinámicos:** Aplica *Fade In* y *Fade Out* (hasta 10s) con previsualización de volumen en vivo.
- **Modos de Corte:** Mantén la selección (Trim) o elimina el centro (Cut), escuchando los saltos en vivo.

---

## 🛠️ Requisitos del Sistema

| Requisito | Detalle |
|---|---|
| **Python** | 3.11 o superior |
| **FFmpeg** | Esencial para conversión de audio y video |
| **Microsoft Word** | Solo para conversión Word → PDF (opcional) |
| **Conexión a Internet** | Para el Link Converter y la descarga de modelos de IA (primera vez) |
| **Sistema Operativo** | Windows 10/11 (probado); compatible con Linux/macOS con ajustes menores |

---

## 📦 Instalación

### 1. Clonar el repositorio
```powershell
git clone https://github.com/Alan-Dave/MediaHub_Converter.git
cd MediaHub_Converter
```

### 2. Crear y activar entorno virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 4. Instalar FFmpeg (Windows — recomendado)
```powershell
winget install "FFmpeg (Essentials Build)"
```
> Alternativamente, descarga el ejecutable desde [ffmpeg.org](https://ffmpeg.org/download.html) y agrégalo al `PATH`.

---

## 🎮 Ejecución

```powershell
python main.py
```

---

## 💡 Notas Adicionales

- **Modelos de IA:** La primera vez que abras el *Quality Enhancer* o el *Background Eraser*, el sistema descargará automáticamente los modelos de IA (~180 MB). Este proceso ocurre una sola vez.
- **Modo Oscuro:** El estado del tema se mantiene durante la sesión. Se puede añadir persistencia entre reinicios en una futura versión.
- **Privacidad:** Todo el procesamiento de archivos (conversión, IA, reescalado) ocurre de forma completamente local. Tus archivos nunca suben a ningún servidor.
- **FFmpeg:** Si el sistema no reconoce FFmpeg, puedes configurar la ruta manualmente en las variables de entorno del sistema o definir la variable `FFMPEG_PATH`. El botón "Configurar FFmpeg" en los convertidores de audio y video explica los pasos.
- **Link Converter + Imágenes:** La descarga de imágenes funciona directamente solo con URLs que apunten a un archivo de imagen (`.jpg`, `.png`, etc.). Para imágenes embebidas en publicaciones de redes sociales, el resultado puede variar.
