# CIM-Builder Builder Architecture

**Status:** revised to match the shipped reference implementation. Everything
below describing a fluent/chainable API, a `builder_base` mixin, or
`cgmes_3_0_0`/`cimhub_2023` as the target profile was the pre-implementation
sketch and is now wrong — see the revision note.

> **Revision note.** `cimbuilder/builders/load/consumer.py`
> (`EnergyConsumerBuilder`) is the real, shipped reference implementation, not
> `LineBuilder`'s old sketch (`object_builder/line/line_builder.py`, itself
> unfinished and never completed). The actual `ObjectBuilder` (`builders/base.py`)
> is **stateless**: `add_<profile>` methods take the object being built as an
> explicit first parameter and return `None` — there is no method chaining, no
> `builder_base` mixin, and no `self.line`/`self.obj` instance state. The real
> profile module family is `cimprofiles.cim18.cim18v17.*` (e.g.
> `connectivity_unbalanced`, `electrical_unbalanced`, `steady_state_hypothesis`),
> not `cgmes_3_0_0`/`cim18gmdm`/`cimhub_2023`. This document is rewritten to
> describe that shape; see `GRAPH_WRITE_CONTRACT.md` §7 for the contract this
> was reconciled against, and `OBJECT_BUILDER_MIGRATION.md` for the phased plan
> that ports `object_builder/`'s old `new_*` functions onto it.

This document defines the standard architecture CIM-Builder's equipment
builders follow. **`EnergyConsumerBuilder`** (`builders/load/consumer.py`) is
the reference implementation. It is the build-side counterpart to CIMHub's own
architecture docs (which define the converter pipeline); CIM-Builder *grows*
CIM graphs rather than converting between formats.

---

## The core idea: build one profile-part at a time

A CIM object is not one flat record — it is the union of fields contributed by
several **profile parts**: connectivity, electrical (impedance / ratings),
steady-state hypothesis, short-circuit (zero-sequence), dynamics, measurement,
asset. A merged profile module (`network.cim`) carries all of these fields on
one class; the real, part-scoped modules (`cimprofiles.cim18.cim18v17.*`) split
them back out.

The wrong move (tried and reverted — `git log` `5b47fd6`) was to re-describe each
object with bespoke functions whose parameter lists fused every profile
together. The **eureka** is to mirror the profile partition in the builder: one
method per profile part, populating *only* that part's fields, called
separately by the caller — see `EnergyConsumerBuilder.add_connectivity` /
`.add_electrical` / `.add_ssh` in `consumer.py`. This:

- matches how CIM is actually split for serialization (connectivity + SSH + TP +
  meas + asset), so a builder maps 1:1 onto an export-part boundary;
- gives each method a real, part-scoped reference module to check writes
  against (`graph_write.set_attr(load, EL, 'pfixed', ...)` — `EL` is
  `cim18v17.electrical_unbalanced`, not the merged `network.cim`), turning a
  category error (writing a short-circuit field inside `add_electrical`) into
  a runtime `ValueError` from `graph_write.set_attr`/`set_assc` (see
  `GRAPH_WRITE_CONTRACT.md` §2) rather than a silent no-op.

---

## Layered flow

```
User / UI wizard / substation assembly / cimtables.load()
        │  constructs a builder, calls builder.create(),
        │  then builder.add_<profile>(obj, ...) per part, passing obj explicitly
        ▼
ObjectBuilder subclass            (EnergyConsumerBuilder, …)
   create(*, name) -> obj                              (base.py, concrete)
   add_connectivity(obj, ...) -> None                   (per-subclass, stateless)
   add_electrical(obj, ...) -> None
   add_ssh(obj, ...) -> None
        │  each method imports its own part module at top level (CN, EL, SSH, ...)
        │  and calls graph_write.set_attr/set_assc(obj, <part module>, attr, value)
        ▼
cimtables.graph_write / cimtables.connectivity   (the only code that mutates obj or network)
        │  set_attr/set_assc check attr against <part module>'s same-named class
        ▼
GraphModel  (network.graph, keyed by the network's own class identity)
        │  network.cim — the single source of profile identity
        ▼
cimgraph profile module            (the merged network.cim; part modules come
                                     from cimprofiles.cim18.cim18v17.*)
```

Three contracts hold at every layer:

1. **Profile identity flows down, never re-derived.** The `GraphModel` carries
   `network.cim`; `create()` reads it once in `__init__` (`self.cim =
   network.cim`). No builder method calls `get_cim_profile()`. This keeps graph
   keys and `isinstance` consistent under a merged profile — `get_cim_profile()`
   and `network.cim` are not guaranteed to be the same object otherwise. See
   `PROFILE_RESOLUTION.md`.
