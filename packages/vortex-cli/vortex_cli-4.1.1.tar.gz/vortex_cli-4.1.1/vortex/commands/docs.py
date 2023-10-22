from __future__ import annotations

import os
import webbrowser


def docs() -> int:
    doc_path = os.path.join(
        os.path.dirname(__file__), "..", "docs", "Tornado Server Blackbook.pdf"
    )
    webbrowser.open_new(doc_path)
    return 0
