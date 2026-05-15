from core.ui.hub_window import HubWindow
from PyQt6.QtWidgets import QApplication
import sys

import traceback
from PyQt6.QtWidgets import QMessageBox

def global_exception_handler(exc_type, exc_value, exc_traceback):
    err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(err_msg)
    # Evitar crear un nuevo QApplication si ya existe
    if QApplication.instance():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error Fatal")
        msg.setText("Ocurrió un error inesperado en la aplicación.")
        msg.setDetailedText(err_msg)
        msg.exec()

sys.excepthook = global_exception_handler

def main():
    app = QApplication(sys.argv)
    window = HubWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
