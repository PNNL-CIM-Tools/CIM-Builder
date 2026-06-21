# Phase 0 — Baseline & Prerequisite Audit

The Phase 0 deliverable from the refactor roadmap
(`/home/ande188/.claude/plans/take-a-look-at-buzzing-crane.md`): a snapshot of
exactly what is broken today, an inventory of the leaf builders to port, the
inconsistencies to fix in-flight, and confirmation that the cim-graph 0.5.0a1
prerequisites are met. **No code was edited in this phase.**

Audited on branch `feature/23` (HEAD `362ba33`) against the local cim-graph
checkout at `/home/ande188/CIM-Graph` (v0.5.0a1).

---

## 1. Current state — the repo does not resolve, import, or test

| Check | Result |
|---|---|
| `cimbuilder/__init__.py` | **empty (0 lines)** — no public surface |
| `pyproject.toml` cim-graph pin | `cim-graph>=0.3.2a2,<0.4.0` |
| `uv sync` / `uv run` | **fails to resolve dependencies** (see below) |
| Test files | exactly one: `tests/test_single_bus_integration.py` |
| That test's imports | `from cimbuilder import new_single_bus_substation, add_feeder_to_single_bus` — **both unresolvable** |

### 1a. Dependency resolution is broken

`uv run` cannot build the environment at the current pin:

```
cim-graph>=0.3.2a2,<=0.3.2a3 depends on gridappsd-python>=2025.3.2a1,<2026.0.0
gridappsd-python was requested with a pre-release marker, but pre-releases
weren't enabled  →  requirements are unsatisfiable
```

So **nothing runs today** without `--prerelease=allow`, and even then the pin
targets the flat `cimhub_2023` profile, not the 0.5 line this refactor needs.
This makes the Phase 1 pin bump a hard prerequisite, not a cleanup — it is the
gate that lets the test suite run at all.

### 1b. The broken test

`tests/test_single_bus_integration.py` imports `new_single_bus_substation` and
`add_feeder_to_single_bus` from `cimbuilder`. These are the functional
`*_functions.py` symbols that were **reverted** in `5b47fd6 Revert "rewrite
substation builder as functions"` and never re-landed. Combined with the empty
`__init__.py`, the import fails at collection time. This is the test Phase 9
reconciles (implement as facades or rewrite to the class API).

---

## 2. Profile-resolution inventory (the rule the refactor changes)

**Finding that corrects the plan's assumption.** The plan text spoke of leaf
builders and substations resolving the profile via `get_cim_profile()`. They do
**not**. Every leaf builder and every substation hard-imports the flat profile
module at module scope:

```python
import cimgraph.data_profile.cimhub_2023 as cim   # TODO: cleaner typing import
```

The `# TODO: cleaner typing import` comment recurs across the codebase — it is
the seam this refactor closes. Only the **eureka sketch**
(`object_builder/line/line_builder.py`) uses `get_cim_profile()`, and it does so
incorrectly per the 0.5 contract (`cim: CN = get_cim_profile()` at lines 32, 50,
65).

So the profile-source rule (`ARCHITECTURE.md`) replaces a **hard-coded flat
module import** with `cim = self.network.cim` — *not* a `get_cim_profile()` call.
The net effect is the same (stop pinning the profile in the leaf), but the
mechanical edit differs from what the plan described.

Files carrying the hard `cimhub_2023` import:

- Leaves: `shunt/new_breaker.py`, `shunt/new_capacitor.py`,
  `switch/new_disconnector.py`, `topology/new_bus_bar_section.py`,
  `generic/new_two_terminal_obj.py`, `generic/new_one_terminal_obj.py`,
  `transformer/new_power_transformer.py`, `transformer/new_tap_changer.py`,
  `load/new_energy_consumer.py`, `generator/new_synchronous_generator.py`,
  the `inverter/new_EVSE*` family, `measurement/new_analog.py`,
  `measurement/new_discrete.py`,
  `protection/new_under_frequency_protection_function_block.py`,
  `base/new_base_voltage.py`.
- Substations: `single_bus.py`, `double_bus_single_breaker.py`,
  `sectionalized_bus.py`, `ring_bus.py`, `breaker_and_a_half.py`,
  `main_and_transfer.py`. (`substation_builder.py` imports `cimgraph.utils as
  cim_utils`, not a profile module.)

---

## 3. Leaf-builder inventory (Phases 3–6 work list)

All under `cimbuilder/object_builder/`. `__init__.py` and `__pycache__` omitted.

| File | Target builder | Phase |
|---|---|---|
| `line/line_builder.py` (sketch) | `LineBuilder` (reference impl) | 3 |
| `topology/new_bus_bar_section.py` | `BusBarSectionBuilder` | 4 |
| `shunt/new_breaker.py` | `BreakerBuilder` | 4 |
| `switch/new_disconnector.py` | `DisconnectorBuilder` | 4 |
| `generic/new_one_terminal_obj.py` | `GenericOneTerminalBuilder` | 5 |
| `generic/new_two_terminal_obj.py` | `GenericTwoTerminalBuilder` | 5 |
| `transformer/new_power_transformer.py` | `PowerTransformerBuilder` | 6 |
| `transformer/new_tap_changer.py` | (tap changer, folded into xfmr) | 6 |
| `shunt/new_capacitor.py` | `CapacitorBuilder` | 6 |
| `load/new_energy_consumer.py` | `EnergyConsumerBuilder` | 6 |
| `generator/new_synchronous_generator.py` | `SynchronousGeneratorBuilder` | 6 |
| `inverter/new_power_electronics_connection.py` + `new_EVSE*` (5 files) | PEC / inverter family | 6 |
| `measurement/new_analog.py`, `measurement/new_discrete.py` | measurement builders | 6 |
| `protection/new_under_frequency_protection_function_block.py` | protection block | 6 |
| `base/new_base_voltage.py` | reused as-is (not a builder; lookup/create) | — |
| `deprecated/create_houses.py` | delete in Phase 10 | 10 |

