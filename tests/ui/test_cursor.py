import pytest

from text_editor.ui.cursor import TextCursor


class MockWidget:
    def update(self):
        pass


def make_cursor(row, col, paddx, paddy):
    cursor = TextCursor(
        row=row,
        col=col,
        paddx=paddx,
        paddy=paddy,
        char_width=10,
        line_height=20,
        parent=MockWidget(),
    )
    return cursor


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
        cursor = make_cursor(row, col, paddx, paddy)
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
        cursor = make_cursor(row, col, 0, 0)
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
        cursor = make_cursor(initial_row, initial_col, 0, 0)
        cursor.move(row_delta, col_delta)
        got_row, got_col = cursor.get_position()
        assert (got_row, got_col) == (expected_row, expected_col), (
            f"Failed for case '{case}': got ({got_row},{got_col}), "
            f"want ({expected_row},{expected_col})"
        )
