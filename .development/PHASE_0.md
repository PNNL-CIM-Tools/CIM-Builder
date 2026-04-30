# Phase 0 — Foundation & Scaffolding

**Goal:** Get the skeleton and the contract right before any builder code moves.

**Size:** 0.5 day

---

## Scope

- `.development/` directory with planning docs (ARCHITECTURE, STYLE_GUIDE, PHASE_CHECKPOINT, PHASE_0..PHASE_8)
- New directory skeleton: `templates/`, `composite_builder/`, `topology_builder/`, `session/`, `_deprecated/`, plus `tests/<layer>/` subdirs
- `cimbuilder/_profile.py` with `get_cim()` helper using `TYPE_CHECKING` guard
- Reference implementation: port `new_breaker` to the new pattern (switches module exists today, so we overwrite the old one in place)
- `tests/conftest.py` with shared fixtures (CIM profile setup, minimal feeder factory, simple network factory, sample substation)
- `pyproject.toml`: add `pydantic>=2.0`, pin `cim-graph`

**Not in scope:**
- Other primitives (Phase 1)
- Templates beyond the empty package (Phase 1)
- Topology builders (Phase 3)
- Session classes (Phase 4)

---

## File checklist

### Created
- [x] `.development/ARCHITECTURE.md`
- [x] `.development/STYLE_GUIDE.md`
- [x] `.development/PHASE_CHECKPOINT.md`
- [x] `.development/PHASE_0.md` … `PHASE_8.md`
- [x] `cimbuilder/_profile.py`
- [x] `cimbuilder/templates/__init__.py` (empty, placeholder for Phase 1)
- [x] `cimbuilder/composite_builder/__init__.py` (empty, placeholder for Phase 2)
- [x] `cimbuilder/topology_builder/__init__.py` (empty, placeholder for Phase 3)
- [x] `cimbuilder/session/__init__.py` (empty, placeholder for Phase 4)
- [x] `cimbuilder/_deprecated/__init__.py` (empty, placeholder for Phase 5)
- [x] `tests/__init__.py`
- [x] `tests/conftest.py`
- [x] `tests/object_builder/__init__.py`
- [x] `tests/object_builder/switch/__init__.py`
- [x] `tests/object_builder/switch/test_new_breaker.py`

### Modified
- [x] `cimbuilder/object_builder/shunt/new_breaker.py` — rewritten per `STYLE_GUIDE.md`.  File stays in `shunt/` for Phase 0; Phase 1 relocates it to `switch/`.
- [x] `pyproject.toml` — added `pydantic>=2.0,<3`.

### Deferred to Phase 1 (intentional)
- `cimbuilder/utils/terminal.py` (split from `utils.py`) — Phase 1 does the utils split along with the full primitives rewrite
- `cimbuilder/__init__.py` rewrite — Phase 1 rewrites it as part of the primitives rewrite
- `cimbuilder/object_builder/__init__.py` cleanup — Phase 1

### Not modified in Phase 0
- All other existing builders (Phase 1)
- All substation topology classes (Phase 3)
- `aggregate_feeder.py` (Phase 2)
- `tests/test_single_bus_integration.py` — **already broken before Phase 0 started**: it imports `new_single_bus_substation` and `add_feeder_to_single_bus` from `cimbuilder`, which the CLAUDE.md describes as existing in `single_bus_functions.py`, but neither the functions nor that file exist in the repo today.  Phase 3 will land the functional topology API and re-enable this test.

---

## Exit criteria

1. [x] `uv run pytest tests/object_builder/switch/test_new_breaker.py` passes (6/6).
2. [~] `uv run pytest tests/test_single_bus_integration.py` still passes — **N/A; pre-existing failure not caused by Phase 0**.  See "Not modified" note above.  Re-enabled in Phase 3.
3. [x] The new `new_breaker` has no `import cimhub_2023 as cim` runtime shadow pattern.  Type hints live under `TYPE_CHECKING`.
4. [x] `cimbuilder._profile.get_cim()` works at runtime with the `cimhub_2023` profile (verified by fixtures and direct test).
5. [x] `pyproject.toml` includes `pydantic>=2.0` as a runtime dependency.
6. [x] `.development/` directory is complete.  (CLAUDE.md pointer update deferred; not a blocker — maintainers will add a line referencing `.development/` when they review.)

---

## Implementation notes

### Breaker location decision

There are currently two `new_breaker.py` files in the repo:
- `cimbuilder/object_builder/shunt/new_breaker.py` — the one that's imported
- There is no `switch/new_breaker.py` today, but the plan places breakers under `switch/`

**Decision:** move `new_breaker` to `object_builder/switch/new_breaker.py` (its correct CIM taxonomy location — Breaker is a Switch, not a Shunt). Keep the old `shunt/new_breaker.py` as a thin re-export for one release to avoid breaking the `from cimbuilder import new_breaker` path.

Actually — simpler: **overwrite `shunt/new_breaker.py` in Phase 0 with the new pattern, and move it to `switch/` in Phase 1 along with the other switch primitives**. Phase 0's job is the pattern, not the taxonomy.

### _profile.py minimal contract

```python
# cimbuilder/_profile.py
from __future__ import annotations
from typing import TYPE_CHECKING
from cimgraph.databases import get_cim_profile

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2023 as cim  # noqa: F401

def get_cim() -> "cim":
    """Return the active CIM profile module.

    Runtime lookup uses `cimgraph.databases.get_cim_profile()` which reads the
    CIMG_CIM_PROFILE environment variable.  The TYPE_CHECKING import above
    gives IDEs autocomplete for cim.Breaker, cim.Terminal, etc. without
    forcing runtime dependency on cimhub_2023 specifically.
    """
    _, cim_module = get_cim_profile()
    return cim_module
```

### conftest.py fixtures

- `setup_environment` — sets `CIMG_CIM_PROFILE=cimhub_2023`, yields
- `tmp_xml` — returns a `tmp_path / 'test.xml'` and a configured `XMLFile`
- `minimal_feeder` — creates a `FeederModel` with a single `sourcebus` `ConnectivityNode` and one `EnergySource`. Returns `(feeder, feeder_network)`.
- `simple_substation_network` — creates a `DistributedArea` + bare `Substation` + `BaseVoltage`, returns a dict
- `cim_profile` — returns the result of `get_cim_profile()` for tests that need the profile module

### Pyproject changes

- Keep `cim-graph>=0.4.3a10` (don't pin hard yet — cim-graph is actively maintained by the same user)
- Add `pydantic>=2.0,<3`
- No version bump in Phase 0 (stays at `0.0.1a0` until Phase 7 bumps to `0.3.0a0`)

---

## Verification

```bash
cd /home/ande188/CIM-Builder
uv sync --all-extras
uv run pytest tests/object_builder/switch/test_new_breaker.py -v
uv run pytest tests/test_single_bus_integration.py -v
```

Both must pass.
