import io

import pytest

from text_editor.ui.editor import (
    App,
    MainWindow,
    TextEditorWidget,
    TextCursor,
)
from PySide6.QtCore import Qt


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
        assert window.windowTitle() == MainWindow.WINDOW_TITLE

    def test_window_size(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert window.width() == MainWindow.WINDOW_WIDTH
        assert window.height() == MainWindow.WINDOW_HEIGHT

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

    def test_move_cursor_left_right(self, qtbot):
        initial_text = "Hello"
        editor = TextEditorWidget(io.StringIO(initial_text))
        qtbot.addWidget(editor)
        cursor = editor.text_cursor

        assert cursor.col == 1  # Initial cursor position
        assert cursor.row == 1

        cursor.move(0, 2)  # row+0, col+2: (1,1) -> (1,3)
        assert cursor.col == 3

        cursor.move(0, -1)  # row+0, col-1: (1,3) -> (1,2)
        assert cursor.col == 2

        cursor.move(0, -5)  # Move beyond start
        assert cursor.col == 1  # Should not go below 1

    def test_insert_text_at_cursor(self, qtbot):
        initial_text = "Helo"
        editor = TextEditorWidget(io.StringIO(initial_text))
        qtbot.addWidget(editor)
        cursor = editor.text_cursor

        assert cursor.col == 1  # Initial cursor position
        assert cursor.row == 1

        cursor.move(0, 2)  # row+0, col+2: (1,1) -> (1,3)

        assert cursor.col == 3

        qtbot.keyClicks(editor, "l")

        want = "Hello"
        got = editor.buffer.get_text()
        assert got == want, f"got '{got}', want '{want}'"
        assert cursor.col == 4  # Cursor should move after inserted character
