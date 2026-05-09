import os
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QProgressBar, QFileDialog,
    QMessageBox, QApplication, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

from apps.link_converter.platform_detector import detect_platform, is_audio_only
from apps.media_converter.ui.ui_theme import (
    APP_COLORS, BUTTON_STYLE, SOFT_BUTTON_STYLE,
    REMOVE_BUTTON_STYLE, CONVERT_BUTTON_STYLE,
    apply_window_theme, make_card_container,
)

# ──────────────────────────────────────────────
#  Estilos específicos del Link Converter
# ──────────────────────────────────────────────
URL_INPUT_STYLE = f"""
    QLineEdit {{
        background-color: #1e1e2a;
        color: #ffffff;
        border: 2px solid #3a3a52;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 11pt;
        font-family: 'Segoe UI', sans-serif;
    }}
    QLineEdit:focus {{
        border-color: #6c63ff;
    }}
    QLineEdit::placeholder {{
        color: #666;
    }}
"""

TYPE_BTN_ACTIVE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            from:#6c63ff, to:#a78bfa);
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 11pt;
        font-weight: bold;
        border: none;
    }
"""

TYPE_BTN_INACTIVE = f"""
    QPushButton {{
        background-color: #2b2b3b;
        color: {APP_COLORS['text_muted']};
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 11pt;
        border: 2px solid #3a3a52;
    }}
    QPushButton:hover {{
        background-color: #35354a;
        color: white;
    }}
"""

TYPE_BTN_DISABLED = f"""
    QPushButton {{
        background-color: #1e1e2a;
        color: #444;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 11pt;
        border: 2px solid #2a2a3a;
    }}
