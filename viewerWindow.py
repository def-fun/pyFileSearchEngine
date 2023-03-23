"""参考于Qt官网：https://doc.qt.io/qtforpython/examples/example_widgets_richtext_syntaxhighlighter.html"""
import re
import codecs
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QColor, QFont, QFontDatabase, QKeySequence,
                           QSyntaxHighlighter, QTextCharFormat)
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPlainTextEdit, QMessageBox


class ViewerWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.resize(640, 512)

        self._editor = QPlainTextEdit()
        self._highlighter = Highlighter()

        self.setup_file_menu()
        self.setup_editor()

        self.setCentralWidget(self._editor)
        self.setWindowTitle("文本查看器")

    def new_file(self):
        self._editor.clear()

    def open_file(self, path=""):
        file_name = path

        if not file_name:
            file_name, _ = QFileDialog.getOpenFileName(self, "选择文件")

        if file_name:
            if self.is_binary_file(file_name):
                QMessageBox.warning(self, "警告", "无法打开二进制文件！")
                return
            with open(file_name, "r", encoding="utf8") as f:
                self._editor.setPlainText(f.read())

    def setup_editor(self):
        class_format = QTextCharFormat()
        class_format.setFontWeight(QFont.Bold)
        class_format.setForeground(Qt.blue)
        pattern = r"^\s*class\s+\w+\(.*$"
        self._highlighter.add_mapping(pattern, class_format)

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(Qt.blue)
        pattern = r"^\s*def\s+\w+\s*\(.*\)\s*:\s*$"
        self._highlighter.add_mapping(pattern, function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#a6a6a6"))
        self._highlighter.add_mapping(r"^\s*#.*$", comment_format)
        self._highlighter.add_mapping(r"^\s*//.*$", comment_format)

        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self._editor.setFont(font)
        self._highlighter.setDocument(self._editor.document())

    def setup_file_menu(self):
        """设置菜单"""
        file_menu = self.menuBar().addMenu("&文件")

        open_file_act = file_menu.addAction("&打开")
        open_file_act.setShortcut(QKeySequence(QKeySequence.Open))
        open_file_act.triggered.connect(self.open_file)

        quit_act = file_menu.addAction("&退出")
        quit_act.setShortcut(QKeySequence(QKeySequence.Quit))
        quit_act.triggered.connect(self.close)

    @staticmethod
    def is_binary_file(file_path):
        """判断文件是不是二进制文件"""
        _TEXT_BOMS = (
            codecs.BOM_UTF16_BE,
            codecs.BOM_UTF16_LE,
            codecs.BOM_UTF32_BE,
            codecs.BOM_UTF32_LE,
            codecs.BOM_UTF8,
        )

        with open(file_path, 'rb') as file:
            initial_bytes = file.read(8192)
            file.close()
            for bom in _TEXT_BOMS:
                if initial_bytes.startswith(bom):
                    continue
                else:
                    if b'\0' in initial_bytes:
                        return True
        return False


class Highlighter(QSyntaxHighlighter):
    """语法高亮显示"""

    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)

        self._mappings = {}

    def add_mapping(self, pattern, format):
        self._mappings[pattern] = format

    def highlightBlock(self, text):
        for pattern, format in self._mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format)


if __name__ == '__main__':
    app = QApplication([])
    window = ViewerWindow()
    window.resize(640, 512)
    window.show()
    app.exec()
