# CIM-Builder Builder Architecture

This document defines the standard architecture that all CIM-Builder builders
must follow after the uniform-API refactor. **`LineBuilder`** is the reference
implementation. It is the build-side counterpart to CIMHub's `ARCHITECTURE.md`
(which defines the converter pipeline); CIM-Builder *grows* CIM graphs rather
than converting between formats.

See the phase roadmap in
`/home/ande188/.claude/plans/take-a-look-at-buzzing-crane.md` for the day-by-day
sequence that brings the repo to this target state.

---

## The core idea: build one profile-part at a time

A CIM object is not one flat record — it is the union of fields contributed by
several **profile parts**: connectivity (EQ topology), electrical (impedance /
ratings), short-circuit (zero-sequence), dynamics, measurement, asset. The
CIMTool-generated dataclasses already carry all of these fields on one class.

The wrong move (tried and reverted — `git log` `5b47fd6`) was to re-describe each
object with bespoke functions whose parameter lists fused every profile
together. The **eureka** is to mirror the profile partition in the builder: one
method per profile part, populating *only* that part's fields, called in
sequence. This:

- matches how CIM is actually split for serialization (EQ + SSH + TP + meas +
  asset), so a builder maps 1:1 onto an export-part boundary;
- maps 1:1 onto the planned UI wizard (one page per profile — Connectivity →
  Electrical → Short-circuit → …);
- lets the type system *scope writes to one profile per method* (see
  `PROFILE_TYPING.md`), turning a category error (`line.r` set during
  connectivity) into an edit-time flag.

---

## Layered flow

```
User / UI wizard / substation assembly
        │  instantiates a builder, calls add_<profile> in sequence
        ▼
ObjectBuilder subclass            (LineBuilder, BreakerBuilder, …)
   create() → add_connectivity() → add_electrical() → add_short_circuit() → …
        │  each method reads cim = self.network.cim  (NOT get_cim_profile())
        ▼
builder_base mixin                 (shared mechanics: terminals, node wiring, graph add)
        │  _cim / _new_terminal / _connect_node / _add
        ▼
GraphModel  (network.graph, keyed by the network's own class identity)
        │  network.cim — the single source of profile identity (cim-graph 0.5 §2)
        ▼
cimgraph profile module            (cimhub_2023 today; cim18gmdm merge under 0.5)
```

Three contracts hold at every layer:

1. **Profile identity flows down, never re-derived.** The `GraphModel` carries
   `network.cim`; every builder reads it. No builder calls `get_cim_profile()`.
   This is cim-graph 0.5 §5; it makes graph keys and `isinstance` agree under a
   merged profile (0.5 §1 Failure 1).
2. **Mechanics live in one place.** Terminal creation, `ConnectivityNode`
   wiring, deterministic UUID seeding, and `add_to_graph` are in
   `builder_base`, not copy-pasted into every builder (the current fragmentation).
3. **Substations are a separate assembly layer.** They orchestrate object
   builders to lay out a topology; they are *not* themselves `ObjectBuilder`s. A
   substation is not one EQ+SSH+TP object, so it has no `add_<profile>` methods.

---

## Module map (target)

```
cimbuilder/
  object_builder/
    object_builder.py        # ObjectBuilder(ABC): the create + add_<profile> contract
    builder_base.py          # shared mixin: _cim, _new_terminal, _connect_node, _add, uuid seeding
    line/line_builder.py     # LineBuilder(ObjectBuilder) — reference implementation
    topology/                # BusBarSectionBuilder
    shunt/                   # BreakerBuilder, CapacitorBuilder
    switch/                  # DisconnectorBuilder
    transformer/             # PowerTransformerBuilder (+ tap changer)
    load/ generator/ inverter/ measurement/ protection/   # remaining equipment
    generic/                 # GenericOneTerminalBuilder / GenericTwoTerminalBuilder
    base/                    # new_base_voltage (BaseVoltage lookup/create)
    __init__.py              # exports builder classes
  substation_builder/        # assembly layer: SingleBusSubstation, MainAndTransferSubstation, …
  utils/                     # terminal_to_node, get_base_voltage, get_source_bus, catalog_parser
  units/                     # Phase 11: per-unit (z_base) conversion engine
  development/               # this doc set + the test-creation strategy
  __init__.py                # THE single user-facing import surface
```

---

## The `ObjectBuilder` contract

`object_builder/object_builder.py` defines the abstract contract. Every
equipment builder subclasses it.

```python
@dataclass
class ObjectBuilder(ABC):
    network: GraphModel
    container: "EquipmentContainer"

    @abstractmethod
    def create(self, name: str): ...          # construct EQ object, set container, add to graph, return self

    @abstractmethod
    def add_connectivity(self, *nodes): ...    # terminals + ConnectivityNode wiring, return self

    # Optional profile parts — default to NotImplementedError, override where the
    # object actually has that profile's fields:
    def add_electrical(self, *a, **k): raise NotImplementedError
    def add_short_circuit(self, *a, **k): raise NotImplementedError
    def add_dynamics(self, *a, **k): raise NotImplementedError
    def from_catalog(self, name_or_spec): raise NotImplementedError
```

