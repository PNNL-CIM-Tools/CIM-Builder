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

builder = LineBuilder(network=network, container=feeder)   # 1. construct the builder

line1 = builder.create(name='Line1')                        # 2. object into the graph
line1.add_connectivity(node1='busA', node2='busB')# 3. terminals + node wiring
line1.add_electrical_bal(r=0.01, x=0.1, bch=0.0,  # 4. balanced impedance (CIMUnit)
                            r_unit='ohm', x_unit='ohm', bch_unit='S')
line1.add_short_circuit(r0=0.03, x0=0.3, b0ch=0.0)# 5. zero-sequence (optional)

```

---

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
