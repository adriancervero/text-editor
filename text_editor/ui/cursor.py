from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget


class TextCursor:
    BLINKING_INTERVAL_MS = 500

    def __init__(
        self,
        row: int,
        col: int,
        char_width: int,
        line_height: int,
        parent: QWidget,
        paddx: int = 0,
        paddy: int = 0,
        blinking: bool = True,
    ):
        self.row = row
        self.col = col
        self.char_width = char_width
        self.line_height = line_height
        self.paddx = paddx
        self.paddy = paddy
        self.parent = parent
        self.blinking = blinking

        # Blinking
        self.visible = True
        if blinking:
            self.blink_timer = QTimer()
            self.blink_timer.timeout.connect(self.toggle_visibility)
            self.start_blinking()

    def start_blinking(self):
        if self.blinking:
            self.blink_timer.start(TextCursor.BLINKING_INTERVAL_MS)

    def toggle_visibility(self):
        self.visible = not self.visible
        self.start_blinking()
        self.parent.update()

    def get_coords(self) -> tuple[int, int, int, int]:
        """Returns cursor position as pixel coordinates (x1, y1, x2, y2)"""
        x = self.paddx + (self.col - 1) * self.char_width
        y = self.paddy + (self.row - 1) * self.line_height
        return x, y, x, y - self.line_height

    def get_position(self) -> tuple[int, int]:
        """Returns cursor position as (row, col)"""
        return self.row, self.col

    def get_index(self) -> int:
        """Returns cursor index base on (row, col)"""
        index = 0
        for r in range(1, self.row):
            index += len(self.parent.buffer.get_line(r)) + 1  # +1 for newline
        index += self.col - 1
        return index

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