2. **Mechanics live in `cimtables`, not in a builder mixin.** Terminal/node
   wiring (`cimtables.connectivity.add_connectivity`), attribute/association
   writes (`cimtables.graph_write.set_attr`/`set_assc`), and `add_to_graph` are
   all in the `cimtables` package (split out of this repo — see
   `CIMTBL_DESIGN.md` §8.1), not a `cimbuilder`-local mixin. A builder method's
   own body is just: resolve any by-name FKs, call `graph_write.set_attr`/
   `set_assc`/`connectivity.add_connectivity` with its own part module.
3. **Substations are a separate assembly layer.** They orchestrate object
   builders to lay out a topology; they are *not* themselves `ObjectBuilder`s. A
   substation is not one profile-built object, so it has no `add_<profile>`
   methods.

---

## Module map (current + target)

```
cimbuilder/
  builders/
    base.py                  # ObjectBuilder: __init__, create, from_table, add — concrete, no ABC
    load/consumer.py          # EnergyConsumerBuilder(ObjectBuilder) — reference implementation
    <category>/<name>.py      # one module per equipment category, ported from object_builder/
                               # (see OBJECT_BUILDER_MIGRATION.md for the phased port plan)
  object_builder/             # pre-port: old new_<equipment>(network, container, name, ...)
                               # factory functions, being replaced category by category
  substation_builder/         # assembly layer: SingleBusSubstation, MainAndTransferSubstation, …
  utils/                      # terminal_to_node, get_base_voltage, get_source_bus, catalog_parser
  development/                # this doc set
  __init__.py                 # THE single user-facing import surface
```

`cimtables` (split out to `/home/ande188/CIM-Tables`, see `CIMTBL_DESIGN.md`
§8.1) provides `graph_write`, `connectivity`, `binder.bind_row`, and the
`.cimtbl` DSL itself — none of that lives in `cimbuilder` any more.

---

## The `ObjectBuilder` contract

`builders/base.py` defines the concrete base class. Every equipment builder
subclasses it:

```python
class ObjectBuilder:
    def __init__(self, network: GraphModel, container: object = None):
        self.network = network
        self.container = container
        self.cim = network.cim

    def create(self, *, name: str) -> object:
        """Bare cim_cls(name=name) — no UUID seeding, no container, no
        add_to_graph. Subclasses override only if construction needs more."""
        return getattr(self.cim, self.cim_class_name)(name=name)

    def from_table(self, row: object) -> object:
        """Generic .cimtbl row -> live object, via cimtables.binder.bind_row.
        No per-class dispatch table; see CIMTBL_DESIGN.md §4.2."""
        return bind_row(self.network, row, obj=self.create(name=row.name), container=self.container)

    def add(self, obj: object) -> object:
        graph_write.add_to_graph(self.network, obj)
        return obj
```

There are no abstract `add_<profile>` methods on the base class at all — a
subclass simply defines whichever `add_<profile>(self, obj, *, ...)` methods
its equipment type's profile actually has fields for (see
`EnergyConsumerBuilder`'s `add_connectivity`/`add_electrical`/`add_ssh` below).
Calling a method that doesn't exist on a given subclass is a plain
`AttributeError` — there's no `NotImplementedError` stub layer to maintain.

**Every `add_<profile>` method is stateless and returns `None`.** The object
being built is passed in explicitly as the first parameter; nothing is chained
off a builder instance, and the builder itself holds only `network`,
`container`, and `cim`:

```python
builder = EnergyConsumerBuilder(network, container=feeder)
load = builder.create(name='load_671')
builder.add_connectivity(load, node='671', BaseVoltage='base_4160')
builder.add_electrical(load, pfixed=10_000, qfixed=3_000)
builder.add_ssh(load, p=10_000, q=3_000)
consumer = builder.add(load)
```

This is deliberate, not a simplification of a chained design: an association
(`BaseVoltage`, `LoadResponse`) belongs to whichever profile part actually
owns that field, resolved and written inside that part's own `add_<profile>`
method — there is no separate `add_references`/`add_assc`-style method, because
associations are not a thing apart from the profile part that declares them.

---

## Where the mechanics actually live

There is no `cimbuilder`-local mixin. Terminal/node wiring and attribute/
association writes are `cimtables` functions, called directly from each
`add_<profile>` method:

