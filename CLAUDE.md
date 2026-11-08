# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

CIM-Builder is a Python library (PNNL, Grid Atlas / MAPLE LEAF projects) for constructing CIM
(Common Information Model) power system models **from scratch**, with no source file to start from
(unlike OpenDSS/PSSE/GIS-based tooling). It builds:

1. New node-breaker substations via interactive API calls.
2. Insertion of existing distribution feeders into those substations.
3. Insertion of aggregate feeder data into existing CIM transmission models.

**The repo is mid-rewrite** (branch `cimtbl_rewrite`). `cimbuilder/object_builder/` is the active,
current pattern — one builder class per CIM class, following `ObjectBuilder` in
`cimbuilder/object_builder/object_builder.py`. `cimbuilder/substation_builder/` is legacy code from
before a revert (`5b47fd6 Revert "rewrite substation builder as functions"`) and does not match the
current API (references undefined `field()`/module globals, calls `utils.get_base_voltage` with the
old signature) — treat it as not yet ported rather than as a pattern to copy. Likewise
`tests/test_single_bus_integration.py` imports `new_single_bus_substation`/`add_feeder_to_single_bus`
from `cimbuilder/__init__.py`, which no longer exports them — that test predates the rewrite.

## Dependencies — sibling repos

This package depends on three PNNL sibling repos, wired as editable local installs in `pyproject.toml`
(`[tool.uv.sources]`), checked out next to this repo (`/home/ande188/CIM-Tables`, `/home/ande188/CIM-Profiles`,
`/home/ande188/CIM-Graph`):

- **`cimprofiles`** — generated CIM18v17 profile submodules, each representing one *facet* of a CIM
  class's data (see "Profile parts" below).
- **`cimtables`** — the write/validation helpers builders call into: `graph_write`, `connectivity`,
  `binder`, `units` (`Qty`). This is where unit conversion and FK/association resolution actually happen.
- **`cim-graph`** (`cimgraph`) — the underlying graph model (`GraphModel`, `DistributedArea`,
  `FeederModel`, `NodeBreakerModel`, database connections like `XMLFile`).

When something looks missing or oddly behaved in a builder (e.g. a `set_attr`/`set_assc_from_mrid`
call), check `cimtables` source directly rather than guessing — it is a local editable package, not
black-box external code.

## Commands

```bash
uv sync                      # install deps (incl. editable sibling repos)
uv run pytest                # run tests
uv run pytest tests/path/to/test_file.py::test_name   # run a single test
```

There is no lint/format config in this repo (no `ruff`/`black` config, no pytest.ini section) — match
surrounding file style.

Note: most of `tests/object_builder/**` subdirectories (one per CIM category: shunt, switch,
transformer, line, load, etc.) currently contain no test files — only
`tests/test_single_bus_integration.py` exists today, and per the note above it targets a pre-rewrite
API and will likely need updating/replacing as the rewrite proceeds.

## Architecture: the ObjectBuilder pattern

Every concrete builder lives under `cimbuilder/object_builder/<category>/` (e.g. `shunt/`, `switch/`,
`transformer/`, `line/`, `load/`, `generator/`, `inverter/`, `measurement/`, `protection/`, `limit/`,
`topology/`, `generic/`) and subclasses `ObjectBuilder`:

```python
class ObjectBuilder(ABC):
    cim_class_name: str   # e.g. "LinearShuntCompensator" — resolved off network.cim at runtime

    def __init__(self, network: GraphModel, container: CN.EquipmentContainer):
        ...

    def create(self, *, mRID=None, name=None, identifier=None, description=None) -> object:
        """Instantiates cim_class_name, adds it to network.graph. Returns the unadded... actually added object."""

    def from_table(self, row: object) -> object:
        """DSL/bulk entry point: binds a validated `<Class>Row` dataclass via cimtables.binder.bind_row."""
```

Each concrete builder (e.g. `LinearShuntCompensatorBuilder` in
`cimbuilder/object_builder/shunt/linear_shunt_compensator.py`) adds a fixed sequence of `add_*` methods
on top of `create()`, each targeting a different **profile part**:

- `add_connectivity` — terminals, `EquipmentContainer`, `BaseVoltage`, phase children (profile part `CN`
  = `connectivity_unbalanced`). Builders for devices with terminals call
  `cimtables.connectivity.add_connectivity(...)` to create `Terminal`s and
  `cimtables.connectivity.add_phase_children(...)` for per-phase sub-objects.
- `add_electrical` — steady-state electrical parameters (profile part `EL_BAL` =
  `electrical_balanced`, or `EL_UNBAL` for unbalanced).
- `add_short_circuit` — zero-sequence / fault parameters (profile part `SC` = `short_circuit`).
- `add_ssh` — real-time/basecase state like `sections`, `inService` (profile part `SSH` =
  `steady_state_hypothesis`).
- Other parts seen across builders: `TP` (`topology`), `LIM` (`operational_limit`), `CONST`/`CONSTR`
  (`construction`), `AD` (`asset_deployment`).

A builder method takes the already-`create()`'d CIM object plus keyword-only params, writes into one
profile part per call via `cimtables.graph_write.set_attr(...)` (scalar attrs, with automatic unit
handling for `Qty`/`float` and `system_base=self.network.base_power` for per-unit fields) and
`cimtables.graph_write.set_assc_from_mrid(...)` (associations resolved by mRID string against
`self.network`), and returns the mutated object (plus any created `Terminal`/phase objects as a tuple).
Builders never instantiate CIM classes directly except in `create()` — all profile-part classes are
looked up off the already-created object's type at the respective profile-part level.

**When adding a new builder**, follow the shape of an existing one in the same category
(`cimbuilder/object_builder/shunt/linear_shunt_compensator.py` is a good four-method reference covering
connectivity + electrical + short-circuit + ssh). Keep one `add_*` method per profile part; don't merge
unrelated profile parts into a single method.

## Units

See the global units guidance for `CIMUnit`/`Qty` conventions (import source units, export with `.to()`,
never hand-multiply by powers of ten). In this repo that machinery is invoked through
`cimtables.graph_write.set_attr(..., system_base=...)` rather than called directly by builders.
