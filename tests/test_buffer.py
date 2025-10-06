import pytest
import io
from text_editor.core.buffer import TextBuffer


def test_append_characters():
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
def test_backspace(case: str, initial: str, expected: str):
    s = io.StringIO(initial)
    tbuffer = TextBuffer(s)
    tbuffer.backspace()
    got = tbuffer.get_text()
    want = expected
    assert got == want, f"got '{got}', want '{want}' for case '{case}'"
