from __future__ import annotations

from datetime import datetime

import tabulate

from vortex import util
from vortex.colour import Colour
from vortex.models import PuakmaServer

_LOG_TYPE_COLOUR_MAP = {
    "D": Colour.TURQUOISE,
    "I": Colour.YELLOW,
    "E": Colour.RED,
}


def log(
    server: PuakmaServer,
    limit: int,
    source_filter: str | None,
    messsage_filter: str | None,
    errors_only: bool,
    info_only: bool,
    debug_only: bool,
) -> int:
    with server as s:
        logs = s.get_last_log_items(
            limit, source_filter, messsage_filter, errors_only, info_only, debug_only
        )

    row_headers = ("Time", "Source", "Message")
    row_data = []
    for log in sorted(logs, key=lambda x: x.date):
        log_colour = _LOG_TYPE_COLOUR_MAP[log.type]
        row = [
            Colour.highlight(
                datetime.strftime(log.date, "%d/%m/%Y %H:%M:%S"), log_colour
            ),
            util.shorten_text(log.item_source),
            log.msg,
        ]
        row_data.append(row)

    print(tabulate.tabulate(row_data, headers=row_headers, maxcolwidths=[None, 30, 80]))

    return 0
