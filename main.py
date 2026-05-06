from src.ui.index import LauncherWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
	app = QApplication(sys.argv)
	window = LauncherWindow()
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
    main()
