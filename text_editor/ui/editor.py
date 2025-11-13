import io

from PySide6.QtWidgets import QWidget, QMainWindow, QApplication
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtCore import Qt

from text_editor.core.buffer import TextBuffer
from text_editor.ui.cursor import TextCursor


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
        self.line_height = font_metrics.lineSpacing()
        self.setFont(font)
        self.text_cursor = TextCursor(
            row=1,
            col=1,
            paddx=self.paddx,
            paddy=self.paddy,
            char_width=char_width,
            line_height=self.line_height,
            parent=self,
        )

    def paintEvent(self, event):
        painter = QPainter(self)

        # Background
        painter.fillRect(event.rect(), QColor("black"))

        # Text
        painter.setPen(QColor("white"))
        lines = self.buffer.get_text().split("\n")
        for i, line in enumerate(lines):
            y = self.paddy + i * self.line_height
            painter.drawText(self.paddx, y, line)

        # Cursor
        self.text_cursor.draw(painter)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.buffer.backspace()
            self.text_cursor.move(0, -1)
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            index = self.get_cursor_index()
            self.buffer.insert(index, "\n")
            self.text_cursor.move(1, -self.text_cursor.col + 1)
        elif event.text():
            index = self.get_cursor_index()
            self.buffer.insert(index, event.text())
            self.text_cursor.move(0, len(event.text()))
        elif event.key() == Qt.Key_Left:
            self.text_cursor.move(0, -1)
        elif event.key() == Qt.Key_Right:
            self.text_cursor.move(0, 1)

        self.update()

    def get_cursor_index(self) -> int:
        lines = self.buffer.get_text().split("\n")
        index = sum(len(line) + 1 for line in lines[: self.text_cursor.row - 1])
        index += self.text_cursor.col - 1
        return index


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
