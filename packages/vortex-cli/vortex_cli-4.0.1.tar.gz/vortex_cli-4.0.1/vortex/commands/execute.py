from __future__ import annotations

import logging

from vortex.models import PuakmaServer

logger = logging.getLogger("vortex")


def execute(server: PuakmaServer, command: str) -> int:
    with server as s:
        resp = s.server_designer.execute_command(command)
    if resp:
        print(resp)
    return 0
