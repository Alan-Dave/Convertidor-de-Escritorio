#-----------------------------------------------
# Convertidor de Imagenes
#-----------------------------------------------

from PIL import Image, ImageFile
import os
import shutil

# Pillow sometimes fails on truncated images; enable loading anyway
ImageFile.LOAD_TRUNCATED_IMAGES = True


def _prepare_dest(ruta_destino: str) -> str:
    """Asegura que la carpeta de destino exista dentro del repositorio.

    - Si `ruta_destino` es relativa, se interpreta respecto a la raíz del repo.
    - Crea el directorio padre si no existe.
    - Devuelve la ruta absoluta final a usar para guardar.
    """
    if ruta_destino is None:
        raise ValueError("ruta_destino no puede ser None")

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    if not os.path.isabs(ruta_destino):
        ruta_abs = os.path.join(repo_root, ruta_destino)
    else:
        ruta_abs = ruta_destino

    parent = os.path.dirname(ruta_abs)
    if parent == '':
        parent = os.path.join(repo_root, 'destino')
        ruta_abs = os.path.join(parent, os.path.basename(ruta_abs))

    os.makedirs(parent, exist_ok=True)
    return ruta_abs


def _find_ffmpeg() -> str | None:
    """Intentar localizar el ejecutable ffmpeg."""
    env_path = os.environ.get('FFMPEG_PATH')
    if env_path:
        env_path = os.path.abspath(env_path)
        if os.path.isfile(env_path):
            return env_path
        if os.path.isdir(env_path):
            for candidate in ('ffmpeg.exe', 'ffmpeg'):
                maybe = os.path.join(env_path, candidate)
                if os.path.isfile(maybe):
                    return maybe

    for name in ('ffmpeg', 'ffmpeg.exe'):
        p = shutil.which(name)
        if p:
            return p

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    candidates = [
        os.path.join(repo_root, 'ffmpeg', 'ffmpeg'),
        os.path.join(repo_root, 'ffmpeg', 'ffmpeg.exe'),
        os.path.join(repo_root, 'ffmpeg', 'bin', 'ffmpeg'),
        os.path.join(repo_root, 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(repo_root, 'bin', 'ffmpeg'),
        os.path.join(repo_root, 'bin', 'ffmpeg.exe'),
        os.path.join(repo_root, 'ffmpeg.exe'),
        os.path.join(repo_root, 'ffmpeg'),
    ]

    user_profile = os.environ.get('USERPROFILE', '')
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    program_files = os.environ.get('ProgramFiles', r'C:\Program Files')
    program_files_x86 = os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)')
    windows_candidates = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\ffmpeg\ffmpeg.exe',
        os.path.join(program_files, 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(program_files_x86, 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(program_files, 'ImageMagick-7.1.1-Q16-HDRI', 'ffmpeg.exe'),
        os.path.join(local_app_data, 'Microsoft', 'WinGet', 'Links', 'ffmpeg.exe'),
        os.path.join(user_profile, 'scoop', 'shims', 'ffmpeg.exe'),
        os.path.join(user_profile, 'scoop', 'apps', 'ffmpeg', 'current', 'bin', 'ffmpeg.exe'),
        os.path.join(os.environ.get('ProgramData', r'C:\ProgramData'), 'chocolatey', 'bin', 'ffmpeg.exe'),
    ]
    candidates.extend(windows_candidates)

    for c in candidates:
        if os.path.isfile(c):
            return c

    try:
        import imageio_ffmpeg
        p = imageio_ffmpeg.get_ffmpeg_exe()
        if p and os.path.isfile(p):
            return p
    except Exception:
        pass

    return None


class ImageFormats:
    formatos_imagen = ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'gif', 'ico']

    @staticmethod
    def _open_image(ruta_origen):
        return Image.open(ruta_origen)

    @staticmethod
    def _save_image(img: Image.Image, ruta_destino: str, formato: str, quality: int = 85):
        ruta_destino = _prepare_dest(ruta_destino)
        formato_lower = formato.lower()

        if formato_lower in ('jpg', 'jpeg'):
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                fondo = Image.new('RGB', img.size, (255, 255, 255))
                fondo.paste(img.convert('RGBA'), mask=img.convert('RGBA').split()[-1])
                fondo.save(ruta_destino, 'JPEG', quality=quality)
            else:
                img.convert('RGB').save(ruta_destino, 'JPEG', quality=quality)
        elif formato_lower == 'png':
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img.save(ruta_destino, 'PNG', optimize=True)
            else:
                img.convert('RGB').save(ruta_destino, 'PNG', optimize=True)
        elif formato_lower == 'webp':
            img.save(ruta_destino, 'WEBP', quality=quality, method=6)
        else:
            try:
                img.save(ruta_destino, formato.upper())
            except Exception:
                img.save(ruta_destino)

        return f"✅ Convertido: {os.path.basename(ruta_destino)}"

    @staticmethod
    def convertir_jpg_a_png(ruta_origen, ruta_destino):
        try:
            img = ImageFormats._open_image(ruta_origen)
            return ImageFormats._save_image(img, ruta_destino, 'png')
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"

    @staticmethod
    def convertir_jpg_a_webp(ruta_origen, ruta_destino):
        try:
            img = ImageFormats._open_image(ruta_origen)
            return ImageFormats._save_image(img, ruta_destino, 'webp')
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"

    @staticmethod
    def convertir_png_a_jpg(ruta_origen, ruta_destino):
        try:
            img = ImageFormats._open_image(ruta_origen)
            return ImageFormats._save_image(img, ruta_destino, 'jpg')
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"

    @staticmethod
    def convertir_png_a_webp(ruta_origen, ruta_destino):
        try:
            img = ImageFormats._open_image(ruta_origen)
            return ImageFormats._save_image(img, ruta_destino, 'webp')
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"

    @staticmethod
    def convertir_webp_a_jpg(ruta_origen, ruta_destino):
        try:
            img = ImageFormats._open_image(ruta_origen)
            return ImageFormats._save_image(img, ruta_destino, 'jpg')
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"

    @staticmethod
    def convertir_webp_a_png(ruta_origen, ruta_destino):
        try:
            img = ImageFormats._open_image(ruta_origen)
            return ImageFormats._save_image(img, ruta_destino, 'png')
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"


