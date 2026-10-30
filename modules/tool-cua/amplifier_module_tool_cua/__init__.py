"""Computer-use automation tool module for Amplifier."""

from __future__ import annotations

import logging
from typing import Any

__amplifier_module_type__ = "tool"

logger = logging.getLogger(__name__)


async def mount(coordinator: Any, config: dict[str, Any] | None = None) -> None:
    """Mount the CUA tool into the Amplifier coordinator.

    Config options:
        backend: Force a specific backend. Values: "fixture", "auto" (default).
                 "auto" detects the current platform and uses its native backend;
                 it raises BackendUnavailableError rather than silently using the
                 simulated fixture. The fixture is used only when requested
                 explicitly (backend: fixture, or AMPLIFIER_CUA_BACKEND=fixture).
                 Every action result carries "backend" and "simulated" fields.
    """
    from .backends.registry import get_backend
    from .tool import CuaTool

    config = config or {}
    backend_name = config.get("backend", "auto")
    backend = get_backend(backend_name)

    tool = CuaTool(backend=backend)
    await coordinator.mount("tools", tool, name=tool.name)
    logger.info("tool-cua mounted with backend=%s", backend.platform)
