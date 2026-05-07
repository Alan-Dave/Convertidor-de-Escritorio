import sys
import os
import datetime
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QComboBox, QHBoxLayout, QProgressDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from apps.media_converter.converters.conversion import ImageFormats
from apps.media_converter.ui.ui_theme import (
    APP_COLORS,
    BUTTON_STYLE,
    COMBO_STYLE,
    DROP_LABEL_STYLE,
    SOFT_BUTTON_STYLE,
    REMOVE_BUTTON_STYLE,
    CONVERT_BUTTON_STYLE,
    apply_window_theme,
    make_card_container,
)

CONVERT_FUNCTIONS = {
    ("jpg", "png"): ImageFormats.convertir_jpg_a_png,
    ("jpg", "webp"): ImageFormats.convertir_jpg_a_webp,
    ("png", "jpg"): ImageFormats.convertir_png_a_jpg,
    ("png", "webp"): ImageFormats.convertir_png_a_webp,
    ("webp", "jpg"): ImageFormats.convertir_webp_a_jpg,
    ("webp", "png"): ImageFormats.convertir_webp_a_png,
}
IMAGE_FORMATS = ["png", "jpg", "webp"]


class ImageDropLabel(QLabel):
    def __init__(self, on_image_dropped, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Arrastra aquí una imagen")
        self.setStyleSheet(f"{DROP_LABEL_STYLE}min-height: 180px;")
        self.setAcceptDrops(True)
        self.image_path = None
        self.on_image_dropped = on_image_dropped
        self.allowed_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(self.allowed_extensions):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith(self.allowed_extensions):
                self.image_path = file_path
                pixmap = QPixmap(file_path)
                self.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
                self.on_image_dropped(file_path)
            else:
                QMessageBox.warning(self, "Formato no soportado", "Este archivo no es una imagen válida para esta sección.")
        else:
            event.ignore()


class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor de Imágenes")
        self.setGeometry(100, 100, 480, 560)
        apply_window_theme(self)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(26, 24, 26, 24)
        card, card_layout = make_card_container()

        top_layout = QHBoxLayout()
        back_btn = QPushButton("← Volver")
        back_btn.setFixedWidth(90)
        back_btn.clicked.connect(self.go_back)
        back_btn.setStyleSheet(SOFT_BUTTON_STYLE)
        top_layout.addWidget(back_btn)
        top_layout.addStretch()
        card_layout.addLayout(top_layout)

        self.label = QLabel("Selecciona o arrastra una imagen para convertir")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(f"color: {APP_COLORS['text_main']}; font-size: 14pt; font-weight:600;")
        card_layout.addWidget(self.label)

        self.image_label = ImageDropLabel(self.on_image_dropped, self)
        card_layout.addWidget(self.image_label)

        combo_layout = QHBoxLayout()
        self.from_combo = QComboBox()
        self.from_combo.addItems(["png", "jpg", "webp"])
        self.from_combo.setEnabled(False)
        combo_layout.addWidget(QLabel("Formato de origen:"))
        combo_layout.addWidget(self.from_combo)

        self.to_combo = QComboBox()
        self.to_combo.addItems(["png", "jpg", "webp"])
        combo_layout.addWidget(QLabel("Formato de destino:"))
        combo_layout.addWidget(self.to_combo)
        card_layout.addLayout(combo_layout)

        self.select_button = QPushButton("Seleccionar Imagen")
        self.select_button.clicked.connect(self.select_image)
        self.select_button.setStyleSheet(BUTTON_STYLE)
        card_layout.addWidget(self.select_button)

        self.select_folder_button = QPushButton("Seleccionar Carpeta")
        self.select_folder_button.clicked.connect(self.select_folder)
        self.select_folder_button.setStyleSheet(BUTTON_STYLE)
        card_layout.addWidget(self.select_folder_button)

        self.remove_button = QPushButton("Quitar Archivo")
        self.remove_button.clicked.connect(self.remove_image)
        self.remove_button.setEnabled(False)
        self.remove_button.setStyleSheet(REMOVE_BUTTON_STYLE)
        card_layout.addWidget(self.remove_button)

        self.convert_button = QPushButton("Convertir Archivo")
        self.convert_button.clicked.connect(self.convert_image)
        self.convert_button.setEnabled(False)
        self.convert_button.setStyleSheet(CONVERT_BUTTON_STYLE)
        card_layout.addWidget(self.convert_button)

        self.from_combo.setStyleSheet(COMBO_STYLE)
        self.to_combo.setStyleSheet(COMBO_STYLE)
        for i in range(combo_layout.count()):
            widget = combo_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setStyleSheet(f"color: {APP_COLORS['text_muted']};")

        self.layout.addWidget(card)
        self.setLayout(self.layout)
        self.image_path = None
        self.batch_files = []

    def go_back(self):
        from apps.media_converter.ui.index import LauncherWindow
        self.index_window = LauncherWindow()
        self.index_window.show()
        self.close()

    def select_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp *.webp)")
        if file_path:
            self.batch_files = []
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
            ext = os.path.splitext(file_path)[1].lstrip('.').lower()
            if ext == 'jpeg':
                ext = 'jpg'
            if ext in IMAGE_FORMATS:
                idx = self.from_combo.findText(ext)
                if idx != -1:
                    self.from_combo.setCurrentIndex(idx)
                self.from_combo.setEnabled(False)
                dests = [f for f in IMAGE_FORMATS if f != ext]
                self.to_combo.clear()
                self.to_combo.addItems(dests)
            self.convert_button.setEnabled(True)
            self.remove_button.setEnabled(True)

    def on_image_dropped(self, file_path):
        self.batch_files = []
        self.image_path = file_path
        ext = os.path.splitext(file_path)[1].lstrip('.').lower()
        if ext == 'jpeg':
            ext = 'jpg'
        if ext in IMAGE_FORMATS:
            idx = self.from_combo.findText(ext)
            if idx != -1:
                self.from_combo.setCurrentIndex(idx)
            self.from_combo.setEnabled(False)
            dests = [f for f in IMAGE_FORMATS if f != ext]
            self.to_combo.clear()
            self.to_combo.addItems(dests)
        self.convert_button.setEnabled(True)
        self.remove_button.setEnabled(True)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Imágenes")
        if not folder_path:
            return
        valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
        files = []
        for root, _, names in os.walk(folder_path):
            for name in names:
                ext = os.path.splitext(name)[1].lower()
                if ext in valid_exts:
                    files.append(os.path.join(root, name))
        if not files:
            QMessageBox.warning(self, "Sin archivos", "No se encontraron imágenes compatibles en la carpeta.")
            return
        self.image_path = None
        self.batch_files = files
        self.image_label.clear()
        self.image_label.setText(f"{len(files)} imágenes seleccionadas")
        self.from_combo.clear()
        self.from_combo.addItem("varios")
        self.to_combo.clear()
        self.to_combo.addItems(IMAGE_FORMATS)
        self.convert_button.setEnabled(True)
        self.remove_button.setEnabled(True)

    def remove_image(self):
        self.image_path = None
        self.batch_files = []
        self.image_label.clear()
        self.image_label.setText("Arrastra aquí una imagen")
        self.convert_button.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.from_combo.clear()
        self.from_combo.addItems(IMAGE_FORMATS)
        self.from_combo.setCurrentIndex(0)
        self.from_combo.setEnabled(False)
        self.to_combo.clear()
        self.to_combo.addItems(IMAGE_FORMATS)

    def choose_output_folder(self):
        return QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")

    def convert_image(self):
        output_dir = self.choose_output_folder()
        if not output_dir:
            return

        if self.batch_files:
            if len(self.batch_files) > 5:
                folder_name = "Conversion_Masiva_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = os.path.join(output_dir, folder_name)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
            to_format = self.to_combo.currentText()
            converted = 0
            skipped = 0
            failed = 0
            total = len(self.batch_files)
            progress = QProgressDialog("Convirtiendo imágenes...", None, 0, total, self)
            progress.setWindowTitle("Procesando")
            progress.setWindowModality(Qt.WindowModality.ApplicationModal)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            progress.show()
            QApplication.processEvents()

            try:
                for idx, file_path in enumerate(self.batch_files, start=1):
                    from_format = os.path.splitext(file_path)[1].lstrip(".").lower()
                    if from_format == "jpeg":
                        from_format = "jpg"
                    if from_format == to_format:
                        skipped += 1
                    else:
                        func = CONVERT_FUNCTIONS.get((from_format, to_format))
                        if not func:
                            failed += 1
                        else:
                            nombre = os.path.splitext(os.path.basename(file_path))[0]
                            ruta_destino = os.path.join(output_dir, f"{nombre}.{to_format}")
                            result = func(file_path, ruta_destino)
                            if str(result).startswith("✅"):
                                converted += 1
                            else:
                                failed += 1
                    progress.setLabelText(f"Convirtiendo imágenes... ({idx}/{total})")
                    progress.setValue(idx)
                    QApplication.processEvents()
            finally:
                progress.close()

            QMessageBox.information(
                self,
                "Conversión masiva",
                f"Convertidos: {converted}\nOmitidos (mismo formato): {skipped}\nFallidos: {failed}",
            )
            try:
                os.startfile(output_dir)
            except AttributeError:
                subprocess.Popen(["xdg-open", output_dir])
            return

        if not self.image_path:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una imagen primero.")
            return
        from_format = self.from_combo.currentText()
        to_format = self.to_combo.currentText()
        if from_format == to_format:
            QMessageBox.warning(self, "Advertencia", "El formato de origen y destino no pueden ser iguales.")
            return

        func = CONVERT_FUNCTIONS.get((from_format, to_format))
        if not func:
            QMessageBox.warning(self, "Error", "Conversión no soportada.")
            return

        nombre = os.path.splitext(os.path.basename(self.image_path))[0]
        ruta_destino = os.path.join(output_dir, f"{nombre}.{to_format}")

        progress = QProgressDialog("Convirtiendo imagen...", None, 0, 0, self)
        progress.setWindowTitle("Procesando")
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress.setMinimumDuration(0)
        progress.show()
        QApplication.processEvents()
        try:
            resultado = func(self.image_path, ruta_destino)
        finally:
            progress.close()

        QMessageBox.information(self, "Conversión", resultado)
        try:
            os.startfile(output_dir)
        except AttributeError:
            subprocess.Popen(['xdg-open', output_dir])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverter()
    window.show()
    sys.exit(app.exec())
