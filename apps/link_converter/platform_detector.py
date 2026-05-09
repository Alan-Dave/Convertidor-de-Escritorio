"""
Módulo para detectar la plataforma de una URL y devolver info del ícono.
"""

import re

# Mapeo: (regex_pattern, nombre_plataforma, nombre_icono, solo_audio)
PLATFORM_MAP = [
    (r"(youtube\.com|youtu\.be)", "YouTube", "youtube.png", False),
    (r"tiktok\.com", "TikTok", "tiktok.png", False),
    (r"instagram\.com", "Instagram", "instagram.png", False),
    (r"(twitter\.com|x\.com)", "X / Twitter", "x.png", False),
    (r"(facebook\.com|fb\.com|fb\.watch)", "Facebook", "facebook.png", False),
    (r"twitch\.tv", "Twitch", "twitch.webp", False),
    (r"soundcloud\.com", "SoundCloud", "soundcloud.png", True),
    (r"vimeo\.com", "Vimeo", "vimeo.png", False)
]


def detect_platform(url: str) -> tuple:
    """
    Detecta la plataforma desde una URL.
    
    Returns:
        tuple: (nombre_plataforma, nombre_icono, solo_audio)
               nombre_icono puede ser None si no se reconoce la plataforma.
    """
    url = url.strip().lower()
    for pattern, name, icon, audio_only in PLATFORM_MAP:
        if re.search(pattern, url):
            return (name, icon, audio_only)
    return ("URL detectada", None, False)


def is_audio_only(url: str) -> bool:
    """Retorna True si la plataforma sólo soporta audio (ej: SoundCloud)."""
    _, _, audio_only = detect_platform(url)
    return audio_only
