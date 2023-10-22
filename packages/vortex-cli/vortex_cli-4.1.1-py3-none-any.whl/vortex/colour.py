from __future__ import annotations

import os
import sys


NORMAL = "\033[m"
RED = "\033[41m"
BOLD = "\033[1m"
GREEN = "\033[42m"
YELLOW = "\033[43;30m"
TURQUOISE = "\033[46;30m"

_terminal_supports_colour = sys.stdout.isatty() and os.getenv("TERM") != "dumb"
_use_colour = _terminal_supports_colour


def set_use_colour(use_colour: bool) -> None:
    global _use_colour
    _use_colour = _terminal_supports_colour and use_colour


def colour(
    text: str,
    colour: str,
    replace_in: str | None = None,
    use_colour: bool | None = None,
) -> str:
    _do_colour = _use_colour
    if use_colour is not None:
        _do_colour = _terminal_supports_colour and use_colour

    if _do_colour:
        coloured_text = f"{colour}{text}{NORMAL}"
    else:
        coloured_text = text

    if replace_in:
        coloured_text = replace_in.replace(text, coloured_text)
    return coloured_text
