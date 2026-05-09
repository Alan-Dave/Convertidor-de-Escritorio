import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QGridLayout, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize
from core.ui.hub_theme import (
    HUB_WINDOW_STYLE, HUB_TITLE_STYLE, CARD_STYLE_NORMAL, 
    CARD_STYLE_DISABLED, CARD_TITLE_STYLE, CARD_SUBTITLE_STYLE,
    BTN_INSTALL_STYLE, BTN_OPEN_STYLE, BTN_DISABLED_STYLE, PORTABLE_LABEL_STYLE
)

def get_asset_path(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, "assets", "hub", filename)

class AppCard(QFrame):
    def __init__(self, title, subtitle, icon_file, btn_text, btn_type="install", is_disabled=False, parent=None):
        super().__init__(parent)
        self.btn_type = btn_type
        
        if is_disabled:
            self.setObjectName("appCardDisabled")
            self.setStyleSheet(CARD_STYLE_DISABLED)
        else:
            self.setObjectName("appCard")
            self.setStyleSheet(CARD_STYLE_NORMAL)
            
            # Add drop shadow
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(4)
            shadow.setColor(QColor(0, 0, 0, 80))
            self.setGraphicsEffect(shadow)

        self.setFixedHeight(180)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(get_asset_path(icon_file))
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setFixedSize(100, 100)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_label)

        # Content Layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet(CARD_TITLE_STYLE)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet(CARD_SUBTITLE_STYLE)
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(subtitle_label)
        content_layout.addStretch()

        # Bottom Actions Layout
        action_layout = QHBoxLayout()
        
        self.action_btn = QPushButton(btn_text)
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if btn_type == "install":
            self.action_btn.setStyleSheet(BTN_INSTALL_STYLE)
            self.action_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ArrowDown))
        elif btn_type == "open":
            self.action_btn.setStyleSheet(BTN_OPEN_STYLE)
            self.action_btn.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogApplyButton))
        else:
            self.action_btn.setStyleSheet(BTN_DISABLED_STYLE)
            self.action_btn.setEnabled(False)
            
        action_layout.addWidget(self.action_btn)
        action_layout.addStretch()
        
        if btn_type != "disabled":
            portable_label = QLabel("🔗 PORTABLE")
            portable_label.setStyleSheet(PORTABLE_LABEL_STYLE)
            action_layout.addWidget(portable_label)
            
        content_layout.addLayout(action_layout)
        main_layout.addLayout(content_layout)


class HubWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Hub")
        self.resize(900, 600)
        self.setStyleSheet(HUB_WINDOW_STYLE)
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 30, 40, 40)
        main_layout.setSpacing(20)
        
        title_label = QLabel("MEDIA HUB")
        title_label.setObjectName("hubTitle")
        title_label.setStyleSheet(HUB_TITLE_STYLE)
        main_layout.addWidget(title_label)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # 1. Multimedia Converter
        self.media_card = AppCard(
            title="MULTIMEDIA\nCONVERTER",
            subtitle="Video, Audio, and Batch Processing",
            icon_file="media.png",
            btn_text=" ABRIR",
            btn_type="open"
        )
        self.media_card.action_btn.clicked.connect(self.launch_media_converter)
        grid_layout.addWidget(self.media_card, 0, 0)
        
        # 2. Document Converter
        self.docs_card = AppCard(
            title="DOCUMENT\nCONVERTER",
            subtitle="PDF, Word, Excel, and OCR",
            icon_file="docs.png",
            btn_text=" ABRIR",
            btn_type="open"
        )
        self.docs_card.action_btn.clicked.connect(self.launch_document_converter)
        grid_layout.addWidget(self.docs_card, 0, 1)
        
        # 3. Quality Enhancer
        self.quality_card = AppCard(
            title="QUALITY\nENHANCER",
            subtitle="AI Image Super Resolution",
            icon_file="quality.webp",
            btn_text=" ABRIR",
            btn_type="open"
        )
        self.quality_card.action_btn.clicked.connect(self.launch_quality_enhancer)
        grid_layout.addWidget(self.quality_card, 1, 0)
        
        # 4. Background Eraser
        self.bg_card = AppCard(
            title="BACKGROUND\nERASER",
            subtitle="AI-Powered Background Removal",
            icon_file="backgrounderaser.webp",
            btn_text=" ABRIR",
            btn_type="open"
        )
        self.bg_card.action_btn.clicked.connect(self.launch_bg_remover)
        grid_layout.addWidget(self.bg_card, 1, 1)
        
        # 5. Link Converter
        self.link_card = AppCard(
            title="LINK\nCONVERTER",
            subtitle="YouTube, TikTok, Instagram & more",
            icon_file="link_converter.webp",
            btn_text=" ABRIR",
            btn_type="open"
        )
        self.link_card.action_btn.clicked.connect(self.launch_link_converter)
        grid_layout.addWidget(self.link_card, 2, 0)

        main_layout.addLayout(grid_layout)
        
    def launch_media_converter(self):
        # We launch the old main index window from apps.media_converter.ui.index
        from apps.media_converter.ui.index import LauncherWindow
        self.media_window = LauncherWindow()
        self.media_window.show()
        self.close()

    def launch_document_converter(self):
        from apps.document_converter.ui.index import DocumentLauncherWindow
        self.doc_window = DocumentLauncherWindow()
        self.doc_window.show()
        self.close()

    def launch_quality_enhancer(self):
        from apps.media_converter.ui.quality_enhancer import QualityEnhancerUI
        self.quality_window = QualityEnhancerUI()
        self.quality_window.show()
        self.close()

    def launch_link_converter(self):
        from apps.link_converter.link_converter_window import LinkConverterWindow
        self.link_window = LinkConverterWindow()
        self.link_window.show()
        self.close()

    def launch_bg_remover(self):
        from apps.media_converter.ui.bg_remover import BackgroundRemoverUI
        self.bg_window = BackgroundRemoverUI()
        self.bg_window.show()
        self.close()
