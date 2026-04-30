# CIM-Builder — Phase Checkpoint (live status)

**Last updated:** 2026-04-30

This document tracks live state across the rewrite. Update it at the end of each working session.

---

## Current phase

**Phase 0 — Foundation & Scaffolding** (complete, awaiting commit)

Next up: **Phase 1 — Templates & Primitives** (blocked until this commit lands).

---

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 0 | Foundation & Scaffolding | 🟢 done | `.development/` docs + `_profile.py` + reference `new_breaker` + `conftest.py` + `pyproject.toml`.  6/6 unit tests pass. |
| 1 | Templates & Primitives | ⚪ pending | Blocks on Phase 0 |
| 2 | Composites | ⚪ pending | Blocks on Phase 1 |
| 3 | Topology Builders | ⚪ pending | Blocks on Phase 2 |
| 4 | Session Classes | ⚪ pending | Blocks on Phase 3 |
| 5 | Back-Compat Shims | ⚪ pending | Blocks on Phase 4 |
| 6 | Catalog Integration & Defaults | ⚪ pending | Blocks on Phase 5; NERC PDFs needed for content |
| 7 | Final Cleanup & Deletion | ⚪ pending | Blocks on Phase 6 |
| 8 | Dynamics builders (deferred) | ⚫ gated | Gated on `cim17v40.dynamics` profile in cim-graph |
| 9 | Split-profile distribution (deferred) | ⚫ gated | Gated on `cimgraph.data_profile.merge` verification |
| 10 | Protection builders (deferred) | ⚫ gated | Driven by downstream demand |
| 11 | MCP server (separate repo) | ⚫ external | Owned by `cim-builder-mcp` |
| 12 | GUI binding (separate repo) | ⚫ external | Owned by `CIMantic-Studio` Phase 5-6 |

Legend: 🟢 done · 🟡 in progress · ⚪ pending · ⚫ gated/external

---

## Open decisions / risks

- **cim-asset-manager timeline**: currently shimmed via internal `cimbuilder/templates/`. Swap when ready (Phase 6+).
- **merge.py verification**: cim-graph's split-profile merge is not yet tested end-to-end. Universal builders (Phases 1-7) do not depend on it.
- **NERC DER PDFs**: Phase 6 needs user-provided PDF source for default DER parameters. Plumbing ships without content.

---

## Session log

### 2026-04-30 — Planning + Phase 0 complete
- Wrote target plan at `/home/ande188/.claude/plans/i-am-the-maintainer-fizzy-blossom.md` (approved by user).
- Created `.development/` docs: `ARCHITECTURE.md`, `STYLE_GUIDE.md`, `PHASE_CHECKPOINT.md`, `PHASE_0.md`–`PHASE_8.md`.
- Added `cimbuilder/_profile.py` with `get_cim()` helper + `TYPE_CHECKING` guard.
- Rewrote `cimbuilder/object_builder/shunt/new_breaker.py` as the reference implementation per `STYLE_GUIDE.md` canonical signature.
- Created `tests/conftest.py` with shared fixtures (`setup_environment`, `cim_profile`, `tmp_xml`, `simple_substation_network`, `connectivity_nodes`, `minimal_feeder`).
- Created `tests/object_builder/switch/test_new_breaker.py` (6 tests, all pass).
- Added package skeletons: `cimbuilder/templates/`, `composite_builder/`, `topology_builder/`, `session/`, `_deprecated/` — all placeholder `__init__.py` only.
- Added `pydantic>=2.0,<3` to `pyproject.toml`.
- **Discovered:** `tests/test_single_bus_integration.py` was already broken before Phase 0 — it imports `new_single_bus_substation` / `add_feeder_to_single_bus` that CLAUDE.md claims exist but do not.  Documented as Phase 3 work.

<!-- Append new session entries here as sessions close -->
