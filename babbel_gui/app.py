from PyQt6.QtWidgets import QApplication
from babbel_gui.ui.main_window import MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Babbel")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
