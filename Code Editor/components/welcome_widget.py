from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

class WelcomeWidget(QWidget):
    newRequested = pyqtSignal()
    openRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        container = QWidget()
        container.setStyleSheet("background-color: #1e1e1e;")
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("Code Editor")
        title.setStyleSheet("""
            font-size: 52px;
            color: #87b5ec;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle
        subtitle = QLabel("Start coding with a new file or open an existing project")
        subtitle.setStyleSheet("font-size: 18px; color: white; margin-bottom: 50px;")
        
        # Button Container
        btn_container = QWidget()
        btn_layout = QVBoxLayout(btn_container)
        btn_layout.setContentsMargins(2, 2, 0, 0)
        btn_layout.setSpacing(10)
        
        # Button Style
        btn_style = """
            QPushButton {
            background-color: #424244;
            color: #ffffff; 
            border: 1px solid #4d4d4f; 
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 16px;
            min-width: 250px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #3a3a3c; 
            border-color: #b0d4f5;
            color: #87b5ec;
        }

        QPushButton:pressed {
            background-color: #353537;
        }
        """
        
        btn_new = QPushButton("New File")
        btn_open = QPushButton("Open File")
        
        for btn in [btn_new, btn_open]:
            btn.setStyleSheet(btn_style)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(300, 60)
        
        btn_new.clicked.connect(self.newRequested.emit)
        btn_open.clicked.connect(self.openRequested.emit)
        
        # Layout
        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)
        container_layout.addWidget(btn_container)
        btn_layout.addWidget(btn_new, 0, Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(btn_open, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(container)
