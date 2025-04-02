from PyQt6.QtGui import QFont, QColor
from PyQt6.Qsci import QsciScintilla, QsciAPIs, QsciLexerHTML, QsciLexerCSS, QsciLexerRuby, QsciLexerPython, QsciLexerCPP, QsciLexerJava, QsciLexerJavaScript

class PythonHighlighter:
    def __init__(self, editor, language="Python"):
        self.editor = editor
        self.language = language

        current_font = QFont("Consolas", 12)
        current_font.setFixedPitch(True)

        self.palette = {
            "paper": QColor("#2E2E2E"),      
            "default": QColor("#CBCBCB"),    
            "identifier": QColor("#D8DEE9"), 
            "comment": QColor("#778899"),    
            "keyword": QColor("#8FA3BF"),    
            "string": QColor("#A3BE8C"),     
            "number": QColor("#B48EAD"),     
            "class_func": QColor("#D8DEE9"), 
                                            
            "operator": QColor("#778899"),   
            "tag_attr_selector": QColor("#8FA3BF"),
            "property_misc": QColor("#D8DEE9"),
            "value": QColor("#A3BE8C"),

        }

        if self.language == "Python":
            self.lexer = QsciLexerPython()
        elif self.language in ("C++", "C"):
            self.lexer = QsciLexerCPP()
        elif self.language == "Java":
            self.lexer = QsciLexerJava()
        elif self.language == "JavaScript":
            self.lexer = QsciLexerJavaScript()
        elif self.language == "HTML":
            self.lexer = QsciLexerHTML()
        elif self.language == "CSS":
            self.lexer = QsciLexerCSS()
        elif self.language == "Ruby":
            self.lexer = QsciLexerRuby()
        elif self.language == "PHP":
            self.lexer = QsciLexerHTML() 
        else: 
            self.lexer = None


        
        if self.lexer:
            
            self.editor.setLexer(self.lexer)
            self.lexer.setFont(current_font)
            self.lexer.setDefaultFont(current_font)

            self._apply_soft_dark_theme_to_lexer()
            self._setup_apis_for_language(self.language)
        else:
            self.editor.setFont(current_font)

            self.editor.setPaper(self.palette["paper"])
            self.editor.setColor(self.palette["default"])

    # Renamed method to reflect the dark theme
    def _apply_soft_dark_theme_to_lexer(self):
        if not self.lexer:
            return
        
        p = self.palette

        self.lexer.setPaper(p["paper"])
        
        self.lexer.setColor(p["default"])

        if isinstance(self.lexer, QsciLexerPython):
            self.lexer.setColor(p["default"], QsciLexerPython.Default)
            self.lexer.setColor(p["identifier"], QsciLexerPython.Identifier)
            self.lexer.setColor(p["string"], QsciLexerPython.SingleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerPython.DoubleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerPython.TripleSingleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerPython.TripleDoubleQuotedString)
            self.lexer.setColor(p["comment"], QsciLexerPython.Comment)
            self.lexer.setColor(p["comment"], QsciLexerPython.CommentBlock)
            self.lexer.setColor(p["keyword"], QsciLexerPython.Keyword)
            self.lexer.setColor(p["class_func"], QsciLexerPython.ClassName)
            self.lexer.setColor(p["class_func"], QsciLexerPython.FunctionMethodName)
            self.lexer.setColor(p["number"], QsciLexerPython.Number)
            self.lexer.setColor(p["operator"], QsciLexerPython.Operator)
            self.lexer.setColor(p["property_misc"], QsciLexerPython.Decorator) # Using property_misc color

        elif isinstance(self.lexer, QsciLexerCPP):
            self.lexer.setColor(p["default"], QsciLexerCPP.Default)
            self.lexer.setColor(p["identifier"], QsciLexerCPP.Identifier)
            self.lexer.setColor(p["string"], QsciLexerCPP.SingleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerCPP.DoubleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerCPP.RawString)
            self.lexer.setColor(p["comment"], QsciLexerCPP.Comment)
            self.lexer.setColor(p["comment"], QsciLexerCPP.CommentLine)
            self.lexer.setColor(p["comment"], QsciLexerCPP.CommentDoc)
            self.lexer.setColor(p["keyword"], QsciLexerCPP.Keyword)
            self.lexer.setColor(p["keyword"], QsciLexerCPP.KeywordSet2)
            self.lexer.setColor(p["number"], QsciLexerCPP.Number)
            self.lexer.setColor(p["operator"], QsciLexerCPP.Operator)
            self.lexer.setColor(p["comment"], QsciLexerCPP.PreProcessor) # Using comment color for preprocessor

        elif isinstance(self.lexer, QsciLexerJava):
            self.lexer.setColor(p["default"], QsciLexerJava.Default)
            self.lexer.setColor(p["identifier"], QsciLexerJava.Identifier)
            self.lexer.setColor(p["string"], QsciLexerJava.SingleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerJava.DoubleQuotedString)
            self.lexer.setColor(p["comment"], QsciLexerJava.Comment)
            self.lexer.setColor(p["comment"], QsciLexerJava.CommentLine)
            self.lexer.setColor(p["comment"], QsciLexerJava.CommentDoc)
            self.lexer.setColor(p["keyword"], QsciLexerJava.Keyword)
            self.lexer.setColor(p["class_func"], QsciLexerJava.ClassName) # May need bold font
            self.lexer.setColor(p["class_func"], QsciLexerJava.FunctionMethodName) # May need bold font
            self.lexer.setColor(p["number"], QsciLexerJava.Number)
            self.lexer.setColor(p["operator"], QsciLexerJava.Operator)
            self.lexer.setColor(p["property_misc"], QsciLexerJava.Annotation) # Using property_misc

        elif isinstance(self.lexer, QsciLexerJavaScript):
            self.lexer.setColor(p["default"], QsciLexerJavaScript.Default)
            self.lexer.setColor(p["identifier"], QsciLexerJavaScript.Identifier)
            self.lexer.setColor(p["string"], QsciLexerJavaScript.SingleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerJavaScript.DoubleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerJavaScript.TemplateString)
            self.lexer.setColor(p["comment"], QsciLexerJavaScript.Comment)
            self.lexer.setColor(p["comment"], QsciLexerJavaScript.CommentLine)
            self.lexer.setColor(p["comment"], QsciLexerJavaScript.CommentDoc)
            self.lexer.setColor(p["keyword"], QsciLexerJavaScript.Keyword)
            self.lexer.setColor(p["number"], QsciLexerJavaScript.Number)
            self.lexer.setColor(p["operator"], QsciLexerJavaScript.Operator)
            self.lexer.setColor(p["value"], QsciLexerJavaScript.Regex) # Using value color

        elif isinstance(self.lexer, QsciLexerHTML):
            self.lexer.setColor(p["default"], QsciLexerHTML.Default)
            self.lexer.setColor(p["tag_attr_selector"], QsciLexerHTML.Tag)
            self.lexer.setColor(p["tag_attr_selector"], QsciLexerHTML.UnknownTag)
            self.lexer.setColor(p["property_misc"], QsciLexerHTML.Attribute)
            self.lexer.setColor(p["property_misc"], QsciLexerHTML.UnknownAttribute)
            self.lexer.setColor(p["value"], QsciLexerHTML.HTMLDoubleQuotedString)
            self.lexer.setColor(p["value"], QsciLexerHTML.HTMLSingleQuotedString)
            self.lexer.setColor(p["comment"], QsciLexerHTML.HTMLComment)
            self.lexer.setColor(p["default"], QsciLexerHTML.OtherInTag)
            self.lexer.setColor(p["operator"], QsciLexerHTML.Entity)

            def apply_sublexer_theme(sublexer_instance, base_style_map):
                sublexer_instance.setPaper(p["paper"]) # Set dark background
                sublexer_instance.setColor(p["default"]) # Set light default color
                for style_const, color_key in base_style_map.items():
                     if color_key in p:
                         sublexer_instance.setColor(p[color_key], style_const)
                     else:
                         sublexer_instance.setColor(p["default"], style_const) # Fallback
                sublexer_instance.setFont(self.lexer.font(sublexer_instance.defaultStyle()))
                sublexer_instance.setDefaultFont(self.lexer.font(sublexer_instance.defaultStyle()))

            js_lexer = QsciLexerJavaScript()
            js_map = {
                QsciLexerJavaScript.Default: "default", QsciLexerJavaScript.Identifier: "identifier",
                QsciLexerJavaScript.SingleQuotedString: "string", QsciLexerJavaScript.DoubleQuotedString: "string",
                QsciLexerJavaScript.TemplateString: "string", QsciLexerJavaScript.Comment: "comment",
                QsciLexerJavaScript.CommentLine: "comment", QsciLexerJavaScript.CommentDoc: "comment",
                QsciLexerJavaScript.Keyword: "keyword", QsciLexerJavaScript.Number: "number",
                QsciLexerJavaScript.Operator: "operator", QsciLexerJavaScript.Regex: "value",
            }
            apply_sublexer_theme(js_lexer, js_map)
            self.lexer.setSubLexer(js_lexer, QsciLexerHTML.Script)
            
            css_lexer = QsciLexerCSS()
            css_map = {
                 QsciLexerCSS.Default: "default", QsciLexerCSS.Selector: "tag_attr_selector",
                 QsciLexerCSS.Property: "property_misc", QsciLexerCSS.Value: "value",
                 QsciLexerCSS.Comment: "comment", QsciLexerCSS.IdSelector: "tag_attr_selector",
                 QsciLexerCSS.ClassSelector: "tag_attr_selector", QsciLexerCSS.PseudoClass: "tag_attr_selector",
                 QsciLexerCSS.Attribute: "property_misc", QsciLexerCSS.Number: "number",
                 QsciLexerCSS.Operator: "operator", QsciLexerCSS.Important: "keyword",
                 QsciLexerCSS.SingleQuotedString: "string", QsciLexerCSS.DoubleQuotedString: "string",
            }
            apply_sublexer_theme(css_lexer, css_map)
            self.lexer.setSubLexer(css_lexer, QsciLexerHTML.Style)


        elif isinstance(self.lexer, QsciLexerCSS):
            self.lexer.setColor(p["default"], QsciLexerCSS.Default)
            self.lexer.setColor(p["tag_attr_selector"], QsciLexerCSS.Selector)
            self.lexer.setColor(p["tag_attr_selector"], QsciLexerCSS.IdSelector)
            self.lexer.setColor(p["tag_attr_selector"], QsciLexerCSS.ClassSelector)
            self.lexer.setColor(p["tag_attr_selector"], QsciLexerCSS.PseudoClass)
            self.lexer.setColor(p["property_misc"], QsciLexerCSS.Property)
            self.lexer.setColor(p["value"], QsciLexerCSS.Value)
            self.lexer.setColor(p["comment"], QsciLexerCSS.Comment)
            self.lexer.setColor(p["property_misc"], QsciLexerCSS.Attribute)
            self.lexer.setColor(p["number"], QsciLexerCSS.Number)
            self.lexer.setColor(p["operator"], QsciLexerCSS.Operator)
            self.lexer.setColor(p["keyword"], QsciLexerCSS.Important) # Use keyword color
            self.lexer.setColor(p["string"], QsciLexerCSS.SingleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerCSS.DoubleQuotedString)

        elif isinstance(self.lexer, QsciLexerRuby):
            self.lexer.setColor(p["default"], QsciLexerRuby.Default)
            self.lexer.setColor(p["identifier"], QsciLexerRuby.Identifier)
            self.lexer.setColor(p["string"], QsciLexerRuby.DoubleQuotedString)
            self.lexer.setColor(p["string"], QsciLexerRuby.SingleQuotedString)
            self.lexer.setColor(p["comment"], QsciLexerRuby.Comment)
            self.lexer.setColor(p["keyword"], QsciLexerRuby.Keyword)
            self.lexer.setColor(p["class_func"], QsciLexerRuby.ClassName) # May need bold
            self.lexer.setColor(p["class_func"], QsciLexerRuby.FunctionMethodName) # May need bold
            self.lexer.setColor(p["number"], QsciLexerRuby.Number)
            self.lexer.setColor(p["operator"], QsciLexerRuby.Operator)
            self.lexer.setColor(p["value"], QsciLexerRuby.Regex) # Using value color
            self.lexer.setColor(p["property_misc"], QsciLexerRuby.Symbol) # Using property_misc


    def _setup_apis_for_language(self, language):
        
        if not self.lexer:
            return

        self.api = QsciAPIs(self.lexer)

        keywords = []
        if language == "Python":
            keywords = [
                "and", "as", "assert", "async", "await", "break", "class", "continue", "def",
                "del", "elif", "else", "except", "False", "finally", "for",
                "from", "global", "if", "import", "in", "is", "lambda", "None",
                "nonlocal", "not", "or", "pass", "raise", "return", "True",
                "try", "while", "with", "yield"
            ]
        elif language in ["C++", "C"]:
            keywords = [
                "auto", "break", "case", "char", "const", "continue", "default",
                "do", "double", "else", "enum", "extern", "float", "for", "goto",
                "if", "int", "long", "register", "return", "short", "signed",
                "sizeof", "static", "struct", "switch", "typedef", "union",
                "unsigned", "void", "volatile", "while"
            ]
            if language == "C++":
                cpp_keywords = [
                    "alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel",
                    "atomic_commit", "atomic_noexcept", "bitand", "bitor", "bool",
                    "catch", "char8_t", "char16_t", "char32_t", "class", "compl",
                    "concept", "consteval", "constexpr", "constinit", "const_cast",
                    "co_await", "co_return", "co_yield", "decltype", "delete",
                    "dynamic_cast", "explicit", "export", "false", "friend", "inline",
                    "mutable", "namespace", "new", "noexcept", "not", "not_eq",
                    "nullptr", "operator", "or", "or_eq", "private", "protected",
                    "public", "reflexpr", "reinterpret_cast", "requires", "static_assert",
                    "static_cast", "synchronized", "template", "this", "thread_local",
                    "throw", "true", "try", "typeid", "typename", "using", "virtual",
                    "wchar_t", "xor", "xor_eq"
                ]
                keywords.extend(cpp_keywords)
        elif language == "Java":
            keywords = [
                "abstract", "assert", "boolean", "break", "byte", "case", "catch",
                "char", "class", "const", "continue", "default", "do", "double",
                "else", "enum", "exports", "extends", "final", "finally", "float", "for",
                "goto", "if", "implements", "import", "instanceof", "int",
                "interface", "long", "module", "native", "new", "non-sealed", "open",
                "opens", "package", "permits", "private", "protected", "provides",
                "public", "record", "requires", "return", "sealed", "short", "static",
                "strictfp", "super", "switch", "synchronized", "this", "throw", "throws",
                "to", "transient", "transitive", "try", "uses", "var", "void",
                "volatile", "while", "yield"
            ]
        elif language == "JavaScript":
             keywords = [
                'abstract', 'arguments', 'await', 'boolean', 'break', 'byte', 'case',
                'catch', 'char', 'class', 'const', 'continue', 'debugger', 'default',
                'delete', 'do', 'double', 'else', 'enum', 'eval', 'export', 'extends',
                'false', 'final', 'finally', 'float', 'for', 'function', 'goto', 'if',
                'implements', 'import', 'in', 'instanceof', 'int', 'interface', 'let',
                'long', 'native', 'new', 'null', 'package', 'private', 'protected',
                'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized',
                'this', 'throw', 'throws', 'transient', 'true', 'try', 'typeof', 'var',
                'void', 'volatile', 'while', 'with', 'yield'
            ]
        elif language == "HTML":
            keywords = [ ] 
        elif language == "CSS":
             keywords = [ 
                "align-content", "align-items", "align-self", "all", "animation",
                "backdrop-filter", "backface-visibility", "background", "background-attachment",
                "background-blend-mode", "background-clip", "background-color", "background-image",
                "background-origin", "background-position", "background-repeat", "background-size",
                "border", "border-bottom", "border-bottom-color", "border-bottom-left-radius",
                "color", "display", "flex", "font", "grid", "height", "justify-content",
                "left", "margin", "opacity", "padding", "position", "right", "text-align",
                "top", "transform", "transition", "width", "z-index"
            ]
        elif language == "Ruby":
            keywords = [
                "BEGIN", "END", "alias", "and", "begin", "break", "case", "class", "def",
                "defined?", "do", "else", "elsif", "end", "ensure", "false",
                "for", "if", "in", "module", "next", "nil", "not", "or",
                "redo", "rescue", "retry", "return", "self", "super", "then",
                "true", "undef", "unless", "until", "when", "while", "yield"
            ]


        for keyword in keywords:
            self.api.add(keyword)

        self.api.prepare()

        self.editor.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.editor.setAutoCompletionCaseSensitivity(False)
        self.editor.setAutoCompletionThreshold(2)
        self.editor.setAutoCompletionUseSingle(QsciScintilla.AutoCompletionUseSingle.AcusNever)