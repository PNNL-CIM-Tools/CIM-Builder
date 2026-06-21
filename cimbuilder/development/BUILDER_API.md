# The Unified Builder API

This guide defines the **public, user-facing API** that every CIM-Builder
builder must present. It is the build-side companion to `ARCHITECTURE.md`
(which covers the internal layering) — this doc fixes the *signatures, naming,
and calling convention* a user sees. It is the counterpart to CIMHub's
`CONVERTER_API.md`.

**Target audience:** developers and AI agents building or migrating builders
through the phase roadmap.

---

## Why this exists

The repo had three disagreeing styles at once: standalone object-builder
functions (`new_breaker(network, container, name, node1, node2, ...)`),
class-based substation builders, and a documented-but-absent `*_functions.py`
substation API. A user had to relearn the calling convention per equipment type,
and parameter lists fused every CIM profile into one signature.

This guide standardizes the build layer so:

- A user sees the **same syntax across every equipment type**.
- New builders are **correct-by-construction** — the `ObjectBuilder` contract
  emits the method set.
- The fluent chain mirrors the CIM profile partition and the planned UI wizard.

---

## The contract in one block

```python
from cimbuilder import LineBuilder    # exported from cimbuilder/__init__.py (Phase 9)

line = (
    LineBuilder(network=network, container=feeder)   # 1. construct the builder
        .create(name='Line1')                        # 2. EQ object into the graph
        .add_connectivity(node1='busA', node2='busB')# 3. terminals + node wiring
        .add_electrical_bal(r=0.01, x=0.1, bch=0.0,  # 4. balanced impedance (CIMUnit)
                            r_unit='ohm', x_unit='ohm', bch_unit='S')
        .add_short_circuit(r0=0.03, x0=0.3, b0ch=0.0)# 5. zero-sequence (optional)
        .build()                                     # 6. return the CIM object
)
```

- **Constructor** takes `network` (a `GraphModel`) and `container` (the
  `EquipmentContainer` the equipment belongs to — a `Feeder`, `Line`,
  `Substation`, or `VoltageLevel`). Nothing else is required up front.
- **`create(name)`** constructs the equipment object, seeds its UUID, sets
  `EquipmentContainer = self.container`, adds it to the graph, and stores it on
  `self`. Returns `self`.
- **`add_<profile>(...)`** each populate one profile part on the stored object.
  Return `self`.
- **`build()`** returns the finished CIM object (the `ACLineSegment`, etc.).
  Optional sugar — `self.<obj>` is also accessible — but `build()` is the
  documented terminal call so the chain reads as an expression.

---

## Method naming (fixed)

| Method | Profile part | Populates |
|--------|--------------|-----------|
| `create(name, ...)` | EQ identity | the equipment object itself, container, graph membership |
| `add_connectivity(node1, node2=None, ...)` | connectivity (CN; lives in EQ under CIM17) | `Terminal`s and their `ConnectivityNode` wiring |
| `add_electrical_bal(...)` | electrical (EQ) | **balanced** impedance / ratings (scalar `r`, `x`, `bch`, rated power/voltage) as CIMUnit |
| `add_electrical_unbal(...)` | electrical (unbalanced) | **per-phase** impedance (`ACLineSegmentPhase`, `PerLengthPhaseImpedance`) — stubbed `NotImplementedError` until the CIM18 parts ship |
| `add_short_circuit(...)` | short-circuit (SC) | zero-sequence (`r0`, `x0`, `b0ch`) |
| `add_dynamics(...)` | dynamics (DN) | dynamics-profile fields |
| `add_measurement(...)` | measurement | `Analog` / `Discrete` measurements on terminals |
| `add_asset(...)` | asset (AST) | wire/cable info, asset references |
| `from_catalog(name_or_spec)` | all | populate the above from a catalog entry |

Rules:

- **Builder class names are `<Equipment>Builder`** in PascalCase matching the CIM
  class: `LineBuilder` (ACLineSegment), `BreakerBuilder`, `DisconnectorBuilder`,
  `BusBarSectionBuilder`, `PowerTransformerBuilder`, `CapacitorBuilder`,
  `EnergyConsumerBuilder`, `SynchronousGeneratorBuilder`,
  `PowerElectronicsConnectionBuilder`.