**Why `create` + `add_connectivity` are abstract and the rest are not.** Every
piece of conducting equipment exists in the graph (`create`) and connects to
nodes (`add_connectivity`). Not every device has electrical impedance,
zero-sequence data, or dynamics. A `Disconnector` implements only `create` +
`add_connectivity`; a `ConcentricNeutralCableInfo`-bearing line implements
electrical + short-circuit + asset. Calling an unimplemented part raises loudly
(Fail Fast) rather than silently doing nothing.

**Every method returns `self`** so a build reads as a chain that mirrors the
profile sequence:

```python
LineBuilder(network=net, container=feeder) \
    .create('Line1') \
    .add_connectivity(node1='busA', node2='busB') \
    .add_electrical(r=0.01, x=0.1, bch=0.0, r_unit='ohm', x_unit='ohm', bch_unit='S')
```

---

## The `builder_base` mixin

`object_builder/builder_base.py` holds the mechanics extracted from today's
standalone functions, so no builder reimplements them:

| Helper | Replaces today's | Behavior |
|--------|------------------|----------|
| `self._cim` | `cim_profile, cim_module = get_cim_profile()` | returns `self.network.cim` — the one identity source |
| `self._new_terminal(eq, seq, name)` | the hand-rolled `cim.Terminal(...)` blocks (inconsistent across builders) | builds a terminal, seeds its UUID deterministically, sets `sequenceNumber` + `ConductingEquipment`, appends to `eq.Terminals` |
| `self._connect_node(terminal, node)` | direct `utils.terminal_to_node(...)` calls | wraps `cimbuilder.utils.terminal_to_node` (accepts a node object or a name string) |
| `self._add(obj)` | `network.add_to_graph(obj)` | adds to the graph; one call site to audit |

This consolidation also fixes the inconsistencies the current code carries — e.g.
`switch/new_disconnector.py` seeds `t1.uuid(...)` twice and never seeds `t2`;
`topology/new_bus_bar_section.py` hand-builds its terminal. Porting onto
`builder_base` removes those by construction.

---

## Profile-source rule (the 0.5 contract)

Every builder method begins:

```python
cim = self.network.cim     # or: cim = self._cim
```

It does **not** call `get_cim_profile()`. The model already carries the
authoritative profile object (cim-graph 0.5 §2: connection chooses it, model
reads it from the connection, leaf reads it from the model). Re-deriving from the
env var is the source of the silent class-identity mismatch the 0.5 plan
eliminates — under a merged profile, `get_cim_profile()` and `network.cim` can be
different class objects, and `network.graph[get_cim_profile().X]` misses every
time. Reading `network.cim` is correct on flat and merged profiles alike.

Genuinely model-less constructors (none expected among the builders) would keep
`get_cim_profile()` — but a builder always receives a `GraphModel`, so the rule
is unconditional here.

---

## Substation assembly layer

`substation_builder/*` stays class-based (`@dataclass`, today inheriting
`SubstationBuilder(ABC)` with `new_branch` / `new_feeder`). After the refactor it
*orchestrates* object builders instead of calling the old `new_*` functions:

```python
# inside SingleBusSubstation.new_feeder(...)
BreakerBuilder(self.network, self.substation) \
    .create(f'{self.substation.name}_{breaker_number}') \
    .add_connectivity(node1=junction1, node2=junction2)
```

It also reads `self.network.cim` (today it calls `get_cim_profile()` in
`__post_init__`). It deliberately has no `add_<profile>` methods — a substation is
a *composition of many objects*, which is a different shape from a single
profile-built object. Keeping the two layers distinct is a locked decision.

---

## Why this is correct-by-construction

- A new equipment type is a small subclass: implement `create` +
  `add_connectivity`, plus whichever profile parts the object actually has.
  Mechanics come free from `builder_base`; identity comes free from
  `network.cim`; typing scope comes free from the §5a annotations.
- The same `add_<profile>` boundary serves three consumers at once — the chained
  API, the export-part split, and the UI wizard pages — so there is one structure
  to keep right, not three.
- Failures are loud: an unimplemented profile part raises; a wrong-identity graph
  key would fail the identity assertion in the test suite
  (`BUILDER_TEST_CREATION.md`).

---

## Related documents

- `BUILDER_API.md` — the public method signatures and naming the contract above
  must present to users.
- `PROFILE_TYPING.md` — how `add_<profile>` methods are typed (§5a).
- `UNITS.md` — how `add_electrical` handles CIMUnit values and the deferred
  per-unit engine.
- `BUILDER_TEST_CREATION.md` — how to test a builder (atom factories + chained
  asserts).
- cim-graph 0.5 contract:
  `/home/ande188/CIM-Graph/docs/development/PROFILE_IDENTITY_0_5_PLAN.md`.
