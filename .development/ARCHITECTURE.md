# CIM-Builder — Target Architecture

**Date:** 2026-04-30
**Status:** Phase 0 (scaffolding) — in progress
**Companion docs:**
- `STYLE_GUIDE.md` — coding rules and canonical signatures
- `PHASE_CHECKPOINT.md` — live status per phase
- `PHASE_0.md`–`PHASE_8.md` — per-phase scope and exit criteria
- Source plan: `/home/ande188/.claude/plans/i-am-the-maintainer-fizzy-blossom.md`

This document describes the **target** architecture — what CIM-Builder becomes after the rewrite. For the phased path to get there, see `PHASE_CHECKPOINT.md` and the per-phase docs.

---

## 1. Product Definition

**CIM-Builder is a Python library for programmatically constructing CIM (Common Information Model) power-system network models from scratch.**

Unlike other CIM tooling that requires a source file (OpenDSS, PSSE, GIS export), CIM-Builder builds CIM directly through function calls. Its primary outputs are CIM object graphs managed by `cim-graph`, serializable to XML/JSON-LD or uploadable to CIM databases.

CIM-Builder serves three audiences:

1. **Python scripts and notebooks** — engineers building or modifying grid models procedurally.
2. **MCP servers** — AI agents invoking network construction operations as tools. Every public function must be discoverable, typed, and JSON-schema-able.
3. **GUIs** (CIMantic Studio Phase 5-6) — buttons that call the same functions that scripts call. No duplicate logic.

### Non-goals (explicitly excluded)

- **Native-format import** (OpenDSS, PSSE, etc.) — handled by `cimhub_*` sub-packages in cim-graph ecosystem
- **Power flow / simulation** — solvers are downstream consumers
- **CIM profile design** — CIM-Builder consumes profiles from cim-graph; it does not extend them
- **Catalog data / content** — equipment catalog contents (transformer specs, conductor specs, NERC DER defaults) live in `cim-asset-manager`; CIM-Builder consumes Pydantic catalog models

---

## 2. Four-Layer API Structure

Each layer has a distinct audience and contract.

| Layer | Module | Audience | What it builds |
|---|---|---|---|
| **1. Primitives** | `object_builder/` | Catalog-driven construction, MCP | One CIM class (e.g., `Breaker`, `LinearShuntCompensator`) |
| **2. Composites** | `composite_builder/` | Scripts, MCP | Chains of CIM objects that belong together (e.g., tap-changing transformer = PwrXfmr + 2 PwrXfmrEnd + 2 Terminal + RatioTapChanger + TapChangerControl) |
| **3. Topology patterns** | `topology_builder/` | Substation construction, MCP | Substation bay arrangements (single bus, breaker-and-a-half, etc.) as free functions |
| **4. Sessions** | `session/` | Notebooks, GUI | Ergonomic context objects that hold `network + substation + base_voltage` and delegate to lower layers |

**Key property:** every layer below 4 exposes free functions. Sessions are sugar; they never do work the functions can't do.

### Directory layout

```
cimbuilder/
├── __init__.py              # Public API re-exports
├── _profile.py              # get_cim() helper with TYPE_CHECKING imports
├── templates/               # Pydantic catalog shims (→ cim-asset-manager later)
├── object_builder/          # Layer 1: primitives
├── composite_builder/       # Layer 2: multi-object chains
├── topology_builder/        # Layer 3: substation bay arrangements (renamed from substation_builder/)
├── session/                 # Layer 4: ergonomic wrappers
├── utils/                   # terminal_to_node, get_or_create_base_voltage, etc.
├── _deprecated/             # Back-compat shims (Phases 5-7, deleted Phase 7)
└── tests/                   # Layer-aligned test subdirs
```

---

## 3. Core Design Rules

### 3.1 Function signatures

Canonical form (see `STYLE_GUIDE.md` for the full spec):

```python
def new_linear_shunt_compensator(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: str | "cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    b_Mvar: float | None = None,
    g_MW: float | None = None,
    section_number: int = 1,
    template: "LinearShuntCompensatorCatalog | None" = None,
) -> "cim.LinearShuntCompensator":
    ...
```

- Positional: `network, container, name, <topology>` — in that order, for every builder
- Everything else keyword-only (`*`)
- `base_voltage` first after `*`, `template` last
- Units in parameter names (`b_Mvar`, `length_km`, `ratedS_MVA`) — converted via `CIMUnit` internally
- No `**kwargs` in public API (breaks MCP schema introspection and GUI form generation)
- Type hints are string-form (`"cim.Breaker"`) to stay compatible with runtime profile switching