- **Only implement the profile methods the object has.** Unimplemented parts
  inherit the base `raise NotImplementedError` — calling one fails loudly. Do not
  add an empty no-op override.
- **Node arguments accept `str | ConnectivityNode`.** A string is resolved by
  name/aliasName against the graph via `utils.terminal_to_node`. This preserves
  the existing ergonomics.
- **Keyword-first for everything past `name`.** `add_connectivity(node1=...,
  node2=...)`. Positional is allowed for the obvious leading args but the
  examples and the UI generate keyword calls.

---

## Argument grouping = profile boundary

A method's parameters are exactly its profile's fields — never another
profile's. `add_electrical_bal` takes `r/x/bch` (+ unit strings); it must not
take `node1` (connectivity) or `r0` (short-circuit). This is the same boundary
the §5a type narrowing enforces at edit time (`PROFILE_TYPING.md`): a parameter
that doesn't belong to the method's profile is a design smell, not a convenience.

**Balanced vs. unbalanced.** Electrical is split one level further:
`add_electrical_bal` sets the scalar balanced impedance (CGMES `core_equipment`,
implemented now); `add_electrical_unbal` sets the per-phase unbalanced model and
raises `NotImplementedError` until the CIM18 unbalanced profile parts are
official. Same method-boundary discipline, applied to the two electrical
representations — a builder never mixes scalar and per-phase fields in one call.

Unit handling in `add_electrical_bal` follows `UNITS.md`: values are wrapped in
CIMUnit constructors (`cim.Resistance(r, r_unit or 'ohm')`); the per-unit path
is stubbed (`NotImplementedError`) until Phase 11.

---

## `from_catalog`

`from_catalog(name_or_spec)` is the one-call convenience: it looks up a spec
(today via `cimbuilder.utils.catalog_parser`; a catalog DB is a future seam) and
calls the relevant `add_<profile>` methods internally. It returns `self`, so it
composes with explicit overrides:

```python
xfmr = (
    PowerTransformerBuilder(network, substation)
        .create('T1')
        .add_connectivity(node1='busHV', node2='busLV')
        .from_catalog('hv69_12')          # fills electrical from the catalog
        .build()
)
```

`from_catalog` is implemented first on `PowerTransformerBuilder` and
`LineBuilder` (Phase 7), then rolled out where catalog data exists.

---

## Convenience facades (optional)

Casual users and the existing test suite expect a few one-call functions. Where
kept, a facade is a *thin wrapper* over the builder chain, defined next to the
builder and exported from `cimbuilder/__init__.py`:

```python
def new_line(network, container, name, node1, node2, r=None, x=None, **kw):
    b = LineBuilder(network, container).create(name).add_connectivity(node1, node2)
    if r is not None or x is not None:
        b.add_electrical_bal(r=r, x=x, **kw)
    return b.build()
```

A facade must not contain build logic of its own — it only sequences builder
methods. This keeps one source of truth (the builder) and avoids re-fragmenting
into the old function style.

---

## Error behavior (Fail Fast)

- Calling an unimplemented `add_<profile>` → `NotImplementedError` with the
  builder/profile in the message.
- A node string that resolves to nothing → the build leaves the terminal's
  `ConnectivityNode` unset; `add_connectivity` should log a warning (it must not
  silently swallow a typo'd bus name). Prefer surfacing it over a cascading
  fallback.
- A per-unit value before Phase 11 → `NotImplementedError` (see `UNITS.md`),
  never a silent wrong-units write.

---

## Substation assembly API (the other layer)

Substations are **not** `ObjectBuilder`s and do not present this method set.
Their API stays as-is in shape (a class instantiated with `connection` /
`network` / `name` / `base_voltage`, with `new_feeder(...)` / `new_branch(...)`),
but internally they call the builder chains above. See `ARCHITECTURE.md` →
"Substation assembly layer". Their public surface is documented with the
substation classes, not here.

---

## Related documents

- `ARCHITECTURE.md` — the layering and `ObjectBuilder` / `builder_base` contract.
- `PROFILE_TYPING.md` — how each `add_<profile>` signature is typed (§5a).
- `UNITS.md` — CIMUnit handling inside `add_electrical_bal`.
- `BUILDER_TEST_CREATION.md` — testing a builder against atom factories.
