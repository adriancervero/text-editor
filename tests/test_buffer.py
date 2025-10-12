import pytest
import io
from text_editor.core.buffer import TextBuffer


class TestTextBuffer:
    def test_append_characters(self):
        tbuffer = TextBuffer()
        tbuffer.append("Hello")

        got = tbuffer.get_text()
        want = "Hello"
        assert got == want, f"got {got}, want {want}"

    @pytest.mark.parametrize(
        "case,initial,expected",
        [
            ("normal", "Hello", "Hell"),
            ("remove last char", "A", ""),
            ("empty text", "", ""),
        ],
    )
    def test_backspace(self, case: str, initial: str, expected: str):
        s = io.StringIO(initial)
        tbuffer = TextBuffer(s)
        tbuffer.backspace()
        got = tbuffer.get_text()
        want = expected
        assert got == want, f"got '{got}', want '{want}' for case '{case}'"

    def test_insert(self):
        s = io.StringIO("Helo")
        tbuff = TextBuffer(s)
        tbuff.insert(2, "l")
        got = tbuff.get_text()
        want = "Hello"
        assert got == want, f"got '{got}', want '{want}'"
