# Profile-Scoped Typing for Builders

**Status:** revised — the `TYPE_CHECKING`-gated sub-profile import model this
doc originally specified was never adopted; the shipped reference
implementation imports real, always-live part modules instead. See the
revision note.

> **Revision note.** `cimbuilder/builders/load/consumer.py`
> (`EnergyConsumerBuilder`) imports its part modules
> (`cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN`, `.
> electrical_unbalanced as EL`, `.steady_state_hypothesis as SSH`) as plain,
> always-executed top-level imports — never gated behind `if TYPE_CHECKING:`.
> There was never a reason to defer them: unlike cim-graph 0.5's old
> `cgmes_3_0_0`/`cim18gmdm` placeholders (which this doc was written against
> and which no longer exist), `cimprofiles.cim18.cim18v17`'s part modules are
> real, lightweight dataclass modules with no circular-import or heavy-runtime
> concern — so there's nothing to gain from hiding the import from the
> interpreter. This doc is rewritten to describe typing against those real
> imports instead. The underlying idea (annotate a method-local name to the
> narrow part module so Pylance flags a cross-part field) is unchanged and
> still valid — only the "how you get the module" step changes.

This document defines the **edit-time typing model** for `ObjectBuilder`
methods: how to annotate a builder method so Pylance narrows completions and
flags a field written through the wrong profile part. The runtime side
(`self.cim = network.cim`, and the actual enforced check,
`graph_write.set_attr`/`set_assc`) is in `ARCHITECTURE.md` and
`GRAPH_WRITE_CONTRACT.md` §2; this doc is the type-checker side that sits on
top of it — Layer 1 of the three-layer model in `PROFILE_RESOLUTION.md`.

> **Scope.** This is layer 1 of 3 (edit-time only). It protects hand-written builder
> code in the editor and does nothing at runtime or for `.cimtbl` data. The runtime
> check is `GRAPH_WRITE_CONTRACT.md` §2; how the profile is selected is
> `PROFILE_RESOLUTION.md`.

---

## The problem

Runtime and edit-time pull in opposite directions:

- **Runtime truth:** `self.cim` (= `network.cim`) is *one* module whose
  `ACLineSegment` carries **every** profile's fields (connectivity + electrical
  + short-circuit + asset…) — a runtime merge, with no single file on disk that
  has only those fields. Pylance can only see it as `ModuleType` / `Any`: no
  completions, no field checking.
- **What we want at edit time:** in `add_electrical` you should get completions
  for `pfixed`, `qfixed` — and a *flag* if you accidentally set a field that
  belongs to a different part. The method should be scoped to **one part's
  fields**.

A single annotation can't be both the wide runtime truth and the narrow
per-method scope. So we annotate a *second*, part-scoped name.

---

## The model: runtime wide, edit-time narrow

| | What the name is bound to | Why |
|---|---|---|
| **Runtime (`self.cim`)** | `network.cim` — the full (merged) module; one object carries every profile's fields | class-identity correctness — object construction and FK resolution need the merged view |
| **Edit time (a part-module import)** | a real, always-imported `cimprofiles.cim18.cim18v17.<part>` module, aliased per part (`CN`, `EL`, `SSH`, …) | scopes that method's **write access** to one profile part — this is the exact module passed as `graph_write.set_attr`/`set_assc`'s `part` argument, so the edit-time check and the runtime check agree |

This is how `consumer.py` is actually written — the part modules are plain,
unconditional imports (nothing is gated behind `TYPE_CHECKING`), because they
cost nothing to import and the same module object is what `graph_write` checks
against at runtime:

```python
import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write


class EnergyConsumerBuilder(ObjectBuilder):
    cim_class_name = 'EnergyConsumer'

    def add_connectivity(self, load, *, node: str, container: object = None,
                          phaseConnection=None, grounded=None, customerCount=None,
                          BaseVoltage=None) -> None:
        connectivity.add_connectivity(
            self.network, load, node_cols={'node': node},
            container=container if container is not None else self.container)
        graph_write.set_attr(load, CN, 'customerCount', customerCount)
        graph_write.set_attr(load, CN, 'grounded', grounded)
        graph_write.set_attr(load, CN, 'phaseConnection', phaseConnection)
        if BaseVoltage is not None:
            target = graph_write.resolve(self.network, self.cim.BaseVoltage, BaseVoltage)
            graph_write.set_assc(load, CN, 'BaseVoltage', target)

    def add_electrical(self, load, *, pfixed=None, qfixed=None,
                        pfixedPct=None, qfixedPct=None, LoadResponse=None) -> None:
        graph_write.set_attr(load, EL, 'pfixed', pfixed)
        graph_write.set_attr(load, EL, 'qfixed', qfixed)
        graph_write.set_attr(load, EL, 'pfixedPct', pfixedPct)
        graph_write.set_attr(load, EL, 'qfixedPct', qfixedPct)
        if LoadResponse is not None:
            target = graph_write.resolve(self.network, self.cim.LoadResponseCharacteristic, LoadResponse)
            graph_write.set_assc(load, EL, 'LoadResponse', target)

    def add_ssh(self, load, *, p=None, q=None) -> None:
        graph_write.set_attr(load, SSH, 'p', p)
        graph_write.set_attr(load, SSH, 'q', q)
```

