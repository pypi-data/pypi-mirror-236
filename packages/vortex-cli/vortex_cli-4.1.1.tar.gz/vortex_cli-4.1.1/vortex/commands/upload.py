from __future__ import annotations

import logging
from pathlib import Path

from vortex.models import PuakmaServer
from vortex.spinner import Spinner

logger = logging.getLogger("vortex")


def upload(server: PuakmaServer, group: str, name: str, pmx_path: Path) -> int:
    with Spinner("Uploading..."):
        with open(pmx_path, "rb") as f:
            pmx_bytes = f.read()

        with server as s:
            app_id = s.download_designer.upload_pmx(group, name, pmx_bytes)

    print(f"Successfully created {group}/{name} [{app_id}] from {pmx_path.name}")
    return 0
