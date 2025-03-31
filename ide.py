import sys
import os
import subprocess
import time
from PyQt6.QtCore import Qt, QDir, QProcess, QRegularExpression, QSize, pyqtSignal
from PyQt6.QtGui import (QPainter, QSyntaxHighlighter, QPalette, QTextCharFormat, QColor, QFont,
                         QTextCursor, QAction, QIcon, QFileSystemModel, 
                         QRegularExpressionValidator, QKeySequence, QFontMetrics, QTextDocument)
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QSplitter, QTreeView, QTabWidget,
                            QTextEdit, QFrame, QToolBar, QStatusBar, QMenuBar,
                            QMessageBox, QFileDialog, QStackedWidget,
                            QLabel, QPushButton, QSizePolicy, QListWidget,
                            QListWidgetItem, QStyleFactory, QComboBox, QDialog, QLineEdit, QCheckBox)

from components.code_editor import CodeEditor
from components.custom_title_bar import CustomTitleBar
from components.welcome_widget import WelcomeWidget
from components.python_highlighter import PythonHighlighter

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1280, 720)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("IDE")
        
        
        self.current_file = None
        self.unsaved_changes = False
        self.setup_ui()
        self.setup_connections()
        self.apply_styles()
        self.old_pos = None

    def setup_ui(self):
    # Central Widget and Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.title_bar = CustomTitleBar(self)
        self.title_bar.setFixedHeight(30)

        

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 1)
        self.main_layout.setSpacing(2)
        
        
        # Create a horizontal layout for the title bar
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.addWidget(self.title_bar)
        
        self.title_bar.setStyleSheet("""CustomTitleBar{
                                        color: #FFFEE9;
                                     }""")
        # Add title bar layout to main layout
        self.main_layout.addLayout(title_bar_layout)
        
        

        # File Explorer
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(os.getcwd()))
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setAnimated(True)
        self.file_tree.setIndentation(1)
        self.file_tree.setAllColumnsShowFocus(True)
        self.file_tree.dragDropMode()
        self.file_tree.setSortingEnabled(True)
        
        self.file_tree.setStyleSheet("""
            QScrollBar:vertical {border: none;background-color: transparent;width: 10px;margin: 25px 0 0px 0;}\
            QScrollBar::handle:vertical{border-radius: 4px;border-color: rgba(216, 216, 216, 75%);border-width: 1px; border-style: solid; background-color: rgba(216, 216, 216, 75%); min-height: 25px;}\
            QScrollBar::add-line:vertical{width: 0px; height: 0px;}\
            QScrollBar::sub-line:vertical{width: 0px; height: 0px;}\
            QScrollBar::add-page:vertical{background-color: transparent;}\
            QScrollBar::sub-page:vertical{background-color: transparent;}\
            QScrollBar:horizontal {border: none;background-color: transparent;width: 10px;margin: 25px 0 10px 0;}\
            QTreeView {background-color: #222222; color: #f1f1f1}
            """)
        
        # Editor Area
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setStyleSheet("padding: 0px;")
        self.tab_widget.ensurePolished()

        # Console
        self.console = QTextEdit()
        self.userConsole = QLineEdit()        
        self.userConsole.editingFinished.connect(self.push_console)
        self.process = None
        self.userConsole.setPlaceholderText("Terminal")
        
        
        self.main_layout.setContentsMargins(1, 1, 1, 1) 
        self.main_layout.setSpacing(3)

        # Reduce margins for other layouts
        if hasattr(self, 'editor_splitter'):
            self.editor_splitter.setContentsMargins(1, 1, 1, 1)
        
        if hasattr(self, 'main_splitter'):
            self.main_splitter.setContentsMargins(1, 1, 1, 1)
        self.userConsole.setStyleSheet("""
            QLineEdit {

                background-color: #191919;  /* Slightly lighter than console background */
                color: #d4d4d4;  /* Light gray text */
            
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12pt;
                
                padding: 5px 5px;

                border: 3px solid #2c2c2c; 
                border-radius: 3px; 
        
                selection-background-color: #264f78;
                selection-color: #ffffff;
            }

            /* Placeholder text styling */
            QLineEdit::placeholder {
                color: #6b6b6b;
                font-style: italic;
            }

            /* Hover and focus states */
            QLineEdit:hover {
                border-color: #3c3c3c;
            }

            QLineEdit:focus {
                border-color: #e1e1e1;  /* Accent color for focus state */
                outline: none;
            }

            /* Clear button styling (if applicable) */
            QLineEdit::clear-button {
                image: url(:/icons/clear.png);  /* Optional: replace with your clear icon */
                width: 18px;
                height: 18px;
                margin-right: 5px;
            }
                                       """)
        self.console.setStyleSheet("""
            QTextEdit {
                /* Base background and text colors */
                background-color: #1e1e1e;  /* Dark background */
                color: #d4d4d4;  /* Light gray text */
                
                /* Typography */
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
                line-height: 1.5;
                
                /* Padding and spacing */
                padding: 15px;
                
                /* Enhanced border styling */
                border: 2px solid #3c3c3c;  /* Slightly defined border */
                border-radius: 2px;  /* Rounded corners */
                background-clip: border;
                
                
                /* Selection highlighting */
                selection-background-color: #264f78;  /* VS Code-like selection */
                selection-color: #ffffff;
                
            }

            /* Placeholder text styling */
            QTextEdit::placeholder {
                color: #6b6b6b;
                font-style: italic;
            }

            /* Optional: Hover and focus effects */
            QTextEdit:hover {
                border-color: #6b6b6b;
            }

            QTextEdit:focus {
                border-color: white;  /* Accent color for focus state */
                outline: none;
            }
        """)
        
        # Welcome Screen
        self.welcome_screen = WelcomeWidget()

        # Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.numbered_lines = QWidget()

        # Editor Splitter
        self.editor_splitter = QSplitter(Qt.Orientation.Vertical)

        self.editor_splitter.addWidget(self.tab_widget)
        self.editor_splitter.addWidget(self.console)
        self.editor_splitter.addWidget(self.userConsole)
        self.editor_splitter.addWidget(self.numbered_lines)
        self.stacked_widget.addWidget(self.welcome_screen)
        self.stacked_widget.addWidget(self.editor_splitter)
        
        # Input field for interactive input
        
        self.editor_splitter.setStyleSheet("""QSplitter::handle {

                                                background-color: qlineargradient(spread:pad, x1:0.1, y1:.1, x2:.1, y2:.1, 
                                                stop:0 rgba(255, 255, 255, 20), 
                                                stop:0.2 rgba(100, 99, 100, 70), 
                                                stop:0.57 rgba(100, 99, 100, 70), 
                                                stop:0.89 rgba(100, 99, 100, 20));
                                                image: url(:/images/splitter.png);
                                            }""")
        
        # Main Splitter
        self.main_splitter = QSplitter()
        self.main_splitter.addWidget(self.file_tree)
        self.main_splitter.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.main_splitter)

        self.main_splitter.setStyleSheet("""QSplitter::handle {

                                                background-color: qlineargradient(spread:pad, x1:0.1, y1:.1, x2:.1, y2:.1, 
                                                stop:0 rgba(255, 255, 255, 0), 
                                                stop:0.2 rgba(100, 99, 100, 50), 
                                                stop:0.57 rgba(100, 99, 100, 50), 
                                                stop:0.89 rgba(100, 99, 100, 0));
                                                image: url(:/images/splitter.png);
                                            }""")
        
        self.main_splitter.setSizes([150, 750])
        self.editor_splitter.setSizes([750, 120, 200])
        self.console.setReadOnly(True)
        self.file_tree.setMaximumWidth(0)

        self.welcome_screen.newRequested.connect(self.new_file)
        self.welcome_screen.openRequested.connect(self.open_file)
        
        self.setup_find_shortcut()
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("padding-bottom:4px")
        self.installEventFilter(self)


        self.setup_toolbar()
        
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #383838;
                border: 1.2px solid #545454; 
                border-radius: 2px;
            }

            QTabWidget {
                background-color: #252526;
                color: #e9e9e9;
                border: none;
                margin: 1px;
            }

            QTabWidget::pane {
                border: 1px transparent;
                background-color: #252526;
                padding: 7px;
            }

            QTabBar {
                background-color: #383838;
                margin: 1px;
            }
            QTabBar::tab::selected {
                background-color: #252526;     
            }

            QTabBar::tab {
                background-color: #1e1e1e;
                color: #f1f1f1;
                padding: 7px 14px;
                margin-right: 1px;
                border: 10px;
                border-top-left-radius: 1px;
                border-top-right-radius: 1px;
                min-width: 1px;
                text-align: center;
                font-weight: 500;
            }

            QTreeView {
                background-color: #252526;
                color: #d4d4d4;
                margin: 2px;
                padding: 1px;
            }

            QSplitter {
                margin: 0px;
            }

            QToolBar {
                margin: 2px;
                padding: 3px;
            }

            QStatusBar {
                
                                                background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:3, y2:3, 
                                                stop:.2 rgba(30, 45, 75, 90), 
                                                stop:0.3 rgba(30, 45, 85, 105), 
                                                stop:0.2 rgba(30, 45, 85, 105), 
                                                stop:0.9 rgba(30, 45, 75, 90));
                                                image: url(:/images/statusbar.png);
            }

            QLineEdit, QTextEdit {
                margin: 2px;
                padding: 2px;
            }
        
        """)

    def setup_menu(self):
        self.menu_bar = QMenuBar(self)
        
        # File Menu
        file_menu = self.menu_bar.addMenu("&File")
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        file_menu.setStyleSheet("padding-top: 20px;")

        # Edit Menu
        edit_menu = self.menu_bar.addMenu("&Edit")
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.undo)
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.redo)
        
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Run Menu
        run_menu = self.menu_bar.addMenu("&Run")
        run_action = QAction("Run Code", self)
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)
        self.menu_bar.resize(600,20)
        
        self.main_layout.addWidget(self.menu_bar)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.position().toPoint() - self.old_pos
            self.move(self.pos() + delta)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = None
    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setAllowedAreas(Qt.ToolBarArea.BottomToolBarArea | Qt.ToolBarArea.LeftToolBarArea)
    
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, toolbar)
        
        self.drop_down = QComboBox(self)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText('File Viewer  ')

        self.show_files = QCheckBox()
        
        self.drop_down.addItems([
            'Python', 'C++', 'C', 'Java', 'JavaScript', 
            'HTML', 'CSS', 'Ruby', 'Go', 'Rust', 
            'Swift', 'PHP', 'Plain Text'
        ])
        self.drop_down.currentTextChanged.connect(self.change_language_highlighting)
        
        actions = [
            ("New File", "document-new", self.new_file),
            ("Open Project", "folder-open", self.open_project),
            ("Open File", "document-open", self.open_file),
            ("Save File", "document-save", self.save_file),
            ("Run Code", "system-run", self.run_code),
            
        ]
        
        toolbar.addWidget(self.show_files)
        self.show_files.stateChanged.connect(self.show_file_tree)

        toolbar.addWidget(self.label)
        for text, icon, handler in actions:
            action = QAction(QIcon.fromTheme(icon), text, self)
            action.triggered.connect(handler)
            toolbar.addAction(action)
    
        
        toolbar.addWidget(self.drop_down)
        

        toolbar.setStyleSheet("""
        QLabel {
            background: 2c2c2c;
            color: #e0e0e0;
            padding-bottom: 3px;
            border: 1px solid transparent;
            margin: 0 3px;
            font-weight: 600;                     
        }
        QToolBar {
            background: #1f1f1f;
            padding: 10px;
            border-top: 0px;
            border-bottom: 1px solid #303030;
        }

        QToolButton {
            background: #2c2c2c;
            color: #e0e0e0;
            padding: 6px 15px;
            border: 1px solid transparent;
            border-radius: 4px;
            margin: 0 6px;
            min-width: 100px;
            font-weight: 600;
        }

        QToolButton:hover {
            background: #353535;
            border-color: #3a8bca;
            color: #ffffff;
        }

        QToolButton:pressed {
            background: #3a3a3a;
            border-color: #2a7db5;
            color: #ffffff;
        }
        """)

    def setup_connections(self):
        self.file_tree.doubleClicked.connect(self.open_file_from_tree)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

    def new_file(self):
        editor = CodeEditor()
        editor.file_path = None  
        self.tab_widget.addTab(editor, "Untitled")
        self.tab_widget.setCurrentWidget(editor)
        self.stacked_widget.setCurrentIndex(1)
        self.unsaved_changes = True
    def open_project(self):
        path = QFileDialog.getExistingDirectory(self, "Open File", "Folder")
        if path:
            directory = os.path.abspath(path)

            print(directory)
            
            QDir.setCurrent(directory) 

            self.file_model.setRootPath(directory)

            self.file_tree.setRootIndex(self.file_model.index(directory))
    
    def open_file(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py)")
            
            if path:
                self.load_file(path)

                self.stacked_widget.setCurrentIndex(1)
            
        except:
            QMessageBox.critical(self, "Error", f"Could not Open File")
    def load_file(self, path):
        try:
            with open(path, 'r') as f:
                content = f.read()
            
            editor = CodeEditor()
            editor.setPlainText(content)
            
            
            directory = os.path.dirname(path)
            QDir.setCurrent(directory)

            self.file_model.setRootPath(directory)
            self.file_tree.setRootIndex(self.file_model.index(directory)) 
            file_extension = os.path.splitext(path)[1].lower()
            language = self.get_language_for_extension(file_extension)
            
            self.tab_widget.addTab(editor, os.path.basename(path))
            self.tab_widget.setCurrentWidget(editor)
            
            self.drop_down.setCurrentText(language)
            self.current_file = path
            self.unsaved_changes = False
            

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def save_file(self):
        current_editor = self.tab_widget.currentWidget()
        
        if not current_editor:
            QMessageBox.warning(self, "Error", "No active editor")
            return
        
        current_tab_text = self.tab_widget.tabText(self.tab_widget.currentIndex())
        
        # If the file is not Untitled and has been previously saved
        if current_tab_text != "Untitled":
            try:
                with open(current_tab_text, 'w') as f:
                    f.write(current_editor.toPlainText())
                self.statusBar().showMessage(f"File saved: {current_tab_text}")
                self.unsaved_changes = False
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file: {e}")
        else:
            # If it's an Untitled file, always prompt for save location
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py);;All Files (*)")
            
            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        f.write(current_editor.toPlainText())
                    
                    # Update tab text with filename
                    current_index = self.tab_widget.currentIndex()
                    self.tab_widget.setTabText(current_index, os.path.basename(file_path))
                    
                    # Add file_path attribute to the editor
                    current_editor.file_path = file_path
                    
                    self.statusBar().showMessage(f"File saved: {file_path}")
                    self.unsaved_changes = False
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error saving file: {e}")
    def get_language_for_extension(self, extension):
        language_map = {
            '.py': 'Python',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.java': 'Java',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.swift': 'Swift',
            '.php': 'PHP'
        }
        
        return language_map.get(extension, 'Plain Text')
    
    def show_file_tree(self, state):
        if state == Qt.CheckState.Checked.value:
            self.file_tree.setMaximumWidth(150)
        else:
            self.file_tree.setMaximumWidth(0)
            
    def change_language_highlighting(self, language):
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            current_editor.highlighter = PythonHighlighter(current_editor.document(), language)

    def close_tab(self, index):
        if self.unsaved_changes:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Save before closing?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()

            elif reply == QMessageBox.StandardButton.Cancel:
                return
        
        self.tab_widget.removeTab(index)

        if self.tab_widget.count() == 0:
            self.stacked_widget.setCurrentIndex(0)
    def push_numbered_lines(self):
        current_editor = self.tab_widget.currentWidget()
        test = current_editor.toPlainText()
        current_editor.setText
        print(test)
    def push_console(self):
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            input_text = self.userConsole.text() + "\n"
            self.process.write(input_text.encode("utf-8"))
            self.console.insertPlainText(input_text)
            self.userConsole.clear()
            self.push_numbered_lines()
        else:
            try:
                command = self.userConsole.text().strip()
                self.userConsole.clear()
                if not command:
                    self.console.append("Error: No command entered")

                if self.process:
                    self.process.kill()
                    self.process = None
                        
                self.process = QProcess()
                self.process.setProgram("cmd")
                self.process.setArguments(["/c", command])

                self.process.readyReadStandardOutput.connect(self.handle_stdout)
                self.process.readyReadStandardError.connect(self.handle_stderr)
                self.process.finished.connect(self.process_finished)
                    
                self.process.start()

                self.console.append(f"Running: {command}\n")
                self.console.append("-" * 50 + "\n")
            except:
                QMessageBox.warning(self, "Error", "No running process to send input.")
        
    def run_code(self):
        self.console.clear()
        
        current_editor = self.tab_widget.currentWidget()
        if not current_editor:
            QMessageBox.warning(self, "Error", "No active editor")
            return
        
        code = current_editor.toPlainText()
        
        temp_file = "temp_script.py"
        try:
            with open(temp_file, "w") as f:
                f.write(code)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create temp file: {e}")
            return
        
        if self.process:
            self.process.kill()
            self.process = None
            
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        
        self.process.start(sys.executable, ["-u", temp_file])
        
        self.console.append(f"Running: python -u {temp_file}\n")
        self.console.append("-" * 50 + "\n")

    def handle_stdout(self):
        if self.process:
            data = self.process.readAllStandardOutput().data().decode()
            self.append_output(data)

    def handle_stderr(self):
        if self.process:
            data = self.process.readAllStandardError().data().decode()
            self.append_output(f'<span style="color:red">{data}</span>')
    
    
    def setup_find_shortcut(self):
        find_shortcut = QAction(self)
        find_shortcut.setShortcut(QKeySequence("Ctrl+F"))
        find_shortcut.triggered.connect(self.show_find_dialog)
        self.addAction(find_shortcut)

    def show_find_dialog(self):
        
        current_editor = self.tab_widget.currentWidget()
        if not current_editor:
            QMessageBox.warning(self, "Error", "No active editor")
            return
        
        find_dialog = QDialog(self)
        find_dialog.setWindowTitle("Find")
        find_dialog.setModal(False)
        
        layout = QVBoxLayout(find_dialog)
        
        find_input = QLineEdit()
        find_input.setPlaceholderText("Enter text to find")
        layout.addWidget(find_input)
        
        options_layout = QHBoxLayout()
        case_sensitive = QCheckBox("Case Sensitive")
        whole_word = QCheckBox("Whole Word")
        options_layout.addWidget(case_sensitive)
        options_layout.addWidget(whole_word)
        layout.addLayout(options_layout)
        
        button_layout = QHBoxLayout()
        find_next_btn = QPushButton("Find Next")
        find_prev_btn = QPushButton("Find Previous")
        button_layout.addWidget(find_next_btn)
        button_layout.addWidget(find_prev_btn)
        layout.addLayout(button_layout)
        
        def find_text(forward=True):
            text_to_find = find_input.text()
            if not text_to_find:
                return
            
            options = QTextDocument.FindFlag(0)
            if case_sensitive.isChecked():
                options |= QTextDocument.FindCaseSensitively()
            if whole_word.isChecked():
                options |= QTextDocument.FindWholeWords
            
            if not forward:
                options |= QTextDocument.FindBackward
            
            cursor = current_editor.textCursor()
            found = current_editor.find(text_to_find, options)
            
            if not found:
                QMessageBox.information(find_dialog, "Find", "Text not found")
        
        find_next_btn.clicked.connect(lambda: find_text(forward=True))
        find_prev_btn.clicked.connect(lambda: find_text(forward=False))
        
        find_dialog.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #d4d4d4;
                border-radius: 6px;
            }

            QLabel {
                color: #b0b0b0;
                font-weight: 500;
            }

            QLineEdit {
                background-color: #3d3d3d;
                color: #d4d4d4;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 6px 8px;
                selection-background-color: #264f78;
                min-height: 28px;
            }

            QLineEdit:focus {
                border: 1px solid #569cd6;
                outline: none;
            }

            QCheckBox {
                background-color: transparent;
                color: #d4d4d4;
                spacing: 6px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #4d4d4d;
                background-color: #3d3d3d;
            }

            QCheckBox::indicator:checked {
                background-color: #569cd6;
                border: 1px solid #569cd6;
            }

            QPushButton {
                background-color: #3d3d3d;
                color: #d4d4d4;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #4d4d4d;
                border-color: #569cd6;
            }

            QPushButton:pressed {
                background-color: #505050;
            }

            QPushButton:default {
                border: 2px solid #569cd6;
            }
        """)
        
        find_dialog.show()

    def process_finished(self, exit_code):
        self.append_output("\n" + "-" * 50 + "\n")
        if exit_code == 0:
            self.append_output(f"Process finished successfully (exit code: {exit_code})")
        else:
            self.append_output(f"Process failed (exit code: {exit_code})")
        
        try:
            if os.path.exists("temp_script.py"):
                os.remove("temp_script.py")
        except Exception as e:
            pass
    def append_output(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        clean_text = text.replace('</span>', '').replace('<span style="color:red">', '')
    
        cursor.insertText(clean_text)
        self.console.ensureCursorVisible()


        self.console.ensureCursorVisible()
    def open_file_from_tree(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            self.load_file(path)
            self.stacked_widget.setCurrentIndex(1)

    def undo(self):
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            current_editor.undo()

    def redo(self):
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            current_editor.redo()
