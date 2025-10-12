import io


class TextBuffer:
    def __init__(self, source: io.IOBase = None) -> None:
        self._text = source.read() if source else ""

    def get_text(self) -> str:
        """Get the current text in the buffer."""
        return self._text

    def append(self, text: str) -> None:
        """Append text to the buffer."""
        self._text += text

    def backspace(self) -> None:
        """Remove the last character from the buffer."""
        self._text = self._text[:-1]

    def insert(self, index: int, text: str) -> None:
        """Insert text at a specific index in the buffer."""
        self._text = self._text[:index] + text + self._text[index:]
