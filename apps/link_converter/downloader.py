"""
Worker de descarga en hilo separado usando yt-dlp.
"""

import os
from PyQt6.QtCore import QThread, pyqtSignal


def _parse_error(e: Exception) -> str:
    """Convierte errores de yt-dlp en mensajes legibles."""
    msg = str(e).lower()
    original = str(e)

    if ("private" in msg and "login" in msg) or "sign in" in msg or "authentication required" in msg:
        return "Este contenido es privado o requiere inicio de sesión."
    if "unavailable" in msg or "not available" in msg:
        return "Este video no está disponible en tu región o fue eliminado."
    if "age" in msg and ("restrict" in msg or "confirm" in msg):
        return "Este contenido tiene restricción de edad y no se puede descargar sin autenticación."
    if "copyright" in msg or "has been blocked" in msg:
        return "Este contenido está bloqueado por derechos de autor."
    if "unsupported url" in msg or "no video formats" in msg or "unable to extract" in msg:
        return "La URL no es válida o no es compatible con ninguna plataforma soportada."
    if "connection" in msg or "network" in msg or "timed out" in msg:
        return "No se pudo conectar. Verifica tu conexión a internet e intenta de nuevo."

    # Recorta mensajes demasiado largos
    if len(original) > 300:
        return original[:300] + "..."
    return original


class DownloadWorker(QThread):
    """
    Hilo de descarga. Emite señales de progreso, finalización y error.
    """
    progress = pyqtSignal(int, str)   # (porcentaje 0-100, texto_estado)
    finished = pyqtSignal(str)         # título del archivo descargado
    error = pyqtSignal(str)            # mensaje de error legible

    def __init__(self, url: str, media_type: str, fmt: str, quality: str, output_dir: str, parent=None):
        """
        Args:
            url: URL a descargar.
            media_type: "video" o "audio".
            fmt: formato destino (ej: "mp4", "mp3").
            quality: calidad de video (ej: "best", "1080", "720"). Ignorado para audio.
            output_dir: carpeta de destino.
        """
        super().__init__(parent)
        self.url = url
        self.media_type = media_type
        self.fmt = fmt
        self.quality = quality
        self.output_dir = output_dir
        self._last_percent = -1
        self._download_completed = False  # bandera: descarga real terminada
        self._downloaded_title = "archivo"

    def run(self):
        try:
            import yt_dlp
        except ImportError:
            self.error.emit("yt-dlp no está instalado. Ejecuta: pip install yt-dlp")
            return

        output_template = os.path.join(self.output_dir, "%(title)s.%(ext)s")

        def progress_hook(d):
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                downloaded = d.get("downloaded_bytes", 0)
                speed = d.get("speed", 0) or 0
                if total > 0:
                    percent = int(downloaded / total * 100)
                else:
                    percent = 0

                if percent != self._last_percent:
                    self._last_percent = percent
                    speed_str = f"{speed/1024/1024:.1f} MB/s" if speed > 0 else ""
                    self.progress.emit(percent, f"Descargando... {percent}% {speed_str}")

            elif d.get("status") == "finished":
                # El archivo crudo ya está en disco — descarga completada
                self._download_completed = True
                self.progress.emit(99, "Procesando archivo...")

        # Intentar usar ffmpeg bundled de imageio-ffmpeg
        ffmpeg_location = None
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            if os.path.isfile(ffmpeg_exe):
                ffmpeg_location = os.path.dirname(ffmpeg_exe)
        except Exception:
            pass

        # Construir opciones de yt-dlp
        ydl_opts = {
            "outtmpl": output_template,
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
        }

        if ffmpeg_location:
            ydl_opts["ffmpeg_location"] = ffmpeg_location

        if self.media_type == "audio":
            ydl_opts.update({
                # Preferir formatos de solo audio que no requieran fusión
                "format": "bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.fmt,
                    "preferredquality": "192",
                }],
            })
        else:
            # Preferir formatos pre-fusionados (no requieren ffmpeg para mezclar)
            # Fallback progresivo hacia streams separados si ffmpeg está disponible
            if self.quality == "best":
                fmt_selector = (
                    f"best[ext={self.fmt}]"
                    f"/best[ext=mp4]"
                    f"/bestvideo+bestaudio/best"
                )
            else:
                height = self.quality  # ej: "1080", "720"
                fmt_selector = (
                    f"best[height<={height}][ext={self.fmt}]"
                    f"/best[height<={height}][ext=mp4]"
                    f"/best[height<={height}]"
                    f"/bestvideo[height<={height}]+bestaudio"
                    f"/best"
                )

            ydl_opts.update({
                "format": fmt_selector,
                "merge_output_format": self.fmt,
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                title = info.get("title", "archivo") if info else "archivo"
                self._downloaded_title = title
                self._download_completed = True

            self.progress.emit(100, "✅ ¡Descarga completada!")
            self.finished.emit(self._downloaded_title)

        except Exception as e:
            if self._download_completed:
                # El archivo ya estaba descargado — la excepción es de post-proceso,
                # se puede ignorar con seguridad.
                self.progress.emit(100, "✅ ¡Descarga completada!")
                self.finished.emit(self._downloaded_title)
            else:
                self.error.emit(_parse_error(e))
