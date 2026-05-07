from core.ui.hub_window import HubWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
	app = QApplication(sys.argv)
	window = HubWindow()
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
    main()
