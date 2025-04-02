import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QApplication
from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from components.python_highlighter import PythonHighlighter

class CodeEditor(QsciScintilla):
    def __init__(self, parent=None, language="Python"):
        super().__init__(parent)
        self.file_path = None
        self.language = language
        self.setup_editor()

    def setup_editor(self):

        self.setUtf8(True)

        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)

        self.setAutoIndent(True)
        self.setIndentationWidth(4)
        self.setBackspaceUnindents(True)
        self.setTabIndents(True)

        self.setEolMode(QsciScintilla.EolMode.EolUnix)

        self.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        self.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagByBorder)
        self.setWrapIndentMode(QsciScintilla.WrapIndentMode.WrapIndentIndented)

        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#3A3D41"))
        self.setMatchedBraceForegroundColor(QColor("#FF8000"))
        self.setUnmatchedBraceForegroundColor(QColor("#FF0000"))
        
        self.setIndentationGuidesBackgroundColor(QColor("#D8DEE9"))
        self.setIndentationGuidesForegroundColor(QColor("#3A3D41"))

        self.setMarginsForegroundColor(QColor("#2D2D30"))
        self.setMarginsBackgroundColor(QColor("#252526"))
        self.setMarginSensitivity(0, True)
        self.marginClicked.connect(self._margin_clicked)

        self.setMarginType(1, QsciScintilla.MarginType.SymbolMargin)
        self.setMarginWidth(1, 15)
        self.setMarginSensitivity(1, True)
        self.setMarginMarkerMask(1, 0b1111111)
        self.markerDefine(QsciScintilla.MarkerSymbol.Circle, 0)
        self.setMarkerBackgroundColor(QColor("#D8DEE9"), 0)
        self.markerDefine(QsciScintilla.MarkerSymbol.RightTriangle, 1)
        self.setMarkerBackgroundColor(QColor("#FF5555"), 1)

        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle, 2)
        self.setMarginWidth(2, 15)
        self.setFoldMarginColors(QColor("#252526"), QColor("#252526"))
        self.setProperty('fold.compact', '0') 

        font = QFont("Consolas", 12)
        font.setFixedPitch(True)
        font.setStyleHint(QFont.StyleHint.TypeWriter)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        self.setFont(font)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, QsciScintilla.STYLE_DEFAULT, b"Consolas")
        self.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, QsciScintilla.STYLE_DEFAULT, 12)

        self.setCallTipsStyle(QsciScintilla.CallTipsStyle.CallTipsNoContext)
        self.setCallTipsVisible(0)
        self.setCallTipsPosition(QsciScintilla.CallTipsPosition.CallTipsBelowText)
        self.setCallTipsBackgroundColor(QColor("#2D2D30"))
        self.setCallTipsForegroundColor(QColor("#D4D4D4"))
        self.setCallTipsHighlightColor(QColor("#007ACC"))

        self.setCaretForegroundColor(QColor("#FFFFFF"))
        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, QsciScintilla.CARETSTYLE_BLOCK)
        self.SendScintilla(QsciScintilla.SCI_SETCARETWIDTH, 2)
        self.SendScintilla(QsciScintilla.SCI_SETADDITIONALCARETSBLINK, 1)
        self.SendScintilla(QsciScintilla.SCI_SETADDITIONALCARETSVISIBLE, 1)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#2D2D30"))
        self.setCaretLineFrameWidth(2)

        self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, 1)
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, 1)

        self.setSelectionBackgroundColor(QColor("#3A3D41"))
        self.setSelectionForegroundColor(QColor("#F0E6D2"))
        self.SendScintilla(QsciScintilla.SCI_SETVIRTUALSPACEOPTIONS, QsciScintilla.SCVS_RECTANGULARSELECTION)

        self.setEdgeMode(QsciScintilla.EdgeMode.EdgeLine)
        self.setEdgeColumn(100)
        self.setEdgeColor(QColor("#404040"))
        self.SendScintilla(QsciScintilla.SCI_SETEDGECOLUMN, 80, 1)
        self.setWhitespaceVisibility(QsciScintilla.WhitespaceVisibility.WsInvisible)
        self.setWhitespaceForegroundColor(QColor("#3A3D41"))
        self.setWhitespaceBackgroundColor(QColor("#1E1E1E"))
        self.setWhitespaceSize(1)
        
        self.SendScintilla(QsciScintilla.SCI_SETLINESTATE, 0, 1)
        self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)
        self.SendScintilla(QsciScintilla.SCI_SETENDATLASTLINE, 1)
        self.SendScintilla(QsciScintilla.SCI_SETMOUSEWHEELCAPTURES, 1)

        self.setHotspotUnderline(True)
        self.setHotspotForegroundColor(QColor("#80BFFF"))
        self.setHotspotBackgroundColor(QColor("#1E1E1E"))
        self.setHotspotWrap(True)

        self.setPaper(QColor("#1E1E1E"))
        self.setColor(QColor("#F0E6D2"))

        self.setIndicatorForegroundColor(QColor("#3A3D41"), 0)
        self.setIndicatorOutlineColor(QColor("#3A3D41"), 0)
        self.setIndicatorDrawUnder(True, 0)

        # Add highlight for occurrences of selected text
        self.SendScintilla(QsciScintilla.SCI_INDICSETSTYLE, 1, QsciScintilla.INDIC_ROUNDBOX)

        self.SendScintilla(QsciScintilla.SCI_INDICSETALPHA, 1, 100)
        self.SendScintilla(QsciScintilla.SCI_INDICSETOUTLINEALPHA, 1, 200)

        # Add keyboard shortcuts or command bindings
        self.SendScintilla(QsciScintilla.SCI_ASSIGNCMDKEY, 
                        ord('D') + (QsciScintilla.SCMOD_CTRL << 16), 
                        QsciScintilla.SCI_SELECTIONDUPLICATE)  # Ctrl+D to duplicate selection

        self.setAutoCompletionFillups(b"(")

        self.setEolVisibility(False)  # Don't show EOL by default

        self.SendScintilla(QsciScintilla.SCI_ANNOTATIONSETSTYLE, 0, 10)
        self.SendScintilla(QsciScintilla.SCI_ANNOTATIONSETVISIBLE, QsciScintilla.ANNOTATION_BOXED)
        

        self.SendScintilla(QsciScintilla.SCI_SETRECTANGULARSELECTIONMODIFIER, 
                        QsciScintilla.SCMOD_ALT)

        self.installEventFilter(self)
        self.SendScintilla(QsciScintilla.SCI_SETCARETPERIOD)
        self.highlighter = PythonHighlighter(self)

    def set_language(self, language):
        self.language = language
        
        self.highlighter = PythonHighlighter(self)
        
        self.setMatchedBraceBackgroundColor(QColor("#3A3D41"))
        self.setMatchedBraceForegroundColor(QColor("#FF8000")) 
        self.setUnmatchedBraceForegroundColor(QColor("#FF0000")) 
        
        self.setIndentationGuidesBackgroundColor(QColor("#2D2D30"))
        self.setIndentationGuidesForegroundColor(QColor("#3A3D41"))

        self.setMarginsForegroundColor(QColor("#2D2D30"))
        self.setMarginsBackgroundColor(QColor("#252526"))
        
        self.setMarkerBackgroundColor(QColor("#FF5555"), 0)
        self.setMarkerBackgroundColor(QColor("#5555FF"), 1)
        
        self.setFoldMarginColors(QColor("#252526"), QColor("#252526"))  # Fold margin colors
        
        self.setCallTipsBackgroundColor(QColor("#2D2D30"))
        self.setCallTipsForegroundColor(QColor("#D4D4D4"))
        self.setCallTipsHighlightColor(QColor("#007ACC"))

        self.setCaretForegroundColor(QColor("#FFFFFF"))
        self.setCaretLineBackgroundColor(QColor("#2D2D30"))

        self.setSelectionBackgroundColor(QColor("#3A3D41"))
        self.setSelectionForegroundColor(QColor("#F0E6D2"))
        
        
        self.setEdgeColor(QColor("#F0E6D2"))
        
        self.setWhitespaceForegroundColor(QColor("#3A3D41"))
        self.setWhitespaceBackgroundColor(QColor("#1E1E1E"))

        self.setHotspotForegroundColor(QColor("#80BFFF")) 
        self.setHotspotBackgroundColor(QColor("#1E1E1E"))
        self.SendScintilla(QsciScintilla.SCI_SETINDENTATIONGUIDES)
        self.setPaper(QColor("#1E1E1E"))
        self.setColor(QColor("#F0E6D2")) 

        self.setIndicatorForegroundColor(QColor("#3A3D41"), 0)
        self.setIndicatorOutlineColor(QColor("#3A3D41"), 0)
        self.setEdgeColor(QColor("#404040"))


    def _margin_clicked(self, margin, line, modifiers):
        if margin == 1:
            if self.markersAtLine(line) & (1 << 0):
                self.markerDelete(line, 0)
            else:
                self.markerAdd(line, 0)
    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress and obj is self:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                
                line, index = self.getCursorPosition()
                current_line_text = self.text(line).rstrip()

                # Let the Enter key create a new line
                super().keyPressEvent(event)

                # Apply auto-indentation
                self.autoIndent(line, current_line_text)
                return True

            elif event.key() == Qt.Key.Key_BraceRight:
                line, index = self.getCursorPosition()
                current_line_text = self.text(line)
                print(line)
                text_before_cursor = current_line_text[:index]
                if text_before_cursor.strip() == "":
                    self.SendScintilla(QsciScintilla.SCI_DELETEBACK)

                    

        return super().eventFilter(obj, event)

    def autoIndent(self, prev_line, current_line_text):
        new_line = prev_line + 1

        prev_indent = self.indentation(prev_line)

        if current_line_text.strip().endswith(":") or current_line_text.strip().endswith("{"):
            total_indent = prev_indent + 4
        else:
            total_indent = prev_indent

        self.setIndentation(new_line, total_indent)
        self.setCursorPosition(new_line, total_indent)

    

