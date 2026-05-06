from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget


APP_COLORS = {
    "bg": "#FAF7F4",
    "card": "#FFFFFF",
    "text_main": "#4B362D",
    "text_muted": "#7A5A49",
    "border": "#E9D8CD",
    "accent": "#E7BFA7",
    "accent_hover": "#DFAE90",
    "accent_soft": "#F8EEE8",
    "drop_bg": "#FCF6F1",
}

RADIUS_LG = 18
RADIUS_MD = 12
RADIUS_SM = 10


def apply_window_theme(widget: QWidget) -> None:
    widget.setStyleSheet(
        f"""
        QWidget {{
            background-color: {APP_COLORS["bg"]};
            color: {APP_COLORS["text_main"]};
            font-family: "Segoe UI", "Inter", sans-serif;
        }}
        QLabel {{
            background: transparent;
        }}
        QMessageBox {{
            background-color: {APP_COLORS["bg"]};
        }}
        QMessageBox QPushButton {{
            background: {APP_COLORS["accent_soft"]};
            border: 1px solid {APP_COLORS["border"]};
            border-radius: {RADIUS_SM}px;
            padding: 8px 14px;
            font-weight: 600;
            min-width: 90px;
        }}
        QMessageBox QPushButton:hover {{
            background: #F3E5DC;
        }}
        QProgressDialog {{
            background: {APP_COLORS["bg"]};
            border: 1px solid {APP_COLORS["border"]};
            border-radius: {RADIUS_MD}px;
        }}
        QProgressBar {{
            background: #FFFFFF;
            border: 1px solid {APP_COLORS["border"]};
            border-radius: {RADIUS_SM}px;
            min-height: 10px;
            text-align: center;
            color: {APP_COLORS["text_main"]};
        }}
        QProgressBar::chunk {{
            background: {APP_COLORS["accent"]};
            border-radius: {RADIUS_SM}px;
        }}
        """
    )


def make_card_container() -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setObjectName("mainCard")
    card.setStyleSheet(
        f"""
        QFrame#mainCard {{
            background: {APP_COLORS["card"]};
            border: 1px solid {APP_COLORS["border"]};
            border-radius: {RADIUS_LG}px;
        }}
        """
    )
    layout = QVBoxLayout(card)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(14)
    return card, layout


BUTTON_STYLE = (
    f"QPushButton{{background:{APP_COLORS['accent']};color:{APP_COLORS['text_main']};"
    f"padding:10px 12px;border-radius:{RADIUS_MD}px;border:1px solid {APP_COLORS['border']};font-weight:600;}}"
    f"QPushButton:hover{{background:{APP_COLORS['accent_hover']};}}"
    f"QPushButton:pressed{{background:#D8A587;}}"
    f"QPushButton:disabled{{background:{APP_COLORS['accent_soft']};color:#B39382;}}"
)


SOFT_BUTTON_STYLE = (
    f"QPushButton{{background:{APP_COLORS['accent_soft']};color:{APP_COLORS['text_main']};"
    f"padding:8px 10px;border-radius:{RADIUS_MD}px;border:1px solid {APP_COLORS['border']};font-weight:600;}}"
    f"QPushButton:hover{{background:#F3E5DC;}}"
    f"QPushButton:pressed{{background:#EFDCCF;}}"
)


COMBO_STYLE = (
    f"QComboBox{{background:#FFFFFF;border:1px solid {APP_COLORS['border']};padding:6px;"
    f"border-radius:{RADIUS_SM}px;color:{APP_COLORS['text_main']};min-height:18px;}}"
    f"QComboBox:hover{{border:1px solid #DDBBA8;}}"
    f"QComboBox:focus{{border:1px solid #D4AA93;}}"
    f"QComboBox::drop-down{{border:none;padding-right:6px;}}"
    f"QComboBox QAbstractItemView{{background:#FFFFFF;border:1px solid {APP_COLORS['border']};"
    f"selection-background-color:{APP_COLORS['accent_soft']};selection-color:{APP_COLORS['text_main']};}}"
)


DROP_LABEL_STYLE = (
    f"background: {APP_COLORS['drop_bg']};"
    f"border: 2px dashed {APP_COLORS['border']};"
    f"color: {APP_COLORS['text_muted']};"
    "padding: 12px;"
    f"border-radius: {RADIUS_MD}px;"
)