"""

COMBO_STYLE_LC = f"""
    QComboBox {{
        background-color: #1e1e2a;
        color: white;
        border: 2px solid #3a3a52;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 10pt;
        min-width: 120px;
    }}
    QComboBox:hover {{ border-color: #6c63ff; }}
    QComboBox::drop-down {{
        border: none;
        padding-right: 10px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #1e1e2a;
        color: white;
        selection-background-color: #6c63ff;
        border: 1px solid #3a3a52;
        border-radius: 6px;
    }}
"""

PROGRESS_STYLE = """
    QProgressBar {
        background-color: #1e1e2a;
        border: 2px solid #3a3a52;
        border-radius: 8px;
        height: 18px;
        text-align: center;
        color: white;
        font-size: 9pt;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            from:#6c63ff, to:#a78bfa);
        border-radius: 6px;
    }
"""

DOWNLOAD_BTN_ACTIVE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            from:#6c63ff, to:#a78bfa);
        color: white;
        border-radius: 10px;
        padding: 13px;
        font-size: 12pt;
        font-weight: bold;
        border: none;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            from:#7c73ff, to:#b79bff);
    }
    QPushButton:pressed {
        background: #5a52d5;
    }
"""

DOWNLOAD_BTN_DISABLED = """
    QPushButton {
        background-color: #1e1e2a;
        color: #444;
        border-radius: 10px;
        padding: 13px;
        font-size: 12pt;
        font-weight: bold;
        border: 2px solid #2a2a3a;
    }
"""


def get_icon_path(icon_file: str) -> str:
    base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base, "assets", "apps", "link_converter", icon_file)


class LinkConverterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Link Converter")
        self.setGeometry(120, 120, 520, 620)
        apply_window_theme(self)

        self._worker = None
        self._media_type = "video"  # "video" o "audio"
        self._current_platform = None
        self._audio_only = False

        self.init_ui()

    # ──────────────────────────────────────────
    #  UI
    # ──────────────────────────────────────────
    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(26, 24, 26, 24)
        card, layout = make_card_container()

        # ── Barra superior ──
        top = QHBoxLayout()
        back_btn = QPushButton("← Volver")
        back_btn.setFixedWidth(90)
        back_btn.clicked.connect(self.go_back)
        back_btn.setStyleSheet(SOFT_BUTTON_STYLE)
        top.addWidget(back_btn)
        top.addStretch()
        layout.addLayout(top)

        # ── Título ──
        title = QLabel("Link Converter")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {APP_COLORS['text_main']}; font-size: 16pt; font-weight: 700;")
        layout.addWidget(title)

        subtitle = QLabel("Descarga video o audio desde redes sociales")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {APP_COLORS['text_muted']}; font-size: 9pt;")
        layout.addWidget(subtitle)

        # ── Logo de plataforma ──
        self.platform_logo = QLabel()
        self.platform_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.platform_logo.setFixedHeight(90)
        self._clear_logo()
        layout.addWidget(self.platform_logo)

        self.platform_name_label = QLabel("")
        self.platform_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.platform_name_label.setStyleSheet(f"color: {APP_COLORS['text_muted']}; font-size: 9pt;")
        layout.addWidget(self.platform_name_label)

        # ── Campo URL ──
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Pega aquí el enlace (YouTube, TikTok, Instagram...)")
        self.url_input.setStyleSheet(URL_INPUT_STYLE)
        self.url_input.textChanged.connect(self._on_url_changed)
        layout.addWidget(self.url_input)

        # ── Separador ──
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #3a3a52;")
        layout.addWidget(sep)

        # ── Tipo: Video / Audio ──
        type_label = QLabel("Tipo de descarga:")
        type_label.setStyleSheet(f"color: {APP_COLORS['text_muted']}; font-size: 9pt;")
        layout.addWidget(type_label)

        type_row = QHBoxLayout()
        self.btn_video = QPushButton("🎬  Video")
        self.btn_video.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_video.clicked.connect(lambda: self._set_type("video"))

        self.btn_audio = QPushButton("🎵  Audio")
        self.btn_audio.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_audio.clicked.connect(lambda: self._set_type("audio"))

        type_row.addWidget(self.btn_video)
        type_row.addWidget(self.btn_audio)
        layout.addLayout(type_row)
        self._update_type_buttons()

        # ── Formato + Calidad ──
        options_row = QHBoxLayout()

        fmt_col = QVBoxLayout()
        fmt_lbl = QLabel("Formato:")
        fmt_lbl.setStyleSheet(f"color: {APP_COLORS['text_muted']}; font-size: 9pt;")
        self.fmt_combo = QComboBox()
        self.fmt_combo.setStyleSheet(COMBO_STYLE_LC)
        self._populate_format_combo()
        fmt_col.addWidget(fmt_lbl)
        fmt_col.addWidget(self.fmt_combo)
        options_row.addLayout(fmt_col)

        options_row.addSpacing(20)

        qual_col = QVBoxLayout()
        qual_lbl = QLabel("Calidad (video):")
        qual_lbl.setStyleSheet(f"color: {APP_COLORS['text_muted']}; font-size: 9pt;")
        self.quality_lbl = qual_lbl
        self.qual_combo = QComboBox()
        self.qual_combo.setStyleSheet(COMBO_STYLE_LC)
        self.qual_combo.addItems(["Mejor disponible", "1080p", "720p", "480p", "360p"])
        qual_col.addWidget(qual_lbl)
        qual_col.addWidget(self.qual_combo)
        options_row.addLayout(qual_col)

        layout.addLayout(options_row)

        # ── Progreso ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(PROGRESS_STYLE)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"color: {APP_COLORS['text_muted']}; font-size: 9pt;")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

        # ── Botón Descargar ──
        self.download_btn = QPushButton("⬇  Descargar")
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self._start_download)
        layout.addWidget(self.download_btn)
        self._update_download_btn()

        outer.addWidget(card)
        self.setLayout(outer)

    # ──────────────────────────────────────────
    #  Lógica de URL / plataforma
    # ──────────────────────────────────────────
    def _on_url_changed(self, text: str):
        text = text.strip()
        if not text:
            self._clear_logo()
            self.platform_name_label.setText("")
            self._audio_only = False
            self._set_type("video")
            self._update_download_btn()
            return

        name, icon, audio_only = detect_platform(text)
        self._audio_only = audio_only
        self._current_platform = name

        # Mostrar logo
        if icon:
            pix = QPixmap(get_icon_path(icon))
            if not pix.isNull():
                self.platform_logo.setPixmap(
                    pix.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
                )
            else:
                self._clear_logo()
        else:
            self._clear_logo()

        self.platform_name_label.setText(name)

        # Si es solo audio, forzar modo audio y deshabilitar video
        if audio_only:
            self._set_type("audio")
        else:
            self._update_type_buttons()

        self._update_download_btn()

    def _clear_logo(self):
        self.platform_logo.clear()
        self.platform_logo.setText("🔗")
        self.platform_logo.setStyleSheet(f"font-size: 48pt; color: {APP_COLORS['text_muted']};")

    # ──────────────────────────────────────────
    #  Tipo Video / Audio
    # ──────────────────────────────────────────
    def _set_type(self, t: str):
        self._media_type = t
        self._update_type_buttons()
        self._populate_format_combo()
        qual_visible = (t == "video")
        self.qual_combo.setVisible(qual_visible)
        self.quality_lbl.setVisible(qual_visible)

    def _update_type_buttons(self):
        # Video
        if self._audio_only:
            self.btn_video.setStyleSheet(TYPE_BTN_DISABLED)
            self.btn_video.setEnabled(False)
            self.btn_video.setCursor(Qt.CursorShape.ForbiddenCursor)
        else:
            self.btn_video.setEnabled(True)
            self.btn_video.setCursor(Qt.CursorShape.PointingHandCursor)
            if self._media_type == "video":
                self.btn_video.setStyleSheet(TYPE_BTN_ACTIVE)
            else:
                self.btn_video.setStyleSheet(TYPE_BTN_INACTIVE)

        # Audio
        if self._media_type == "audio":
            self.btn_audio.setStyleSheet(TYPE_BTN_ACTIVE)
        else:
            self.btn_audio.setStyleSheet(TYPE_BTN_INACTIVE)

    def _populate_format_combo(self):
        self.fmt_combo.clear()
        if self._media_type == "video":
            self.fmt_combo.addItems(["mp4", "mkv", "webm", "avi"])
        else:
            self.fmt_combo.addItems(["mp3", "m4a", "flac", "ogg", "wav"])

    # ──────────────────────────────────────────
    #  Botón Descargar
    # ──────────────────────────────────────────
    def _update_download_btn(self):
        has_url = bool(self.url_input.text().strip())
        if has_url:
            self.download_btn.setEnabled(True)
            self.download_btn.setStyleSheet(DOWNLOAD_BTN_ACTIVE)
        else:
            self.download_btn.setEnabled(False)
            self.download_btn.setStyleSheet(DOWNLOAD_BTN_DISABLED)

    # ──────────────────────────────────────────
    #  Descarga
    # ──────────────────────────────────────────
    def _start_download(self):
        url = self.url_input.text().strip()
        if not url:
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de descarga")
        if not output_dir:
            return

        fmt = self.fmt_combo.currentText()
        quality_map = {
            "Mejor disponible": "best",
            "1080p": "1080",
            "720p": "720",
            "480p": "480",
            "360p": "360",
        }
        quality = quality_map.get(self.qual_combo.currentText(), "best")

        # Preparar UI para descarga
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setVisible(True)
        self.status_label.setText("Iniciando descarga...")
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet(DOWNLOAD_BTN_DISABLED)
        self.url_input.setEnabled(False)
        QApplication.processEvents()

        from apps.link_converter.downloader import DownloadWorker
        self._worker = DownloadWorker(
            url=url,
            media_type=self._media_type,
            fmt=fmt,
            quality=quality,
            output_dir=output_dir,
        )
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(lambda title: self._on_finished(title, output_dir))
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_progress(self, percent: int, text: str):
        self.progress_bar.setValue(percent)
        self.status_label.setText(text)

    def _on_finished(self, title: str, output_dir: str):
        self.progress_bar.setValue(100)
        self.status_label.setText("✅ ¡Descarga completada!")
        self._reset_ui()

        QMessageBox.information(
            self,
            "Descarga completada",
            f"✅ Descargado correctamente:\n\n\"{title}\"\n\nGuardado en:\n{output_dir}",
        )
        try:
            os.startfile(output_dir)
        except Exception:
            try:
                import subprocess
                subprocess.Popen(["xdg-open", output_dir])
            except Exception:
                pass

    def _on_error(self, message: str):
        self.progress_bar.setVisible(False)
        self.status_label.setVisible(False)
        self._reset_ui()
        QMessageBox.critical(
            self,
            "Error en la descarga",
            f"❌ No se pudo completar la descarga:\n\n{message}",
        )

    def _reset_ui(self):
        self.url_input.setEnabled(True)
        self._update_download_btn()

    # ──────────────────────────────────────────
    #  Navegación
    # ──────────────────────────────────────────
    def go_back(self):
        from core.ui.hub_window import HubWindow
        self.hub = HubWindow()
        self.hub.show()
        self.close()
