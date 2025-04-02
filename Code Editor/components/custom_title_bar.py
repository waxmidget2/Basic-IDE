from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPalette, QColor, QIcon

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(40,40,40))
        
        self.setPalette(palette)
        
        layout = QHBoxLayout(self)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        
        # Icon
        self.icon = QLabel()
        self.icon.setPixmap(QIcon(":window-icon").pixmap(16, 16))
        layout.addWidget(self.icon)
        
        # Title
        self.title = QLabel("SQUIB IDE")
        self.title.setStyleSheet("color: #FFFEE9; font-weight: Bold;")
        layout.addWidget(self.title)
        
        
    
        # Window buttons
        self.minimize_button = self._create_window_button("─", self.parent.showMinimized)
        self.maximize_button = self._create_window_button("□", self.toggle_maximize)
        self.close_button = self._create_window_button("✕", self.parent.close, hover_color="#E81123")
        
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)
        
    def _create_window_button(self, text, clicked_handler, hover_color="#555555"):
        button = QPushButton(text)
        button.setFixedSize(30, 25)
        button.setStyleSheet(f"""
            QPushButton {{
                color: white;
                background-color: transparent;
                border: none;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        button.clicked.connect(clicked_handler)
        return button
        
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
