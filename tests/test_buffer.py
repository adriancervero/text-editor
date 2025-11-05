import pytest
import io
from text_editor.core.buffer import TextBuffer, PieceTable, Piece


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


def assertText(original_buffer, add_buffer, pieces, expected_text):
    pt = PieceTable()
    pt.original_buffer = original_buffer
    pt.add_buffer = add_buffer
    pt.pieces = pieces

    got = pt.get_text()
    want = expected_text
    assert got == want, f"got {got}, want {want}"


class TestPieceTable:
    @pytest.mark.parametrize(
        "case, original_text",
        [
            ("empty original", ""),
            ("non-empty original", "Hello, World!"),
        ],
    )
    def test_init_with_original_text(self, case: str, original_text: str):
        pt = PieceTable(original=original_text)
        assert len(pt.pieces) == 1
        assert pt.add_buffer == ""
        assert pt.original_buffer == original_text
        piece = pt.pieces[0]
        assert piece.source == "original"
        assert piece.start == 0
        assert piece.length == len(original_text)

    def test_get_text(self):
        original_buffer = "Hello"
        add_buffer = " world"
        pieces = [
            Piece(source="original", start=0, length=5),
            Piece(source="add", start=0, length=6),
        ]
        expected_text = "Hello world"
        assertText(original_buffer, add_buffer, pieces, expected_text)

        original_buffer = "ello"
        add_buffer = "H"
        pieces = [
            Piece(source="add", start=0, length=1),
            Piece(source="original", start=0, length=4),
        ]
        expected_text = "Hello"
        assertText(original_buffer, add_buffer, pieces, expected_text)

        original_buffer = "Helo"
        add_buffer = "l"
        pieces = [
            Piece(source="original", start=0, length=2),
            Piece(source="add", start=0, length=1),
            Piece(source="original", start=2, length=2),
        ]
        expected_text = "Hello"
        assertText(original_buffer, add_buffer, pieces, expected_text)

    @pytest.mark.parametrize(
        "case, original_text, text_to_add, pos, expected_text",
        [
            ("at the end", "Hello", " world", 5, "Hello world"),
            ("at the start", "ello", "H", 0, "Hello"),
            ("at center", "Helo", "l", 2, "Hello"),
        ],
    )
    def test_add_text(self, case, original_text, text_to_add, pos, expected_text):
        pt = PieceTable(original=original_text)
        pt.add(text_to_add, pos)
        got = pt.get_text()
        assert got == expected_text, f"got {got}, want {expected_text}"

    def test_multiple_add_text(self):
        original_text = "From beggining"

        pt = PieceTable(original=original_text)

        pt.add(" the end", 14)
        want = "From beggining the end"
        got = pt.get_text()
        assert got == want, f"first add: got {got}, want {want}"

        pt.add(" to", 14)
        want = "From beggining to the end"
        got = pt.get_text()
        assert got == want, f"second add, got {got}, want {want}"
