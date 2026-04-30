# Phase 7 — Final Cleanup & Delete Old API

**Goal:** Ship the rewrite. Delete the deprecation shims (or gate behind an env var for one more release). Remove the old SQLite catalog. Bump version.

**Size:** 0.5 day

**Blocked by:** Phase 6

---

## Scope

### Deletions

- [ ] `cimbuilder/_deprecated/` — delete, or gate behind `CIMBUILDER_LEGACY_API=1` env var with a final-release warning
- [ ] `cimbuilder/catalog/` — entire SQLite catalog subsystem (content moves to `cim-asset-manager`)
- [ ] `data_catalog/` directory at repo root (source JSON/CSV — moves to `cim-asset-manager`)
- [ ] `cimbuilder/utils/catalog_parser.py` (should already be gone after Phase 1, but verify)
- [ ] `cimbuilder/object_builder/deprecated/create_houses.py`
- [ ] Any remaining `__pycache__` or stale `.pyc` files

### Version bump

- `pyproject.toml`: version → `0.3.0a0`
- Update `README.md`:
  - Remove references to class-based API
  - Update installation / quickstart examples to use `SubstationSession`
  - Link to `docs/MIGRATION.md`

### Notebook refresh

All notebooks under `docs/` get a rewrite pass to use the new API. This is scope that may spill across multiple working sessions — track separately in `PHASE_CHECKPOINT.md`.

Minimum notebook coverage:
- [ ] `docs/01_overview/1_1_overview.ipynb`
- [ ] `docs/02_object_builder/2_1_object_builder.ipynb`
- [ ] `docs/03_substation_builder/3_1_single_bus.ipynb`
- [ ] `docs/03_substation_builder/3_2_sectionalized_bus.ipynb`
- [ ] `docs/03_substation_builder/breaker_and_half.ipynb`
- [ ] `docs/03_substation_builder/ring_bus.ipynb`
- [ ] `docs/03_substation_builder/main_and_transfer.ipynb`
- [ ] `docs/03_substation_builder/double_bus_single_breaker.ipynb`

### MCP contract pre-flight

Write a small script (`.development/tools/verify_mcp_contract.py`, not shipped) that:
1. Iterates every name in `cimbuilder.__all__`
2. Runs `inspect.signature()` on each
3. Asserts no `**kwargs` parameter
4. Asserts every parameter has a type annotation

---

## Exit criteria

- [ ] Repo contains no code paths from the pre-rewrite API (or only behind the `CIMBUILDER_LEGACY_API` gate).
- [ ] `uv run pytest` passes all tests.
- [ ] `uv build` produces a valid wheel.
- [ ] README and all notebooks in `docs/` reference only the new API.
- [ ] Version is `0.3.0a0`.
- [ ] MCP contract pre-flight script passes.
