# Profile-Scoped Typing for Builders

This document defines the **edit-time typing model** for `ObjectBuilder`
methods. It is CIM-Builder's adoption of cim-graph 0.5 §5a
(`/home/ande188/CIM-Graph/docs/development/PROFILE_IDENTITY_0_5_PLAN.md`). The
runtime side (`cim = self.network.cim`) is in `ARCHITECTURE.md`; this doc is the
type-checker side that sits on top of it.

The `line_builder.py` sketch was the first probe at this model. This doc
formalizes what it was reaching for.

---

## The problem

Runtime and edit-time pull in opposite directions:

- **Runtime truth:** `self.network.cim` is *one* module whose `ACLineSegment`
  carries **every** profile's fields (connectivity + electrical + short-circuit +
  asset…). Under cim-graph 0.5 this module is a runtime *merge* — it has **no
  file on disk**. Pylance can only see it as `ModuleType` / `Any`: no
  completions, no field checking.
- **What we want at edit time:** in `add_electrical_bal` you should get
  completions for `r`, `x`, `bch` — and a *flag* if you accidentally set `r0`
  (short-circuit). The method should be scoped to **one profile's fields**. (The
  connectivity flag arrives with the CIM18 CN split; under CIM17 the CN classes
  share the EQ part.)

A single annotation can't be both the wide runtime truth and the narrow per-method
scope. So we split them.

---

## The model: runtime wide, edit-time narrow

| | What `cim` is | Why |
|---|---|---|
| **Runtime** | `self.network.cim` — the full (merged) module; one object carries every profile's fields | class-identity correctness — the 0.5 thesis |
| **Edit time** | annotated as **one** sub-profile per method (`cim: CN`, `cim: EQ`, `cim: SC`) via `TYPE_CHECKING` imports | scopes each method's **write access** to one profile |

The per-method annotation is **deliberately narrower than the runtime truth**.
That is the point: it tells Pylance "in this method you may only touch this
profile's fields."

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from cimgraph.models import GraphModel
from cimbuilder.object_builder.object_builder import ObjectBuilder

if TYPE_CHECKING:
    import cimgraph.data_profile.cgmes_3_0_0.core_equipment          as EQ
    import cimgraph.data_profile.cgmes_3_0_0.short_circuit           as SC
    import cimgraph.data_profile.cgmes_3_0_0.steady_state_hypothesis as SSH
    # import cimgraph.data_profile.cgmes_3_0_0.dynamics              as DN


@dataclass
class LineBuilder(ObjectBuilder):
    network: GraphModel
    container: "EQ.EquipmentContainer"

    def create(self, name: str) -> "LineBuilder":
        cim: EQ = self.network.cim                 # runtime: the merged module
        self.line: "EQ.ACLineSegment" = cim.ACLineSegment(name=name)
        self.line.EquipmentContainer = self.container
        self._add(self.line)
        return self

    def add_connectivity(self, node1, node2) -> "LineBuilder":
        cim: EQ = self.network.cim                 # CIM17: CN lives in EQ (see below)
        t1 = self._new_terminal(self.line, 1, f'{self.line.name}_t1')
        t2 = self._new_terminal(self.line, 2, f'{self.line.name}_t2')
        self._connect_node(t1, node1)
        self._connect_node(t2, node2)
        return self

    def add_electrical_bal(self, r, x, bch,
                           r_unit=None, x_unit=None, bch_unit=None) -> "LineBuilder":
        cim: EQ = self.network.cim                 # balanced: scalar r/x/bch on EQ
        self.line.r = cim.Resistance(r, r_unit or 'ohm')
        self.line.x = cim.Reactance(x, x_unit or 'ohm')
        self.line.bch = cim.Susceptance(bch, bch_unit or 'S')
        return self

    def add_electrical_unbal(self, *a, **k) -> "LineBuilder":
        # per-phase impedance (ACLineSegmentPhase / PerLengthPhaseImpedance) —
        # stubbed until the CIM18 unbalanced profile parts ship (next round)
        raise NotImplementedError('unbalanced electrical lands with the CIM18 parts')

    def add_short_circuit(self, r0, x0, b0ch) -> "LineBuilder":
        cim: SC = self.network.cim                 # r0/x0/b0ch live in the SC part
        self.line.r0 = cim.Resistance(r0, 'ohm')
        self.line.x0 = cim.Reactance(x0, 'ohm')
        self.line.b0ch = cim.Susceptance(b0ch, 'S')
        return self
