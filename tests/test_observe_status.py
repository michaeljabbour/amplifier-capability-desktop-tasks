"""A composite observation must not claim a complete snapshot after failures."""

from __future__ import annotations

import pytest

from amplifier_module_tool_cua.models import ActionResult, ActionStatus
from amplifier_module_tool_cua.tool import CuaTool


class ObservationBackend:
    platform = "test"
    simulated = True

    def __init__(self, outcomes):
        self.outcomes = outcomes

    async def _observe(self, name):
        outcome = self.outcomes[name]
        if isinstance(outcome, Exception):
            raise outcome
        return ActionResult(outcome, message=f"{name} {outcome.value}", data={
            "screenshot_base64": "image", "x": 1, "y": 2,
            "windows": [], "focused_window": None, "elements": [],
        })

    async def screenshot(self):
        return await self._observe("screenshot")

    async def cursor_position(self):
        return await self._observe("cursor_position")

    async def window_info(self):
        return await self._observe("window_info")

    async def semantic_tree(self):
        return await self._observe("semantic_tree")


NAMES = ("screenshot", "cursor_position", "window_info", "semantic_tree")


@pytest.mark.asyncio
@pytest.mark.parametrize("outcome,expected", [
    (ActionStatus.SUCCESS, "success"),
    (ActionStatus.FAILURE, "failure"),
    (ActionStatus.BLOCKED, "blocked"),
])
async def test_uniform_observation_status(outcome, expected):
    result = await CuaTool(ObservationBackend(dict.fromkeys(NAMES, outcome))).execute({"action": "observe"})
    assert result["status"] == expected
    assert result["partial"] is False
    assert set(result["observations"]) == set(NAMES)
    assert all(x["status"] == outcome.value for x in result["observations"].values())
    assert result["backend"] == "test" and result["simulated"] is True
    if outcome != ActionStatus.SUCCESS:
        assert result["data"] == {}
        assert result["message"]


@pytest.mark.asyncio
async def test_partial_observation_keeps_confirmed_data_and_failure_receipts():
    outcomes = dict.fromkeys(NAMES, ActionStatus.FAILURE)
    outcomes["screenshot"] = ActionStatus.SUCCESS
    result = await CuaTool(ObservationBackend(outcomes)).execute({"action": "observe"})
    assert result["status"] == "ambiguous" and result["partial"] is True
    assert result["data"] == {"screenshot_base64": "image"}
    assert result["observations"]["cursor_position"]["status"] == "failure"
    assert "1/4" in result["message"]
    assert result["backend"] == "test" and result["simulated"] is True


@pytest.mark.asyncio
async def test_component_exception_does_not_discard_other_observations():
    outcomes = dict.fromkeys(NAMES, ActionStatus.SUCCESS)
    outcomes["cursor_position"] = RuntimeError("cursor unavailable")
    result = await CuaTool(ObservationBackend(outcomes)).execute({"action": "observe"})
    assert result["status"] == "ambiguous" and result["partial"] is True
    assert result["data"]["screenshot_base64"] == "image"
    assert "semantic_tree" in result["data"]
    assert "cursor" not in result["data"]
    assert result["observations"]["cursor_position"] == {"status": "failure", "message": "cursor unavailable"}
    assert "3/4" in result["message"]
    assert result["backend"] == "test" and result["simulated"] is True


@pytest.mark.asyncio
async def test_all_component_exceptions_are_failure_with_provenance():
    result = await CuaTool(ObservationBackend(dict.fromkeys(NAMES, RuntimeError("unavailable")))).execute({"action": "observe"})
    assert result["status"] == "failure" and result["partial"] is False
    assert result["data"] == {}
    assert all(x["status"] == "failure" for x in result["observations"].values())
    assert result["backend"] == "test" and result["simulated"] is True
