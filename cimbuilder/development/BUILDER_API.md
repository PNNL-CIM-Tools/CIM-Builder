# The Unified Builder API

**Status:** revised to match the shipped reference implementation
(`cimbuilder/builders/load/consumer.py`). The fluent/chained contract this doc
originally specified was the pre-implementation sketch and was never built
that way — see the revision note.

> **Revision note.** The real `ObjectBuilder` (`builders/base.py`) and its
> first subclass, `EnergyConsumerBuilder` (`builders/load/consumer.py`), are
> **stateless**: `add_<profile>` methods take the object as an explicit first
> parameter and return `None`. There is no `line1.add_connectivity(...)`
> method-on-the-created-object chaining, no `add_electrical_bal`/
> `add_short_circuit` naming (the real split is `add_electrical`/`add_ssh`,
> following the object's actual profile parts), and no `NotImplementedError`
> stub layer — a builder subclass simply doesn't define a method for a profile
> part its equipment type doesn't have. See `ARCHITECTURE.md` for the full
> contract and `GRAPH_WRITE_CONTRACT.md` §7 for why this shape was chosen over
> the chain.

This guide defines the **public, user-facing API** that every CIM-Builder
builder presents. It is the build-side companion to `ARCHITECTURE.md` (which
covers the internal layering) — this doc fixes the *signatures, naming, and
calling convention* a user sees.

**Target audience:** developers and AI agents porting `object_builder/`'s old
`new_*` functions onto this shape — see `OBJECT_BUILDER_MIGRATION.md` for the
phased plan.

---

## Why this exists

The repo had disagreeing styles at once: standalone object-builder functions
(`new_breaker(network, container, name, node1, node2, ...)`), class-based
substation builders, and a documented-but-absent `*_functions.py` substation
API. A user had to relearn the calling convention per equipment type, and
parameter lists fused every CIM profile into one signature.

This guide standardizes the build layer so:

- A user sees the **same syntax across every equipment type**: construct the
  builder, call `create()`, then call each `add_<profile>(obj, ...)` the
  equipment type actually has, passing the object back in each time.
- New builders are **correct-by-construction** — each `add_<profile>` method
  checks its writes against that profile part's own real module
  (`graph_write.set_attr`/`set_assc`), so a field written on the wrong part
  raises instead of silently landing somewhere unintended.
- The method-per-part boundary mirrors the CIM profile partition (how CIM is
  actually split for serialization), not a UI-chain convenience.

---

## The contract in one block

```python
from cimbuilder.builders.load.consumer import EnergyConsumerBuilder

builder = EnergyConsumerBuilder(network, container=feeder)     # 1. construct the builder
load = builder.create(name='load_671')                          # 2. bare object, not yet in the graph
builder.add_connectivity(load, node='671', BaseVoltage='base_4160')  # 3. terminals + node wiring + by-name FK
builder.add_electrical(load, pfixed=10_000, qfixed=3_000)        # 4. electrical profile part
builder.add_ssh(load, p=10_000, q=3_000)                         # 5. steady-state hypothesis part
consumer = builder.add(load)                                     # 6. add_to_graph, returns the object
```

Each `add_<profile>` call takes the object back as its first argument and
returns `None` — there is nothing to chain, because the object itself (not the
builder) is what every later call and the caller's own code needs. A
particular equipment type only defines the `add_<profile>` methods its profile
actually has fields for (a `Disconnector` builder, for instance, would have no
`add_electrical` at all).

---

## Error behavior (Fail Fast)

- Calling an `add_<profile>` a given subclass doesn't define → plain
  `AttributeError` (there is no stub/`NotImplementedError` layer to maintain).
- Writing a field through the wrong part module, or a field that doesn't exist
  at all → `ValueError` from `graph_write.set_attr`/`set_assc`, naming the part
  module, class, and attribute (`GRAPH_WRITE_CONTRACT.md` §2).
- A by-name FK (`BaseVoltage='base_4160'`) that doesn't resolve → `ValueError`
  raised by the `add_<profile>` method itself (see `consumer.py`'s
  `graph_write.resolve` calls) — never a silent `None`/no-op write.

---

## Substation assembly API (the other layer)

Substations are **not** `ObjectBuilder`s and do not present this method set.
Their API stays as-is in shape (a class instantiated with `connection` /
`network` / `name` / `base_voltage`, with `new_feeder(...)` / `new_branch(...)`),
but internally they call `builder.create()` / `builder.add_<profile>(obj, ...)`
on the equipment builders above. See `ARCHITECTURE.md` → "Substation assembly
layer". Their public surface is documented with the substation classes, not
here.

---

## Related documents

- `ARCHITECTURE.md` — the full layering and `ObjectBuilder` contract.
- `GRAPH_WRITE_CONTRACT.md` — the `set_attr`/`set_assc` contract every
  `add_<profile>` method writes through.
- `UNITS.md` — CIMUnit handling inside an `add_<profile>` method.
- `OBJECT_BUILDER_MIGRATION.md` — the phased plan porting `object_builder/`
  onto this API.
