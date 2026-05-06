# Convertidor Multimedia (PyQt6)
<<<<<<< HEAD

Aplicación de escritorio hecha en Python para convertir **imágenes**, **audio** y **video** sin depender de páginas con anuncios.

Incluye interfaz gráfica con drag & drop, selección de archivo/carpeta, validación por tipo de archivo y barra de progreso durante la conversión.

## Características

- Conversión por módulos: `Imagen`, `Audio` y `Video`.
- Arrastrar y soltar con validación de formato por sección.
- Conversión individual y por carpeta (lotes).
- Indicador visual de progreso:
  - archivo único: progreso indeterminado (animación),
  - lote: progreso real por cantidad de archivos.
- Salida automática en carpeta `destino/`.
- Interfaz moderna en PyQt6.

## Formatos soportados

### Imágenes
- Entrada: `png`, `jpg`, `jpeg`, `bmp`, `webp`
- Salida: `png`, `jpg`, `webp`

### Audio
- Entrada: `mp3`, `wav`, `flac`, `ogg`, `m4a` (y `mpeg` en selección)
- Salida: `mp3`, `wav`, `flac`, `ogg`, `m4a`

### Video
- Entrada: `mp4`, `mkv`, `avi`, `mov`, `webm`
- Salida: `mp4`, `mkv`, `avi`, `mov`, `webm`

## Requisitos

- Python 3.11+ (recomendado)
- Dependencias de `requirements.txt`
- **FFmpeg** (obligatorio para audio/video)

## Instalación

1) Clona o descarga el proyecto.

2) Crea y activa entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3) Instala dependencias:

```powershell
pip install -r requirements.txt
```

4) Instala FFmpeg (Windows recomendado):

```powershell
winget install "FFmpeg (Essentials Build)"
```

Si no queda en `PATH`, define la variable:

```powershell
setx FFMPEG_PATH "C:\ruta\a\ffmpeg.exe"
```

## Ejecución

```powershell
python main.py
```

## Estructura del proyecto

```text
Convertidor/
├─ main.py
├─ requirements.txt
├─ src/
│  ├─ converters/
│  │  └─ conversion.py
│  └─ ui/
│     ├─ index.py
│     ├─ images_converter.py
│     ├─ audio_converter.py
│     ├─ video_converter.py
│     └─ ui_theme.py
├─ assets/
│  └─ icons/
└─ destino/              # se crea automáticamente al convertir
```

## Notas

- El módulo de imágenes usa `Pillow`.
- Los módulos de audio y video usan `ffmpeg`.
- Si arrastras un archivo de tipo incorrecto, la app muestra advertencia y lo rechaza.

## Troubleshooting rápido

- **“ffmpeg no está disponible”**  
  Instala FFmpeg o configura `FFMPEG_PATH`.

- **El archivo convertido no se reproduce**  
  Prueba con formatos estándar (`mp3`, `wav`, `mp4`) y vuelve a convertir desde el archivo original.
=======

Aplicación de escritorio hecha en Python para convertir **imágenes**, **audio** y **video** sin depender de páginas con anuncios.

Incluye interfaz gráfica con drag & drop, selección de archivo/carpeta, validación por tipo de archivo y barra de progreso durante la conversión.

## Características

- Conversión por módulos: `Imagen`, `Audio` y `Video`.
- Arrastrar y soltar con validación de formato por sección.
- Conversión individual y por carpeta (lotes).
- Indicador visual de progreso:
  - archivo único: progreso indeterminado (animación),
  - lote: progreso real por cantidad de archivos.
- Salida automática en carpeta `destino/`.
- Interfaz moderna en PyQt6.

## Formatos soportados

### Imágenes
- Entrada: `png`, `jpg`, `jpeg`, `bmp`, `webp`
- Salida: `png`, `jpg`, `webp`

### Audio
- Entrada: `mp3`, `wav`, `flac`, `ogg`, `m4a` (y `mpeg` en selección)
- Salida: `mp3`, `wav`, `flac`, `ogg`, `m4a`

### Video
- Entrada: `mp4`, `mkv`, `avi`, `mov`, `webm`
- Salida: `mp4`, `mkv`, `avi`, `mov`, `webm`

## Requisitos

- Python 3.11+ (recomendado)
- Dependencias de `requirements.txt`
- **FFmpeg** (obligatorio para audio/video)

## Instalación

1) Clona o descarga el proyecto.

2) Crea y activa entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3) Instala dependencias:

```powershell
pip install -r requirements.txt
```

4) Instala FFmpeg (Windows recomendado):

```powershell
winget install "FFmpeg (Essentials Build)"
```

Si no queda en `PATH`, define la variable:

```powershell
setx FFMPEG_PATH "C:\ruta\a\ffmpeg.exe"
```

## Ejecución

```powershell
python main.py
```

## Estructura del proyecto

```text
Convertidor/
├─ main.py
├─ requirements.txt
├─ src/
│  ├─ converters/
│  │  └─ conversion.py
│  └─ ui/
│     ├─ index.py
│     ├─ images_converter.py
│     ├─ audio_converter.py
│     ├─ video_converter.py
│     └─ ui_theme.py
├─ assets/
│  └─ icons/
└─ destino/              # se crea automáticamente al convertir
```

## Notas

- El módulo de imágenes usa `Pillow`.
- Los módulos de audio y video usan `ffmpeg`.
- Si arrastras un archivo de tipo incorrecto, la app muestra advertencia y lo rechaza.

## Troubleshooting rápido

- **“ffmpeg no está disponible”**  
  Instala FFmpeg o configura `FFMPEG_PATH`.

- **El archivo convertido no se reproduce**  
  Prueba con formatos estándar (`mp3`, `wav`, `mp4`) y vuelve a convertir desde el archivo original.

>>>>>>> b8c0e45fb896732b9024c04aa25da3e10473c5bd