```

`cim: SC = self.network.cim` — the annotation says SC, the runtime value is the
full merged module. The assignment is fine at runtime (it's the same object);
Pylance treats `cim` as the SC slice and offers only SC's classes. The local
annotation **narrows**, it does not change the value.

> **CIM17 vs CIM18 — the connectivity slice.** In CGMES 3.0 (CIM17), the
> `core_equipment` (EQ) part carries *both* the connectivity classes (`Terminal`,
> `ConnectivityNode`) and the electrical fields (`r`, `x`, `bch`). So today
> `add_connectivity` and `add_electrical_bal` both annotate `cim: EQ`. The
> **method boundary still holds** — connectivity wiring and impedance values are
> distinct methods (and distinct wizard pages) — only the *type slice* coincides.
> CIM18 splits connectivity into its own part; when those official profile parts
> ship, `add_connectivity` narrows to `cim: CN` with no change to the method
> shape. The seam is already in place; only the annotation tightens.

---

## Why scope by profile

- **Guardrail.** `self.line.r0` inside `add_electrical_bal` is a category error —
  `r0` is short-circuit. With the method scoped to `cim: EQ`, Pylance rejects it
  (`r0` is only on the SC slice). The profile partition is enforced at edit time,
  not discovered at runtime. (Under CIM17 the EQ slice still holds connectivity,
  so a connectivity/electrical mix-up is *not* yet flagged — that guardrail
  arrives with the CIM18 CN split. The SC ↔ EQ guardrail works today.)
- **No file on disk.** No `.pyi`, no `generate_type_stubs`, no canonical flat
  import. The `TYPE_CHECKING` imports of the real `cgmes_3_0_0` sub-profile
  modules are the only machinery, and they are erased at runtime (`if
  TYPE_CHECKING` is always false at runtime; `from __future__ import annotations`
  makes the string annotations lazy).
- **It maps 1:1 onto the UI wizard.** "Add Line" → a wizard with one page per
  profile (Connectivity → Electrical → Short-circuit). Each page is backed by one
  `add_<profile>` method, and that method's profile slice is exactly the set of
  fields the page renders. Type narrowing and UI step structure are the same
  boundary.

---

## The one wrinkle (don't mistake it for a bug)

The method's profile slice is narrower than the runtime module. That is correct
for **writes**. If a method legitimately needs to **read** a field that belongs
to another profile on the same object, Pylance will flag it. That flag is the
signal to **move the read into the method scoped to that profile**, not to widen
the annotation. The constraint is healthy — document it, don't defeat it.

(Contrast: exporters/converters read *across* profiles by design and use the
**wide** annotation — the whole merged profile, via a `.pyi`. That is CIMHub's
§5c case, not ours. Builders write, so builders narrow.)

---

## Today vs. the 0.5 target

cim-graph **0.5.0a1** ships the deployable target: `network.cim` is live on
`GraphModel`, and the `cgmes_3_0_0` merged profile exposes real sub-profile parts
(`core_equipment`, `short_circuit`, `topology`, `steady_state_hypothesis`,
`state_variables`, `operation`, `equipment_boundary`, `geographical_location`,
`diagram`, `dynamics`). The §5a imports resolve against a real checkout.

| | Today (`feature/23` pin) | Target (cim-graph 0.5.0a1) |
|---|---|---|
| Runtime profile | flat `cimhub_2023` | `cgmes_3_0_0` runtime merge |
| Profile source in method | should become `self.network.cim` (Phase 3) | `self.network.cim` |
| `TYPE_CHECKING` imports | not yet (pin predates 0.5) | `cgmes_3_0_0.core_equipment` / `.short_circuit` / … |
| Connectivity slice | n/a | `cim: EQ` (CIM17); narrows to `cim: CN` when CIM18 parts ship |
| Annotation | single flat slice until the pin is bumped | full §5a per-method narrowing |

**Gap status (Phase 0 / Phase 1).** The gap the original plan flagged is now
**closed at the source**: 0.5.0a1 deploys `cgmes_3_0_0` with the parts the §5a
imports need. The remaining work is to bump CIM-Builder's own dependency pin
(`cim-graph>=0.3.2,<0.4.0` → the 0.5 line) in Phase 1. Until then:

1. Develop builders against the local 0.5.0a1 checkout
   (`/home/ande188/CIM-Graph`), where `network.cim` and the `cgmes_3_0_0` parts
   exist.
2. The runtime code (`cim = self.network.cim`) is correct either way — only the
   edit-time `TYPE_CHECKING` annotation depends on the installed package version.

**Note — `cim18gmdm` (unbalanced).** 0.5.0a1 also ships a `cim18gmdm` merged
profile, but its `electrical` part collapses connectivity + balanced electrical
together and there is no separate `short_circuit` part. The unbalanced /
per-phase model (`ACLineSegmentPhase`, `PerLengthPhaseImpedance`) is the
`add_electrical_unbal` path, deferred to the next round (see `BUILDER_API.md`).
The reference builders target `cgmes_3_0_0` first.

---

## Checklist for typing a builder method

- [ ] `from __future__ import annotations` at the top of the file
- [ ] sub-profile imports under `if TYPE_CHECKING:` (erased at runtime)
- [ ] each `add_<profile>` opens with `cim: <SLICE> = self.network.cim`
- [ ] the stored object (`self.line`, …) is annotated with the profile slice it's
      being written through in that method
- [ ] no method reads or writes a field outside its profile slice — if Pylance
      flags one, move it to the right method rather than widening
- [ ] no `.pyi`, no flat canonical import for the builder (that's the converter
      pattern, not this one)

---

## Related documents

- `ARCHITECTURE.md` — the runtime `network.cim` rule this typing sits on.
- `BUILDER_API.md` — the method signatures being typed.
- cim-graph 0.5 §5a (builder/write typing) and §5c (converter/read typing):
  `/home/ande188/CIM-Graph/docs/development/PROFILE_IDENTITY_0_5_PLAN.md`.
