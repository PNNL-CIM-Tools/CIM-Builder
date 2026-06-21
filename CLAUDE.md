# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

> **Status — refactor in progress (`feature/23`).** CIM-Builder is mid-way
> through a uniform builder-API refactor. This file describes **two things,
> clearly marked**: the *current* state of the code (what exists on this branch
> today) and the *target* builder-class API the refactor is moving toward. The
> day-by-day plan and the detailed specs live in `cimbuilder/development/` — read
> those before writing builder code. **Do not trust pre-refactor descriptions of
> a `catalog/` SQLite system, `*_functions.py` substation API, or a
> `feeder_builder/` module: none of those exist on this branch** (an attempted
> functional rewrite was reverted in `5b47fd6`).

## Project Overview

CIM-Builder is a Python library for creating CIM (Common Information Model)
models from scratch, without requiring pre-existing model files like OpenDSS,
PSSE, or GIS data. It builds on `cim-graph` (CIMantic Graphs), which provides the
graph model and CIM data-profile support.

The library builds:
1. Node-breaker substations in CIM
2. Distribution feeders inserted into node-breaker substations
3. Aggregate feeder data inserted into existing CIM transmission models
4. Individual CIM equipment objects (lines, transformers, switches, …)

## Development Commands

```bash
# Install dependencies (with dev extras)
uv sync --all-extras

# Run tests
uv run pytest
uv run pytest tests/path/to/test_file.py::test_function_name -v

# Build distribution packages
uv build
```

**Dependency note.** This branch pins `cim-graph>=0.5.0a2,<0.6.0` (a pre-release;
`[tool.uv] prerelease = "allow"` is set so the environment resolves). The 0.5
line is what provides `network.cim` and the `cgmes_3_0_0` merged profile the
refactor targets. See `cimbuilder/development/BASELINE.md` for why the pin moved.

---

## The refactor — read these first

The refactor introduces a single, uniform **builder-class API**: every equipment
type is an `ObjectBuilder` subclass built **one CIM profile-part at a time**
(connectivity → electrical → short-circuit → …). The specs:

| Doc (`cimbuilder/development/`) | What it defines |
|---|---|
| `README.md` | Index + reading order + locked decisions |
| `ARCHITECTURE.md` | `ObjectBuilder` contract, `builder_base` mixin, profile-source rule, substation assembly layer |
| `BUILDER_API.md` | The public `create() → add_<profile>() → build()` chain a user types |
| `PROFILE_TYPING.md` | §5a per-method profile-scoped typing (`cim: EQ` / `cim: SC`) |
| `UNITS.md` | CIMUnit in `add_electrical_bal`; per-unit deferred to Phase 11 |
| `BUILDER_TEST_CREATION.md` | Atom-test strategy for builders |
| `BASELINE.md` | Phase 0 audit: what's broken today + the leaf-builder work list |

The phase roadmap (phases 0–11, one per working day) is the execution plan the
above specs are implemented against.

### Target API (what the refactor builds toward)

```python
from cimbuilder import LineBuilder   # exported from cimbuilder/__init__.py (Phase 9)

line = (
    LineBuilder(network=network, container=feeder)
        .create(name='Line1')
        .add_connectivity(node1='busA', node2='busB')
        .add_electrical_bal(r=0.01, x=0.1, bch=0.0,
                            r_unit='ohm', x_unit='ohm', bch_unit='S')
        .add_short_circuit(r0=0.03, x0=0.3, b0ch=0.0)
        .build()
)
```

- Builder classes are stateless aside from the object under construction; each
  `add_<profile>` populates one profile part and returns `self`.
- `add_electrical_bal` sets balanced scalar impedance; `add_electrical_unbal`
  (per-phase) is a `NotImplementedError` stub until the CIM18 unbalanced parts
  ship.
- **Substations stay a separate assembly layer** — they orchestrate object
  builders, they are not `ObjectBuilder`s themselves.

---

## Current code structure (what exists on this branch today)

### `object_builder/` — equipment factory **functions** (pre-refactor)

