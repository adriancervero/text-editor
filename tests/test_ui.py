import io

import pytest

from text_editor.ui.editor import (
    App,
    MainWindow,
    TextEditorWidget,
    TextCursor,
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class TestApp:
    def test_app_window_exists(self):
        app = App(show=False)
        assert hasattr(app, "window")
        assert isinstance(app.window, MainWindow)
        app.quit()


class TestMainWindow:
    def test_window_title(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert window.windowTitle() == WINDOW_TITLE

    def test_window_size(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert window.width() == WINDOW_WIDTH
        assert window.height() == WINDOW_HEIGHT

    def test_text_editor_widget_exists(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert hasattr(window, "editor")
        assert isinstance(window.editor, TextEditorWidget)


class TestTextEditorWidget:
    @pytest.mark.parametrize("initial_text", ["", "Hello, World!", "Line 1\nLine 2"])
    def test_initial_text(self, qtbot, initial_text):
        editor = TextEditorWidget(
            width=400, height=300, source=io.StringIO(initial_text)
        )
        qtbot.addWidget(editor)
        want = initial_text
        got = editor.buffer.get_text()
        assert got == want, f"got '{got}', want '{want}'"
        assert editor.width() == 400
        assert editor.height() == 300

    def test_append_text(self, qtbot):
        editor = TextEditorWidget(source=io.StringIO("My first editor!"))
        qtbot.addWidget(editor)
        want = editor.buffer.get_text() + " Hello"
        qtbot.keyClicks(editor, " Hello")
        got = editor.buffer.get_text()
        assert got == want, f"got '{got}', want '{want}'"

    def test_backspace_removal(self, qtbot):
        editor = TextEditorWidget(source=io.StringIO("My first editor!"))
        qtbot.addWidget(editor)
        initial_text = editor.buffer.get_text()
        want = initial_text[:-1]
        qtbot.keyPress(editor, Qt.Key_Backspace)
        got = editor.buffer.get_text()
        assert got == want, f"got '{got}', want '{want}'"

    def test_paint_event(self, qtbot):
        editor = TextEditorWidget(source=io.StringIO("Testing paint event"))
        qtbot.addWidget(editor)
        editor.repaint()
        assert True

    def test_cursor_exists(self, qtbot):
        editor = TextEditorWidget()
        qtbot.addWidget(editor)
        assert hasattr(editor, "text_cursor")
        assert isinstance(editor.text_cursor, TextCursor)

    def test_cursor_initial_position(self, qtbot):
        initial_text = "Testing cursor position"
        editor = TextEditorWidget(io.StringIO(initial_text))
        qtbot.addWidget(editor)
        cursor = editor.text_cursor
        assert cursor.row == 1
        assert cursor.col == 1


class TestTextCursor:
    @pytest.mark.parametrize(
        "row, col, paddx, paddy, expected_desc",
        [
            (1, 1, 50, 50, "cursor at origin (1,1)"),
            (2, 5, 50, 50, "cursor at middle position (2,5)"),
            (3, 10, 100, 80, "cursor with different padding (3,10)"),
        ],
    )
    def test_get_coords(self, row, col, paddx, paddy, expected_desc):
        font = QFont("Courier", 12)
        cursor = TextCursor(row=row, col=col, paddx=paddx, paddy=paddy, font=font)
        coords = cursor.get_coords()

        want_x = paddx + (col - 1) * cursor.char_width
        want_y = paddy - (row - 1) * cursor.line_height
        want = (want_x, want_y, want_x, want_y - cursor.line_height)

        assert coords == want, f"Failed for {expected_desc}: got {coords}, want {want}"

    @pytest.mark.parametrize(
        "row, col",
        [
            (1, 1),
            (5, 10),
        ],
    )
    def test_get_position(self, row, col):
        font = QFont("Courier", 12)
        cursor = TextCursor(row=row, col=col, font=font)
        got = cursor.get_position()
        want = (row, col)
        assert got == want, (
            f"Failed for cursor at ({row},{col}): got {got}, want {want}"
        )

    @pytest.mark.parametrize(
        "initial_row, initial_col, row_delta, col_delta, expected_row, expected_col, case",
        [
            (1, 1, 1, 1, 2, 2, "move down right"),
            (5, 5, -2, -3, 3, 2, "move up left"),
            (3, 3, -5, -5, 1, 1, "move to origin"),
            (10, 10, 0, 0, 10, 10, "no movement"),
        ],
    )
    def test_move(
        self,
        initial_row,
        initial_col,
        row_delta,
        col_delta,
        expected_row,
        expected_col,
        case,
    ):
        font = QFont("Courier", 12)
        cursor = TextCursor(row=initial_row, col=initial_col, font=font)
        cursor.move(row_delta, col_delta)
        got_row, got_col = cursor.get_position()
        assert (got_row, got_col) == (expected_row, expected_col), (
            f"Failed for case '{case}': got ({got_row},{got_col}), "
            f"want ({expected_row},{expected_col})"
        )
