import io

from PySide6.QtWidgets import QWidget, QMainWindow, QApplication
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtCore import Qt, QTimer

from text_editor.core.buffer import TextBuffer

WINDOW_TITLE = "Text Editor"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class TextCursor:
    BLINKING_INTERVAL_MS = 500

    def __init__(
        self,
        row: int,
        col: int,
        font: QFont,
        parent: QWidget,
        paddx: int = 0,
        paddy: int = 0,
    ):
        self.row = row
        self.col = col
        font_metrics = QFontMetrics(font)
        self.char_width = font_metrics.horizontalAdvance("a")
        self.line_height = font_metrics.ascent()
        self.paddx = paddx
        self.paddy = paddy
        self.parent = parent

        # Blinking
        self.visible = True
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.toggle_visibility)
        self.start_blinking()

    def start_blinking(self):
        self.blink_timer.start(TextCursor.BLINKING_INTERVAL_MS)

    def toggle_visibility(self):
        self.visible = not self.visible
        self.start_blinking()
        self.parent.update()

    def get_coords(self) -> tuple[int, int, int, int]:
        """Returns cursor position as pixel coordinates (x1, y1, x2, y2)"""
        x = self.paddx + (self.col - 1) * self.char_width
        y = self.paddy - (self.row - 1) * self.line_height
        return x, y, x, y - self.line_height

    def get_position(self) -> tuple[int, int]:
        """Returns cursor position as (row, col)"""
        return self.row, self.col

    def move(self, row_delta: int, col_delta: int):
        """Moves cursor by (row_delta, col_delta)"""
        self.visible = True
        self.start_blinking()
        self.row += row_delta
        self.col += col_delta
        if self.row < 0:
            self.row = 1
        if self.col < 0:
            self.col = 1

    def draw(self, painter: QPainter):
        if not self.visible:
            return
        coords = self.get_coords()
        painter.drawLine(*coords)


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
        self.setFont(font)
        self.text_cursor = TextCursor(
            row=1, col=1, paddx=self.paddx, paddy=self.paddy, font=font, parent=self
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
            self.buffer.append(event.text())
            self.text_cursor.move(0, len(event.text()))
        elif event.key() == Qt.Key_Left:
            self.text_cursor.move(0, -1)
        elif event.key() == Qt.Key_Right:
            self.text_cursor.move(0, 1)

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