class AudioFormats:
    formatos_audio = ['mp3', 'wav', 'flac', 'ogg', 'm4a', 'mpeg', 'aac', 'wma', 'alac', 'aiff']

    @staticmethod
    def _run_ffmpeg(ruta_origen, ruta_destino, extra_args=None):
        import subprocess
        if extra_args is None:
            extra_args = []
        ruta_destino = _prepare_dest(ruta_destino)
        ffmpeg_path = _find_ffmpeg()
        if not ffmpeg_path:
            return False, '❌ ffmpeg no está disponible. Añádelo a PATH o define la variable de entorno FFMPEG_PATH apuntando al ejecutable.'
        cmd = [ffmpeg_path, '-y', '-i', ruta_origen] + extra_args + [ruta_destino]
        try:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, cwd=repo_root)
            return True, f"✅ Convertido: {os.path.basename(ruta_origen)} -> {os.path.basename(ruta_destino)}"
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode(errors='replace') if isinstance(e.stderr, (bytes, bytearray)) else str(e.stderr)
            return False, f"⚠️ Error en ffmpeg: {stderr}"

    @staticmethod
    def _default_audio_args(formato_destino: str):
        fmt = (formato_destino or '').lower()
        if fmt == 'mp3':
            return ['-vn', '-c:a', 'libmp3lame', '-b:a', '192k']
        if fmt == 'wav':
            return ['-vn', '-c:a', 'pcm_s16le', '-ar', '44100', '-ac', '2']
        if fmt == 'flac':
            return ['-vn', '-c:a', 'flac']
        if fmt == 'ogg':
            return ['-vn', '-c:a', 'libvorbis', '-q:a', '5']
        if fmt in ('m4a', 'aac'):
            return ['-vn', '-c:a', 'aac', '-b:a', '192k']
        return ['-vn', '-c:a', 'aac', '-b:a', '192k']

    @staticmethod
    def convertir(ruta_origen, ruta_destino, formato_destino=None):
        try:
            if formato_destino is None:
                formato_destino = os.path.splitext(ruta_destino)[1].lstrip('.').lower()
            extra_args = AudioFormats._default_audio_args(formato_destino)
            ok, msg = AudioFormats._run_ffmpeg(ruta_origen, ruta_destino, extra_args=extra_args)
            return msg
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"


class VideoFormats:
    formatos_video = ['mp4', 'mkv', 'avi', 'mov', 'webm', 'flv', 'wmv', 'm4v', '3gp', 'mpeg']

    @staticmethod
    def _run_ffmpeg(ruta_origen, ruta_destino, extra_args=None):
        import subprocess
        if extra_args is None:
            extra_args = []
        ruta_destino = _prepare_dest(ruta_destino)
        ffmpeg_path = _find_ffmpeg()
        if not ffmpeg_path:
            return False, '❌ ffmpeg no está disponible. Añádelo a PATH o define la variable de entorno FFMPEG_PATH apuntando al ejecutable.'
        cmd = [ffmpeg_path, '-y', '-i', ruta_origen] + extra_args + [ruta_destino]
        try:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, cwd=repo_root)
            return True, f"✅ Convertido: {os.path.basename(ruta_origen)} -> {os.path.basename(ruta_destino)}"
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode(errors='replace') if isinstance(e.stderr, (bytes, bytearray)) else str(e.stderr)
            return False, f"⚠️ Error en ffmpeg: {stderr}"

    @staticmethod
    def _default_video_args(formato_destino: str):
        fmt = (formato_destino or '').lower()
        if fmt in ('mp4', 'mov', 'm4v'):
            return ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart']
        if fmt == 'mkv':
            return ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k']
        if fmt == 'webm':
            return ['-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '32', '-c:a', 'libopus', '-b:a', '128k']
        if fmt == 'avi':
            return ['-c:v', 'mpeg4', '-q:v', '5', '-c:a', 'libmp3lame', '-b:a', '192k']
        if fmt == 'wmv':
            return ['-c:v', 'wmv2', '-c:a', 'wmav2']
        if fmt == 'flv':
            return ['-c:v', 'flv', '-c:a', 'libmp3lame', '-b:a', '128k']
        if fmt == '3gp':
            return ['-c:v', 'h263', '-c:a', 'aac', '-b:a', '96k']
        return ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k']

    @staticmethod
    def convertir(ruta_origen, ruta_destino, formato_destino=None):
        try:
            if formato_destino is None:
                formato_destino = os.path.splitext(ruta_destino)[1].lstrip('.').lower()
            extra_args = VideoFormats._default_video_args(formato_destino)
            ok, msg = VideoFormats._run_ffmpeg(ruta_origen, ruta_destino, extra_args=extra_args)
            return msg
        except Exception as e:
            return f"⚠️ Error con {os.path.basename(ruta_origen)}: {e}"