`CN`/`EL`/`SSH` are real module objects: Pylance resolves them against the
actual files in `cimprofiles/cim18/cim18v17/`, so `graph_write.set_attr(load,
EL, 'pfixed', ...)` gets real completions for `EL.EnergyConsumer`'s fields, and
a typo'd or wrong-part attribute name is a `ValueError` at runtime (§2 of
`GRAPH_WRITE_CONTRACT.md`) — not currently flagged at edit time, since
`set_attr`'s `attr` parameter is a plain `str`, not a `Literal` over the part
module's field names. Getting a edit-time flag for that would mean typing
`attr` against `EL`'s own fields (e.g. an overload per part module) — not
attempted yet; today's guardrail is runtime-only, same as any other `attr: str`
call.

> **Why no `self.cim: EL` narrowing inside the method.** Earlier drafts of this
> doc had each method open with `cim: <SLICE> = self.network.cim` — re-binding
> the *merged* module under a narrow annotation. The shipped code doesn't do
> this: it imports the real part module directly under its own name (`EL`), so
> there's no runtime value being "re-typed," just a second, narrower import
> used only for the parts of the method that need it (mainly as `graph_write`'s
> `part` argument). `self.cim` (the merged module) is still what `create()` and
> FK resolution (`self.cim.BaseVoltage`) use — the two names serve different
> purposes and are never meant to be interchangeable.

---

## Why scope by profile

- **Guardrail.** Setting a short-circuit field inside `add_electrical` is a
  category error. Passing `graph_write.set_attr(load, EL, 'r0', ...)` fails at
  runtime (`r0` isn't a field of `EL.EnergyConsumer`); importing and passing
  `cimprofiles.cim18.cim18v17.short_circuit as SC` instead, inside the right
  method, is what gets it right. The profile partition is enforced per-method
  by which part module that method imports and passes to `graph_write` — a
  method only has access to the part modules it chose to import.
- **No file on disk needed beyond the real profile package.** No `.pyi`, no
  `generate_type_stubs`, no canonical flat import — just a plain import of the
  real `cimprofiles.cim18.cim18v17.<part>` module.
- **It maps 1:1 onto the CIM export-part split.** Connectivity, electrical,
  SSH, short-circuit, asset are real serialization-part boundaries; one
  `add_<profile>` method per part keeps the builder's method boundary aligned
  with that split (and with any future UI wizard built around the same parts).

---

## The one wrinkle (don't mistake it for a bug)

A method's part-module import is narrower than `self.cim`. That is correct for
**writes** scoped to that part. If a method legitimately needs to **resolve a
reference** that belongs to another part on the same object (e.g.
`add_connectivity` resolving `BaseVoltage`), it reads that reference's target
class off `self.cim` (the merged module), not off the narrow part import — see
`consumer.py`'s `self.cim.BaseVoltage` / `self.cim.LoadResponseCharacteristic`.
The part import is for the `graph_write` call's `part` argument specifically,
not a replacement for `self.cim` everywhere in the method.

(Contrast: exporters/converters read *across* profiles by design and use the
wide, merged module throughout. Builders mostly write, so builders bring in a
narrow part module for the write call, while still reading `self.cim` for
anything that needs the merged view.)

---

## Related documents

- `ARCHITECTURE.md` — the runtime `self.cim` rule this typing sits on, and the
  full `ObjectBuilder` shape.
- `BUILDER_API.md` — the method signatures being typed.
- `GRAPH_WRITE_CONTRACT.md` §2 — the runtime check `graph_write.set_attr`/
  `set_assc`'s `part` argument performs; this doc's edit-time narrowing and
  that runtime check use the exact same module object.
- `PROFILE_RESOLUTION.md` — all three profile mechanisms (this is Layer 1).
