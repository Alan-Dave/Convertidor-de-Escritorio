from PyQt6.QtWidgets import QWidget

HUB_BG_COLOR = "#0D2C54"

HUB_WINDOW_STYLE = f"""
    QMainWindow {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0B1D3A, stop:1 #133D7A);
    }}
"""

HUB_TITLE_STYLE = """
    QLabel#hubTitle {
        color: white;
        font-size: 24pt;
        font-weight: bold;
        font-family: "Segoe UI", "Arial", sans-serif;
    }
"""

CARD_STYLE_NORMAL = """
    QFrame#appCard {
        background-color: #F8F9FB;
        border-radius: 12px;
    }
"""

CARD_STYLE_DISABLED = """
    QFrame#appCardDisabled {
        background-color: #D3D8DE;
        border-radius: 12px;
    }
"""

CARD_TITLE_STYLE = """
    QLabel {
        color: #1A1A1A;
        font-size: 16pt;
        font-weight: 900;
        font-family: "Segoe UI", "Arial", sans-serif;
    }
"""

CARD_SUBTITLE_STYLE = """
    QLabel {
        color: #555555;
        font-size: 10pt;
        font-family: "Segoe UI", "Arial", sans-serif;
    }
"""

BTN_INSTALL_STYLE = """
    QPushButton {
        background-color: #218838;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 11pt;
    }
    QPushButton:hover {
        background-color: #28A745;
    }
    QPushButton:pressed {
        background-color: #1E7E34;
    }
"""

BTN_OPEN_STYLE = """
    QPushButton {
        background-color: #0069D9;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 11pt;
    }
    QPushButton:hover {
        background-color: #007BFF;
    }
    QPushButton:pressed {
        background-color: #0062CC;
    }
"""

BTN_DISABLED_STYLE = """
    QPushButton {
        background-color: #A0A5AA;
        color: #444444;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 11pt;
    }
"""

PORTABLE_LABEL_STYLE = """
    QLabel {
        color: #888888;
        font-weight: bold;
        font-size: 10pt;
    }
"""
