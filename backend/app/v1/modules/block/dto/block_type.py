from enum import Enum


class BlockType(str, Enum):
    """
    Supported educational block types rendered by QuantumMind.
    """

    HEADING = "heading"

    PARAGRAPH = "paragraph"

    LIST = "list"

    EQUATION = "equation"

    IMAGE = "image"

    CODE = "code"

    QUOTE = "quote"

    NOTE = "note"

    WARNING = "warning"

    EXAMPLE = "example"

    EXERCISE = "exercise"

    QUIZ = "quiz"

    INTERACTIVE = "interactive"