Standalone `new_<equipment>(network, container, name, node1, node2, ...)`
functions, one per equipment category. They build the whole object (terminals +
connectivity + add-to-graph) in one call. **These are being ported to
`ObjectBuilder` subclasses** (Phases 3–6); the function bodies are the blueprint
for the builder methods.

Categories: `base/` (BaseVoltage lookup/create), `topology/` (bus bar section),
`shunt/` (breaker, capacitor), `switch/` (disconnector), `transformer/` (power
transformer + tap changer), `line/` (the `LineBuilder` eureka sketch),
`load/` (energy consumer), `generator/` (synchronous generator), `inverter/`
(PEC, EVSE family), `measurement/` (analog, discrete), `protection/`, and
`generic/` (`new_one_terminal_obj` / `new_two_terminal_obj`).

> **Profile import (the seam being closed).** Today every leaf function imports
> the flat profile at module scope:
> ```python
> import cimgraph.data_profile.cimhub_2023 as cim   # TODO: cleaner typing import
> ```
> The refactor replaces this with `cim = self.network.cim` inside each builder
> method (the cim-graph 0.5 layered-identity rule — see `ARCHITECTURE.md`). Do
> **not** add `get_cim_profile()` calls to leaf builders; the connection resolves
> the profile once and the model carries it as `network.cim`.

### `substation_builder/` — class-based substation assemblers

`@dataclass` classes (`SingleBusSubstation`, `MainAndTransferSubstation`,
`RingBus`, `SectionalizedBus`, `DoubleBusSingleBreaker`, `BreakerAndAHalf`)
inheriting `SubstationBuilder(ABC)` with `new_branch` / `new_feeder`. They
currently call the `new_*` functions and hard-import `cimhub_2023`. Phase 8
updates them to instantiate builder classes and read `self.network.cim`. This
layer **stays class-based** (a substation is a composition of many objects, not
one profile-built object).

### `utils/` — helpers (reuse, don't reinvent)

- `utils.py` — `terminal_to_node()` (connects a terminal to a node object *or*
  name string); the builder-base `_connect_node` wraps it.
- `get_base_voltage.py` — BaseVoltage lookup/create by nominal voltage.
- `get_source_bus.py` — feeder source-bus discovery (`NormalHeadTerminal`, then
  a node named `sourcebus`).
- `catalog_parser.py` — legacy JSON spec parser; the seam for `from_catalog`.

### `cimbuilder/__init__.py`

**Empty today.** Phase 9 populates it with the public builder/substation classes.
Until then there is no `cimbuilder.<symbol>` surface, and
`tests/test_single_bus_integration.py` (which imports `new_single_bus_substation`)
fails at collection — that test is reconciled in Phase 9.

---

## CIM-graph integration patterns

### Profile identity (the 0.5 contract)

The profile is resolved **once, at the connection** (`get_cim_profile()` inside
`ConnectionInterface.__init__`), and read downstream: the model sets
`self.cim = self.connection.cim`, and builders read `network.cim`. Never
re-derive the profile in a leaf — under a merged profile that yields a different
class object and misses every graph key. (`cimbuilder/development/BASELINE.md` §5
traces the full chain.)

### Graph model operations

- `network.add_to_graph(obj)` — add to the identity-keyed graph
- `network.get_all_edges(cim_class)` — hydrate associations
- `network.pprint(cim_class)` — pretty-print instances
- `network.upload()` — upload to a database (needs a `ConnectionInterface`)

### Terminal ↔ connectivity

```
Equipment -> Terminal -> ConnectivityNode <- Terminal <- Equipment
```

`utils.terminal_to_node()` wires a terminal to a node (object or name string).

### Units

Physical quantities are set via `CIMUnit` constructors with an input unit
(`cim.Resistance(v, 'ohm')`, `cim.Voltage(kv, 'kV')`); cimgraph stores SI
internally. **Never manually scale** (`* 1e3`, `* 1e6`). See
`cimbuilder/development/UNITS.md` and the global units guide in `~/.claude/CLAUDE.md`.

## Important Notes

- Python >=3.10.
- UUID generation uses deterministic seeding for reproducibility.
- BaseVoltage objects are searched by nominal voltage and created if not found.
- When adding feeders/branches to substations, breaker numbers generate unique
  equipment names.
