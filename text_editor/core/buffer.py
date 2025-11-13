import io
from dataclasses import dataclass


@dataclass
class Piece:
    source: str
    start: int
    length: int


class PiecesList:
    def __init__(self, pieces=[]):
        self.pieces: list[Piece] = pieces

    def __len__(self):
        return len(self.pieces)

    def __iter__(self):
        for piece in self.pieces:
            yield piece

    def __getitem__(self, index):
        return self.pieces[index]

    def insert(self, piece: Piece, pos: int) -> None:
        """
        Insert a piece at the given logical position.
        If the position is inside an existing piece, split it.
        """
        curr_pos = 0
        idx = 0

        # Find the piece index where to insert
        while idx < len(self.pieces) and curr_pos < pos:
            curr_piece = self.pieces[idx]
            curr_pos += curr_piece.length
            idx += 1

        if idx > 0:
            curr_piece = self.pieces[idx - 1]
        else:
            curr_piece = None

        # If position is inside a piece, split it
        if curr_piece and curr_pos != pos:
            left_length = pos - (curr_pos - curr_piece.length)
            right_length = curr_piece.length - left_length

            # Adjust current piece to left length
            curr_piece.length = left_length

            # Create right piece
            right_piece = Piece(
                source=curr_piece.source,
                start=curr_piece.start + left_length,
                length=right_length,
            )

            self.pieces.insert(idx, piece)
            self.pieces.insert(idx + 1, right_piece)
        else:
            self.pieces.insert(idx, piece)


class PieceTable:
    def __init__(self, original: str = "") -> None:
        self.original_buffer = original
        self.add_buffer = ""
        self.pieces = PiecesList([Piece("original", 0, len(original))])

    def get_text(self) -> str:
        text = ""
        for piece in self.pieces:
            if piece.source == "original":
                buffer = self.original_buffer
            else:
                buffer = self.add_buffer
            text += buffer[piece.start : piece.start + piece.length]
        return text

    def add(self, text: str, pos: int) -> None:
        added_piece = Piece(source="add", start=len(self.add_buffer), length=len(text))
        self.add_buffer += text
        self.pieces.insert(added_piece, pos)


class TextBuffer:
    def __init__(self, source: io.IOBase = None) -> None:
        text = source.read() if source else ""
        self.buffer = PieceTable(text)

    def get_text(self) -> str:
        """Get the current text in the buffer."""
        return self.buffer.get_text()

    def append(self, text: str) -> None:
        """Append text to the buffer."""
        self.buffer.add(text, len(self.buffer.get_text()))

    def backspace(self) -> None:
        """Remove the last character from the buffer."""
        pass

    def insert(self, index: int, text: str) -> None:
        """Insert text at a specific index in the buffer."""
        self.buffer.add(text, index)