### 3.2 CIM profile access

Runtime profile lookup uses `cimbuilder._profile.get_cim()`:

```python
from cimbuilder._profile import get_cim

def new_breaker(network, container, name, node1, node2, ...):
    cim = get_cim()
    breaker = cim.Breaker(name=name)
    ...
```

Type hints use the `TYPE_CHECKING` guard — the import is invisible at runtime:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2023 as cim
```

Profile-scoped builders (dynamics, split-profile distribution — Phase 8+) import their own profile module under `TYPE_CHECKING`, e.g. `cimgraph.data_profile.cim17v40.dynamics`.

### 3.3 Units

Per CLAUDE.md: never manually multiply/divide by `1e3`, `1e6`. Always use `CIMUnit` constructor:

```python
# BAD
load.p = total_load_kw * 1000

# GOOD
load.p = cim.ActivePower(total_load_kw, 'kW')
```

Comparisons and arithmetic on CIMUnit values use `.to('<unit>')` or `float(x)`.

### 3.4 Templates (catalog integration)

Builders that can be catalog-driven accept a `template: CatalogEntry` parameter (Pydantic model). Precedence rule:

1. Explicit kwargs win
2. Template values fill remaining `None` kwargs
3. Type-level defaults fill what remains

Templates live in `cimbuilder/templates/` (Pydantic shims) until `cim-asset-manager` ships, then the import path changes — no other code changes.

### 3.5 What MCP sees

Every function in `cimbuilder/__init__.py`'s re-export list is an MCP tool candidate. The MCP server repo (separate) generates tool schemas via `inspect.signature()`. This is why:

- No `**kwargs`
- All types explicit
- Docstrings are user-facing (LLM reads them as tool descriptions)

---

## 4. Build State & Persistence

CIM-Builder does not own persistence. All builders:

- Take a `GraphModel` argument (or the session holds one)
- Call `network.add_to_graph(obj)` for every created object
- Do NOT call `network.upload()` — that's the caller's choice

Sessions expose `.write_xml(path)`, `.write_json_ld(path)`, `.upload()` as parity passthroughs.

---

## 5. Backward Compatibility

Old class-based API (`SingleBusSubstation`, `DoubleBusSingleBreakerSubstation`, etc.) becomes thin `DeprecationWarning` shims in `cimbuilder/_deprecated/` for one release. Deleted in Phase 7.

Shim contract: calling `SingleBusSubstation(connection, name, base_voltage)` is equivalent to `SubstationSession.single_bus(connection, name, base_voltage)` — same CIM output, warning only.

---

## 6. Dependencies

Current pinning (Phase 0):
- `cim-graph>=0.4.3a10` — the CIM object graph layer
- `pydantic>=2.0` (NEW in Phase 0) — for template shims

Future (Phase 6+):
- `cim-asset-manager` — replaces `cimbuilder/templates/` shims with the real package

Development:
- `pytest>=8.3.5`
- `pre-commit>=2.17.0`

---

## 7. What cim-graph features are we coupled to?

- `GraphModel`, `DistributedArea`, `FeederModel`, `NodeBreakerModel` — runtime container
- `ConnectionInterface` subclasses (`XMLFile`, etc.) — persistence adapters
- `cimgraph.databases.get_cim_profile()` — profile registry
- `cimgraph.utils.write_xml`, `write_json_ld` — serialization
- `cimgraph.data_profile.identity.Identity` — base class of every CIM dataclass
- `cimgraph.data_profile.units.CIMUnit` subclasses — unit-aware quantities

Split-profile support (Phase 9) additionally uses `cimgraph.data_profile.merge.merge_profiles` + `generate_type_stubs` to handle CIM18GMDM-style split `connectivity`/`electrical` profiles.

---

## 8. Cross-repo coordination

CIM-Builder sits in a family:

| Repo | Role | Coupling |
|---|---|---|
| `cim-graph` | CIM profile + graph model runtime | Hard dependency |
| `cim-asset-manager` (forthcoming) | Catalog data + Pydantic models + ingestion pipelines | Hard dependency (Phase 6+); internal shims meanwhile |
| `CIMantic-Studio` | GUI viewer & editor | Consumes CIM-Builder in Phase 5-6 of its own roadmap |
| `cim-builder-mcp` (forthcoming separate repo) | MCP server exposing CIM-Builder's public functions as tools | Consumes CIM-Builder |

CIM-Builder makes no assumptions about which of these consumers are present.
