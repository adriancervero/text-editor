import io

import pytest

from text_editor.ui.editor import (
    App,
    MainWindow,
    TextEditorWidget,
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
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
        editor = TextEditorWidget(source=io.StringIO(initial_text))
        qtbot.addWidget(editor)
        want = initial_text
        got = editor.buffer.get_text()
        assert got == want, f"got '{got}', want '{want}'"

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
