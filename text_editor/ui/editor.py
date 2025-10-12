import io

from PySide6.QtWidgets import QWidget, QMainWindow, QApplication
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtCore import Qt

from text_editor.core.buffer import TextBuffer
from text_editor.ui.cursor import TextCursor


""" Each line a commit:
TODO: - Multiline
TODO: - Text selection

"""


class TextEditorWidget(QWidget):
    def __init__(
        self, source: io.IOBase = None, width: int = 400, height: int = 300, parent=None
    ):
        super().__init__(parent)
        self.resize(width, height)
        self.setFocusPolicy(Qt.StrongFocus)

        self.buffer = TextBuffer(source)

        self.paddx = 50
        self.paddy = 50
        font = QFont("Courier", 12)
        font_metrics = QFontMetrics(font)
        char_width = font_metrics.horizontalAdvance("M")
        line_height = font_metrics.lineSpacing()
        self.setFont(font)
        self.text_cursor = TextCursor(
            row=1,
            col=1,
            paddx=self.paddx,
            paddy=self.paddy,
            char_width=char_width,
            line_height=line_height,
            parent=self,
        )

    def paintEvent(self, event):
        painter = QPainter(self)

        # Background
        painter.fillRect(event.rect(), QColor("black"))

        # Text
        painter.setPen(QColor("white"))
        painter.drawText(self.paddx, self.paddy, self.buffer.get_text())

        # Cursor
        self.text_cursor.draw(painter)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.buffer.backspace()
            self.text_cursor.move(0, -1)
        elif event.text():
            index = self.text_cursor.col - 1
            self.buffer.insert(index, event.text())
            self.text_cursor.move(0, len(event.text()))
        elif event.key() == Qt.Key_Left:
            self.text_cursor.move(0, -1)
        elif event.key() == Qt.Key_Right:
            self.text_cursor.move(0, 1)

        self.update()


class MainWindow(QMainWindow):
    WINDOW_TITLE = "Text Editor"
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    def __init__(self, source: io.IOBase = None):
        super().__init__()
        self.setWindowTitle(MainWindow.WINDOW_TITLE)
        self.resize(MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT)
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
