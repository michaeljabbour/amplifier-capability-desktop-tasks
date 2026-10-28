---
name: desktop-tasks
description: "Complete a bounded desktop task through observed controls and verify the resulting state. Use when asked to operate an application through an available computer-use surface."
---

# Desktop Tasks

Use the host computer-use tool that is actually available. This package supplies the operating method; it does not grant desktop access or invent missing tools. Prefer a purpose-built API when it can complete the requested operation.

Plan: identify the application, desired final state, user authorization and observable success condition. Keep the supplied native 20-action/2-retry defaults unless the task calls for another bounded budget. Count actions and report partial work when the budget ends.

Operate: read references/dual-world-reasoning.md and references/action-confidence.md. Use accessibility data to identify a control, then confirm it against the visible state. Coordinate-only actions require a current screenshot. If the two views disagree, re-observe before acting. Follow the host's own reference and permission rules.

Recover: read references/recovery-patterns.md only when needed. A success return without the expected post-state is ambiguous. Re-observe at most twice for one uncertain step, then stop or use an evidenced alternative. Do not repeat a consequential submission merely because its response was unclear.

Record what was observed, attempted and verified. A fixture pass proves backend plumbing only. The retained native modules/tool-cua contains real platform backends and a deterministic FixtureBackend; installation of that optional adapter does not demonstrate live OS permission or physical task acceptance.
