"""Every action result states which backend produced it and whether it was simulated."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from amplifier_module_tool_cua import mount
from amplifier_module_tool_cua.backends.registry import BackendUnavailableError
from amplifier_module_tool_cua.tool import CuaTool

ACTIONS = [
    {"action": "screenshot"},
    {"action": "cursor_position"},
    {"action": "screen_info"},
    {"action": "window_info"},
    {"action": "semantic_tree"},
    {"action": "observe"},
    {"action": "click", "x": 1, "y": 2},
    {"action": "double_click", "x": 1, "y": 2},
    {"action": "type_text", "text": "hi"},
    {"action": "key_press", "key": "a"},
    {"action": "scroll", "x": 1, "y": 2, "dy": 3},
    {"action": "move_cursor", "x": 1, "y": 2},
    {"action": "nope"},
]


@pytest.mark.asyncio
@pytest.mark.parametrize("args", ACTIONS, ids=[a["action"] for a in ACTIONS])
async def test_fixture_results_are_marked_simulated(args):
    from amplifier_module_tool_cua.backends.fixture import FixtureBackend

    result = await CuaTool(backend=FixtureBackend()).execute(args)
    assert result["backend"] == "fixture"
    assert result["simulated"] is True


@pytest.mark.asyncio
async def test_native_results_are_not_marked_simulated():
    from amplifier_module_tool_cua.backends.linux import LinuxStubBackend

    result = await CuaTool(backend=LinuxStubBackend()).execute({"action": "click", "x": 1, "y": 1})
    assert result["backend"] == "linux"
    assert result["simulated"] is False


@pytest.mark.asyncio
async def test_exception_path_carries_provenance():
    class Boom:
        platform = "macos"

        async def click(self, **kw):
            raise RuntimeError("kaput")

    result = await CuaTool(backend=Boom()).execute({"action": "click"})  # type: ignore[arg-type]
    assert result["status"] == "failure"
    assert result["backend"] == "macos" and result["simulated"] is False


@pytest.mark.asyncio
async def test_mount_auto_surfaces_native_failure(coordinator, monkeypatch):
    monkeypatch.delenv("AMPLIFIER_CUA_BACKEND", raising=False)
    with patch("amplifier_module_tool_cua.backends.registry.sys") as mock_sys:
        mock_sys.platform = "freebsd"
        with pytest.raises(BackendUnavailableError):
            await mount(coordinator, config={"backend": "auto"})
    assert "tools" not in coordinator._mounted


@pytest.mark.asyncio
async def test_mount_explicit_fixture_still_works(coordinator):
    await mount(coordinator, config={"backend": "fixture"})
    tool = coordinator._mounted["tools"]["cua"]
    result = await tool.execute({"action": "click", "x": 1, "y": 1})
    assert result["simulated"] is True