Already-present stub files (committed, were the eureka probe): `object_builder.py`
(the `ObjectBuilder` ABC), `line/line_builder.py`, `topology/terminal_builder.py`.

---

## 4. Inconsistencies to fix in-flight (confirmed)

1. **Disconnector double-uuid bug** — `switch/new_disconnector.py:18–22`:
   ```python
   t1 = cim.Terminal()
   t1.uuid(name=f"{name}_t1")
   t2 = cim.Terminal()
   t1.uuid(name=f"{name}_t2")   # BUG: seeds t1 again; t2 never gets a uuid
   ```
   The `builder_base._new_terminal` helper (Phase 2) fixes this by construction.

2. **Hand-rolled terminal idiom** — `topology/new_bus_bar_section.py:21` builds
   `cim.Terminal()` inline and adds it separately (`add_to_graph` at lines 27/28),
   rather than through a shared helper. Each leaf reinvents terminal creation;
   centralizing in `builder_base` removes the drift.

3. **Mixed terminal-naming idiom** — some builders use `cim.Terminal(name=...)`,
   others construct then call `t.uuid(name=...)`. The `_new_terminal` helper
   standardizes seeding + `sequenceNumber` + `ConductingEquipment` + append.

4. **Pervasive `# TODO: cleaner typing import`** — the flat `cimhub_2023` import
   noted in §2; removed once `network.cim` is the source.

---

## 5. Prerequisite gate — cim-graph 0.5.0a1 (SATISFIED)

The refactor depends on two facts about cim-graph 0.5. Both are confirmed in the
local checkout (`/home/ande188/CIM-Graph`, v0.5.0a1):

### 5a. `network.cim` is live, and it is the leaf of a single-resolution chain

The profile is resolved **once, at the connection**, and read downstream — the
0.5 §2/§5 layered-identity contract:

```
ConnectionInterface.__init__   databases/__init__.py:76
    self.cim_profile, self.cim = get_cim_profile()     # the ONLY get_cim_profile() call
        │
        ▼
GraphModel (Feeder/NodeBreaker/DistributedArea/BusBranch).__post_init__
    self.cim = self.connection.cim                     # models/*_model.py
        │
        ▼
builder reads  cim = self.network.cim                  # the rule (ARCHITECTURE.md)
```

`GraphModel` uses `self.cim.__all__` / `getattr(self.cim, ...)` throughout
(`graph_model.py:74–75, 215, 306, 386`). A builder that re-derives via
`get_cim_profile()` would, under a merged profile, get a *different class object*
than `network.cim` and miss every graph key — exactly the failure mode the rule
prevents.

### 5b. The `cgmes_3_0_0` sub-profile parts import, with the EQ/SC split intact

```python
import cimgraph.data_profile.cgmes_3_0_0.core_equipment as EQ   # EQ.ACLineSegment → True
import cimgraph.data_profile.cgmes_3_0_0.short_circuit  as SC   # SC.ACLineSegment → True
```

`ACLineSegment` is defined in both parts: `core_equipment` carries `r/x/bch/gch`
(balanced, → `add_electrical_bal`); `short_circuit` carries `r0/x0/b0ch/g0ch`
(zero-sequence, → `add_short_circuit`). This is the §5a partition the
`PROFILE_TYPING.md` annotations target. Parts available: `core_equipment`,
`short_circuit`, `topology`, `steady_state_hypothesis`, `state_variables`,
`operation`, `equipment_boundary`, `geographical_location`, `diagram`,
`dynamics`.

### 5c. Branch / dependency strategy

The gap is closed at the source; the remaining action is the **Phase 1 pin
bump** (`>=0.3.2a2,<0.4.0` → the 0.5 line). Until the pin lands, develop builders
against the local 0.5.0a1 checkout, where `network.cim` and the `cgmes_3_0_0`
parts already exist. Note that resolving *any* environment currently requires
pre-releases enabled (§1a) — the pin bump should resolve cleanly to 0.5.0a1.

---

## 6. Phase 0 conclusions → adjustments to later phases

- **Phase 1 is now gating, not cosmetic.** The environment does not resolve at
  the current pin; bumping it is what makes `uv run pytest` possible at all.
- **The profile-source edit is "replace a hard module import", not "remove a
  `get_cim_profile()` call".** Update the Phase 3/8 mechanical descriptions
  accordingly — the leaves import `cimhub_2023 as cim` at module scope.
- **`base/new_base_voltage.py` is reused, not ported** — it is a lookup/create
  helper, not an `ObjectBuilder`. (`utils.get_base_voltage` is its caller.)
- Everything else in the roadmap stands.

**No source files were modified in Phase 0.** Next: Phase 1 (rewrite the stale
`CLAUDE.md` API sections, bump the pin).
