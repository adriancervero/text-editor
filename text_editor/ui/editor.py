import io

from PySide6.QtWidgets import QWidget, QMainWindow, QApplication
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

from text_editor.core.buffer import TextBuffer

WINDOW_TITLE = "Text Editor"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class TextEditorWidget(QWidget):
    def __init__(self, source: io.IOBase = None):
        super().__init__()
        self.buffer = TextBuffer(source)
        self.setFocusPolicy(Qt.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor("white"))
        painter.drawText(10, 50, self.buffer.get_text())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.buffer.backspace()
        elif event.text():
            self.buffer.append(event.text())
        self.update()


class MainWindow(QMainWindow):
    def __init__(self, source: io.IOBase = None):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.editor = TextEditorWidget(source=source)
        self.setCentralWidget(self.editor)


class App(QApplication):
    def __init__(self, source: io.IOBase = None, show: bool = True):
        super().__init__()
        self.window = MainWindow(source=source)

        if show:
            self.window.show()

    def run(self):
        self.exec()