| Call | Replaces today's | Behavior |
|------|------------------|----------|
| `self.cim` | `cim_profile, cim_module = get_cim_profile()` | set once in `__init__` from `network.cim` — the one identity source |
| `connectivity.add_connectivity(network, obj, node_cols=..., container=...)` | the hand-rolled `cim.Terminal(...)` + `utils.terminal_to_node(...)` blocks (inconsistent across the old `new_*` functions — see `OBJECT_BUILDER_MIGRATION.md`) | builds terminal(s), wires them to the named/object node(s), sets `EquipmentContainer` |
| `graph_write.set_attr(obj, <part module>, attr, value)` | direct `setattr(obj, attr, value)` | checks `attr` is a real, non-association field of `<part module>`'s same-named class before writing; raises otherwise |
| `graph_write.set_assc(obj, <part module>, assc, target)` | direct `setattr(obj, assc, target)` on both sides, by hand | writes both sides of the association from the part module's own `metadata['inverse']`, so the graph is never one-sided |
| `graph_write.add_to_graph(network, obj)` | `network.add_to_graph(obj)` | adds to the graph and the network's `NameIndex` together |

Porting an old `new_*` function onto these fixes its inconsistencies by
construction — e.g. `switch/new_disconnector.py` seeds `t1.uuid(...)` twice and
never seeds `t2`; `topology/new_bus_bar_section.py` hand-builds its terminal.
Going through `connectivity.add_connectivity` for every builder removes that
drift instead of reproducing it per equipment type.

---

## Profile-source rule

`__init__` reads `self.cim = network.cim` once; builder methods use `self.cim`
for resolving FK target classes and constructing objects
(`getattr(self.cim, cls_name)(...)`), never `get_cim_profile()`. The model
already carries the authoritative merged profile object — re-deriving from the
env var is the source of a silent class-identity mismatch: under a merged
profile, `get_cim_profile()` and `network.cim` can be different class objects,
and `network.graph[get_cim_profile().X]` misses every time. Reading
`network.cim` is correct on flat and merged profiles alike. See
`PROFILE_RESOLUTION.md` for the full three-layer picture (this is Layer 3).

A builder's `add_<profile>` methods additionally import their own **part**
module at the top of the file (e.g. `cimprofiles.cim18.cim18v17.
electrical_unbalanced as EL`) and pass it as the `part` argument to
`graph_write.set_attr`/`set_assc` — that's a separate, stronger check (Layer 2)
than `self.cim`, and is what actually catches a field written on the wrong
profile part. See `GRAPH_WRITE_CONTRACT.md` §2.

---

## Substation assembly layer

`substation_builder/*` stays class-based (`@dataclass`, today inheriting
`SubstationBuilder(ABC)` with `new_branch` / `new_feeder`). As builder classes
land for the equipment it calls (`BreakerBuilder`, `DisconnectorBuilder`,
`BusbarSectionBuilder`, …), it *orchestrates* them instead of the old `new_*`
functions:

```python
# inside SingleBusSubstation.new_feeder(...)
builder = BreakerBuilder(self.network, self.substation)
breaker = builder.create(name=f'{self.substation.name}_{breaker_number}')
builder.add_connectivity(breaker, node1=junction1, node2=junction2)
```

It also reads `self.network.cim` (today it calls `get_cim_profile()` in
`__post_init__`). It deliberately has no `add_<profile>` methods — a substation is
a *composition of many objects*, which is a different shape from a single
profile-built object. Keeping the two layers distinct is a locked decision.

---

## Why this is correct-by-construction

- A new equipment type is a small, stateless subclass: an `add_connectivity`
  taking the object plus whichever by-name FKs it has, and one `add_<profile>`
  per other part the object actually has fields for. Mechanics come free from
  `cimtables.graph_write`/`connectivity`; identity comes free from `self.cim`.
- The same `add_<profile>` boundary serves the direct/manual API, the generic
  `.cimtbl` loader (`from_table`/`bind_row`, which needs zero per-class
  dispatch — see `CIMTBL_DESIGN.md` §4.2), and the export-part split, so there
  is one structure to keep right, not several.
- Failures are loud: `graph_write.set_attr`/`set_assc` raise `ValueError` on a
  field that isn't a real, correctly-kinded field of the part module passed in;
  an unresolved by-name FK raises in the calling `add_<profile>` method itself.

---

## Related documents

- `GRAPH_WRITE_CONTRACT.md` — the full `graph_write`/`set_attr`/`set_assc`
  contract this architecture is built on, including §7's `ObjectBuilder` shape.
- `PROFILE_RESOLUTION.md` — the three profile mechanisms (edit-time typing,
  runtime `set_attr`/`set_assc` checking, `Profile=`/`network.cim` selection)
  and how they compose.
- `CIMTBL_DESIGN.md` — the `.cimtbl` DSL this builder shape underlies
  (`bind_row`, now in the separate `cimtables` package).
- `OBJECT_BUILDER_MIGRATION.md` — the phased plan porting `object_builder/`'s
  old `new_*` functions onto this shape.
- `UNITS.md` — CIMUnit construction/conversion rules for `add_<profile>`
  methods that set physical quantities.
