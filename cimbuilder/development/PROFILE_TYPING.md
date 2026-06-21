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
- **What we want at edit time:** in `add_electrical` you should get completions
  for `r`, `x`, `bch` — and a *flag* if you accidentally set `r0` (short-circuit)
  or wire a node (connectivity). The method should be scoped to **one profile's
  fields**.

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
    import cimgraph.data_profile.cim18gmdm.connectivity   as CN
    import cimgraph.data_profile.cim18gmdm.electrical     as EQ
    import cimgraph.data_profile.cim18gmdm.short_circuit  as SC
    import cimgraph.data_profile.cim18gmdm.asset          as AST
    # import cimgraph.data_profile.cim18gmdm.dynamics     as DN


@dataclass
class LineBuilder(ObjectBuilder):
    network: GraphModel
    container: "CN.EquipmentContainer"

    def create(self, name: str) -> "LineBuilder":
        cim: EQ = self.network.cim                 # runtime: the merged module
        self.line: "EQ.ACLineSegment" = cim.ACLineSegment(name=name)
        self.line.EquipmentContainer = self.container
        self._add(self.line)
        return self

    def add_connectivity(self, node1, node2) -> "LineBuilder":
        cim: CN = self.network.cim                 # edit time: only CN fields offered
        t1 = self._new_terminal(self.line, 1, f'{self.line.name}_t1')
        t2 = self._new_terminal(self.line, 2, f'{self.line.name}_t2')
        self._connect_node(t1, node1)
        self._connect_node(t2, node2)
        # self.line.r = ...  ← would be flagged here: `r` is electrical, wrong method
        return self

    def add_electrical(self, r, x, bch,
                       r_unit=None, x_unit=None, bch_unit=None) -> "LineBuilder":
        cim: EQ = self.network.cim                 # same object, electrical slice
        self.line.r = cim.Resistance(r, r_unit or 'ohm')
        self.line.x = cim.Reactance(x, x_unit or 'ohm')
        self.line.bch = cim.Susceptance(bch, bch_unit or 'S')
        return self

    def add_short_circuit(self, r0, x0, b0ch) -> "LineBuilder":
        cim: SC = self.network.cim
        self.line.r0 = cim.Resistance(r0, 'ohm')
        self.line.x0 = cim.Reactance(x0, 'ohm')
        self.line.b0ch = cim.Susceptance(b0ch, 'S')
        return self
```

`cim: CN = self.network.cim` — the annotation says CN, the runtime value is the
full module. The assignment is fine at runtime (it's the same object); Pylance
treats `cim` as the CN slice and offers only CN's classes. The local annotation
**narrows**, it does not change the value.

---

## Why scope by profile

- **Guardrail.** `self.line.r` inside `add_connectivity` is a category error —
  `r` is electrical. With the method scoped (the object typed via the active
  profile slice) Pylance rejects it. The profile partition is enforced at edit
  time, not discovered at runtime.
- **No file on disk.** No `.pyi`, no `generate_type_stubs`, no canonical flat
  import. The `TYPE_CHECKING` imports of the real `cim18gmdm` sub-profile modules
  are the only machinery, and they are erased at runtime (`if TYPE_CHECKING` is
  always false at runtime; `from __future__ import annotations` makes the string
  annotations lazy).
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

## Today vs. 0.5

| | Today (`feature/23`) | Target (cim-graph 0.5) |
|---|---|---|
| Runtime profile | flat `cimhub_2023` | `cim18gmdm` runtime merge |
| Profile source in method | should become `self.network.cim` (Phase 3) | `self.network.cim` |
| `TYPE_CHECKING` imports | `cim18gmdm.connectivity` etc. **may not yet exist** | the real sub-profile packages |
| Annotation | use a single slice (or `# type: ignore` the import) until the sub-profiles are importable | full §5a per-method narrowing |

**Gap to track (Phase 0 / Phase 1).** The §5a `TYPE_CHECKING` imports target the
`cim18gmdm` sub-profile packages. The current dependency pin is
`cim-graph>=0.3.2,<0.4.0` with the flat `cimhub_2023` profile; the sub-profile
packages arrive with the 0.5 line. Until the pin is bumped (Phase 1), the
`TYPE_CHECKING` imports may be unresolved. Options, in order of preference:

1. Develop builders against the local cim-graph 0.5 checkout
   (`/home/ande188/CIM-Graph`), where `network.cim` and the sub-profiles exist.
2. Temporarily annotate with the flat profile (`import cimgraph.data_profile.cimhub_2023 as CN`)
   as a single slice; swap to true sub-profile slices when 0.5 lands.

The runtime code (`cim = self.network.cim`) is correct either way — only the
edit-time annotation depends on the sub-profile packages existing.

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
