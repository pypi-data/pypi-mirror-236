from __future__ import annotations

import os
import sys
from enum import Enum


class Colour(Enum):
    NORMAL = "\033[m"
    RED = "\033[41m"
    BOLD = "\033[1m"
    GREEN = "\033[42m"
    YELLOW = "\033[43;30m"
    TURQUOISE = "\033[46;30m"

    _use_colour = sys.stdout.isatty() and os.getenv("TERM") != "dumb"

    @classmethod
    def highlight(cls, text: str, colour: Colour, replace_in: str | None = None) -> str:
        if cls._use_colour:
            new_text = f"{colour.value}{text}{cls.NORMAL.value}"
        else:
            new_text = text
        if replace_in:
            new_text = replace_in.replace(text, new_text)
        return new_text
