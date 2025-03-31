import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ide import IDE

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ide = IDE()
    ide.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
