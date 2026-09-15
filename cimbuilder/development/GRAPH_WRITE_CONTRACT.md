# graph_write contract & profile-part grounding

**Status:** design contract, agreed 2026-09-15 (revised same day once a
runtime part-check replaced the original Pylance-only mechanism — see §2).
Read this before adding any new `add_<part>` method to any `ObjectBuilder`
subclass, or before touching `cimbuilder/core/graph_write.py`. This doc is the
thing to re-read cold in a future session — it does not assume you remember
this conversation.

Related docs: `CIMTBL_DESIGN.md` (§4.1 `ObjectBuilder`, §12.3 graph-write core),
root `CLAUDE.md` (`ARCHITECTURE.md` table, target builder API, units rules).
This doc supersedes those where they conflict on the specific questions below —
those docs describe the pre-existing plan; this doc records what was actually
decided once real profile source got read.

---

## 1. The three concerns, kept separate

Every `add_<part>` method call touches three genuinely different problems.
They are solved by three different mechanisms, on purpose — do not try to
merge them into one function or one type:

| Concern | Solved by | Where it lives |
|---|---|---|
| "Is this the *right attribute* for this profile part?" | Runtime part-module field check | `graph_write.set_attr` / `graph_write.set_assc` |
| "Is the *value* the right CIMUnit/shape?" | Runtime Qty handling | `graph_write.set_attr` |
| "Did I write *both sides* of an association?" | Runtime inverse-metadata lookup | `graph_write.set_assc` |

**All three now live inside `graph_write`, driven by the same mechanism**: a
part module (`CN`, `EL`, ...) passed into `set_attr`/`set_assc`, checked by
name against `type(load).__name__`'s field set in that module. There is no
separate static/Pylance mechanism anymore — see §2 for why the original
Pylance-parameter-typing idea was superseded, and why that's fine.

---

## 2. Part-membership checking: runtime, not static (concern 1)

### Why the original Pylance approach was replaced

The first version of this contract proposed typing each `add_<part>` method's
object parameter to a part-scoped class (`load: CN.EnergyConsumer`) so Pylance
would flag an out-of-part attribute access in the editor. That mechanism is
real (confirmed earlier this session) but has two real limits: it only ever
fires for a human looking at the editor — it is a no-op at the moment code
actually runs, e.g. against real `.cimtbl` row data — and it silently does
nothing once `cimhub_2026`'s profile is merged (today), since a merged class
has every field regardless of "part," so there's nothing to narrow against.

A cleaner, **runtime** check replaces it, discovered by directly probing the
mechanism:

```python
from types import ModuleType
import cimgraph.data_profile.cimhub_2026 as cim
import cimgraph.data_profile.cim18gmdm.connectivity as CN

test_load = cim.EnergyConsumer(name='test')
setattr(test_load, 'customerCount', 2)   # CN.EnergyConsumer has this field - fine
setattr(test_load, 'p', 200.0)           # CN.EnergyConsumer does NOT - should fail
```

The key property, and the reason this works at all: **the check is entirely
name-keyed, never identity- or type-based.** `test_load` is a real
`cimhub_2026.EnergyConsumer` instance — it has no subclass/inheritance
relationship to `CN.EnergyConsumer` whatsoever, and never will, regardless of
which profile `CIMG_DATA_PROFILE` resolves to at runtime. The check only ever
asks: "does the class in `CN` *named* `type(load).__name__` declare a field
*named* `'customerCount'`?" — two string lookups, nothing else. That's what
decouples the reference part module (`CN`, imported at the top of the builder
file, chosen for being genuinely part-scoped and proven-correct) from the
live runtime profile (`cimhub_2026`, resolved by `CIMG_DATA_PROFILE`, possibly
merged, possibly a completely different class hierarchy). One is a shape
reference; the other is what's actually being built. They never need to be
the same class, or even related classes, for the check to be meaningful.

This also means the check keeps working unchanged, with zero code changes,
once `cimhub_2026` splits for real next week — only the *import* at the top of
each builder file changes (`cim18gmdm.connectivity` → `cimhub_2026.connectivity`,
a mechanical `sed`), because the mechanism never depended on which module `CN`
pointed to, only on it being a genuinely part-scoped reference.

### The collapsed API contract

Two entry points, both in `cimbuilder/core/graph_write.py`, both taking the
part module as an explicit argument:

```python
set_attr(load, CN, 'customerCount', value)         # scalar / Qty
set_assc(load, CN, 'BaseVoltage', bv_obj)          # association, forward + reverse
```

- **`load`** — the live object being mutated (any profile's instance; never
  type-checked against `CN`, only name-checked — see above).
- **`CN`** — the reference part module, a plain **top-level import** in the
  builder file (not `TYPE_CHECKING`-gated — it's consulted at runtime now):
  ```python
  import cimgraph.data_profile.cim18gmdm.connectivity as CN
  import cimgraph.data_profile.cim18gmdm.electrical as EL
  ```
- **class name** — never passed explicitly; both functions derive it as
  `type(load).__name__` and look up `getattr(CN, that_name)`. One less
  parameter, and it's always correct since it's asking "does *this object's*
  class, by name, have this field in this part" — the only question that
  matters.
- **Fail fast, loudly, on any mismatch** — wrong part module for this
  attribute, or wrong function for this field's category (see below) — always
  a raised, clear exception. Never a silent skip, never a bare `KeyError`.

### `set_attr` — scalars and Qtys

```python
def set_attr(load: object, part: ModuleType, attr: str, value: object) -> None:
    """Set a plain scalar or Qty onto load.<attr>, after checking that <attr>
    is a real, non-association field of part.<type(load).__name__>.

    Raises ValueError if:
    - <attr> is not a field of that part's class at all (wrong part, or a
      typo) - wrong-part attributes must fail loudly, not silently pass
      through to a merged profile that happens to have every field.
    - <attr> IS a field, but it's an association (has metadata['inverse']) -
      use set_assc for that, not set_attr.
    """
```

Internals: same Qty-unwrap logic `set_attr` already has today (unchanged,
still driven by `_cim_unit_type` off `type(load)` for the actual CIMUnit
construction — that part was never broken). What's new is the guard at the
top: look up `getattr(part, type(load).__name__).__dataclass_fields__`,
`KeyError` on a missing `attr` becomes a wrapped, clear `ValueError` naming
the part module and class (a bare `KeyError('p')` doesn't explain the
profile-part concept to someone unfamiliar with it), and a field whose
`metadata['inverse']` is not `None` is also rejected — that's `set_assc`'s
job, and a builder method calling the wrong one is exactly the kind of
mistake this contract exists to catch.

**`create_attr` and the original `link()` design are both dropped entirely** —
superseded by this section and §3's `set_assc`, respectively. Every
`add_<part>` method calls `graph_write.set_attr`/`graph_write.set_assc` — no
exceptions, no bare `setattr`, no literal-assignment style anywhere in builder
code.

---

## 3. `set_assc` — associations, forward + reverse in one call

Confirmed by reading cimgraph's own bidirectional-set convention in
`cimgraph/databases/fileparsers/xml_parser.py` (`parse_value`, ~line 260-270):
when cimgraph's XML parser establishes an association, it calls the
lower-level `create_edge` **twice** — once for the forward attribute, once for
the reverse attribute name found via `.metadata['inverse']` on the dataclass
field:

```python
value = self.create_edge(self.graph, cim_class, identifier, sub_tag, edge_class, edge_uri)
try:
    reverse = cim_class.__dataclass_fields__[association].metadata['inverse']
    self.create_edge(self.graph, edge_class, edge_uuid, reverse, cim_class, identifier)
except Exception as e:
    _log.log(self.log_level, f'Could not identify inverse for ...')
```

`create_edge` itself (`cimgraph/databases/__init__.py:234`) only ever writes
one attribute per call — **the caller is responsible for issuing both.**
`set_assc` is our one call site for "establish an association," so it takes
over that responsibility once, generically, so no builder method ever has to
know `.metadata['inverse']` exists.

### The metadata, confirmed real and generic

Every association-typed dataclass field carries `.metadata['inverse']` as
`'<ClassName>.<attrName>'`, regardless of profile part; plain scalar/enum
fields carry `inverse: None`. That's the same signal `set_attr`/`set_assc` use
to reject the wrong category of field (§2):

```
>>> import dataclasses
>>> import cimgraph.data_profile.cim18gmdm.connectivity as CN
>>> for f in dataclasses.fields(CN.EnergyConsumer):
...     print(f.name, '|', f.type, '|', f.metadata.get('inverse'))
...
customerCount | Optional[int]              | None
grounded      | Optional[bool]             | None
phaseConnection | Optional[PhaseShuntConnectionKind] | None
EquipmentContainer | Optional[EquipmentContainer] | EquipmentContainer.Equipments
BaseVoltage   | Optional[BaseVoltage]      | BaseVoltage.ConductingEquipment
Terminals     | list[Terminal]             | Terminal.ConductingEquipment
```

And the reverse side can independently be singular or list-shaped — check
both sides, don't assume:

```
>>> CN.BaseVoltage.__dataclass_fields__['ConductingEquipment'].type
'list[ConductingEquipment]'
```

So `set_assc(load, CN, 'BaseVoltage', bv_obj)` — forward side (`load.BaseVoltage`)
is singular, reverse side (`bv_obj.ConductingEquipment`) is a list.

### The `set_assc` contract

```python
def set_assc(load: object, part: ModuleType, assc: str, target: object) -> None:
    """Set load.<assc> = target AND write the reverse side onto target,
    resolved from part.<type(load).__name__>'s field metadata['inverse'].
    The one call site for establishing any association - both sides are
    always written together, so the graph is never one-sided.

    Raises ValueError if:
    - <assc> is not a field of part.<type(load).__name__> at all (wrong part,
      typo).
    - <assc> IS a field, but it's a plain scalar (metadata['inverse'] is
      None) - use set_attr for that, not set_assc.
    """
```

Behavior, decided 2026-09-15:

- **Resolve the reverse attribute name from `.metadata['inverse']` only** (via
  the same `part` module argument used for the forward-field check — no
  separate lookup, no explicit `reverse=` override param). Missing metadata is
  the "not a field of this part" failure above, not a separate silent case.
- **Whichever side (forward or reverse) is a `list[...]` field:** append
  `target` (or `load`, on the reverse side) onto that list, matching
  `create_edge`'s own dedup-by-identity check (`if not any(x is obj for x in
  obj_list)`) so re-linking the same pair twice is a no-op, not a duplicate.
- **Whichever side is a singular (`Optional[...]`) field:** overwrite
  unconditionally — plain `setattr`. This matches cimgraph's own `create_edge`
  behavior for singular associations (last write wins, no validation). If a
  caller links contradictory singular associations, that's a modeling/
  validation problem `set_assc` does not own — same posture as `resolve()`
  never raising on a missing name (§12.3 of `CIMTBL_DESIGN.md`).
- Forward and reverse sides are checked/branched **independently** — one can
  be singular while the other is a list (the common case, e.g.
  `EnergyConsumer.BaseVoltage` singular vs. `BaseVoltage.ConductingEquipment`
  a list).

Implementation note: resolve everything off `type(load)`/`type(target)` and
the given `part` module — never off `network.cim`. Neither function takes a
`network` parameter; that's intentional, matching how `set_attr` already
works today.

---

## 5. Grounding yourself in a real profile part before writing a method

**Never guess which attributes belong to which part. Grep the real source.**
This applies whether you're a human or an agent — the whole point of this
section is that "known CIM knowledge" is not a substitute for reading the
actual profile module, because extension classes, ShadowExtensions, and this
project's own split choices can differ from the UML you might expect.

### Which profile to read

- **`cim18gmdm`** is the canonical, already-split, live-interop-tested (with
  Siemens/GE) reference for *how a real profile part is structured*. Use it to
  ground every `add_<part>` method you write, **even though this repo's actual
  runtime profile is `cimhub_2026`.**
- **`cimhub_2026`** is this repo's real profile, but it is **currently a single
  merged module** — `cimgraph.data_profile.cimhub_2026.network.cim.<Class>`
  carries every attribute from every part, because it has not been split yet.
  Per the repo owner: it will be split next week, following the same
  submodule/part shape `cim18gmdm` already uses, at which point a `sed
  s/cim18gmdm/cimhub_2026/` across this repo's `TYPE_CHECKING` imports becomes
  mechanically valid. **Until that split lands, do not type a builder method's
  parameter against `cimhub_2026`'s part module — it doesn't have one.** Type
  it against `cim18gmdm`'s real part class instead (§2's example), and don't
  worry that the runtime object being passed in is actually a `cimhub_2026`
  instance — Pylance's structural check only cares that the runtime object
  *has* the fields the type hint promises, and today it has every field of
  every part, a superset, so no false positive occurs. This is a temporary
  state — revisit every `TYPE_CHECKING` import in this repo once the split
  lands.
- **`cim18gmdm` is EQ-only today** — no SSH (steady-state hypothesis), no
  dynamics, no short-circuit, no AssetInfo module exist yet in this dependency.
  **If a grep for the part module comes back empty, that part genuinely
  doesn't exist as a real, grounded reference yet.** Do not fabricate a
  plausible-looking module path or class shape to fill the gap — see the rule
  at the end of §6.

### How to inspect a part module

Two techniques, use both:

**(a) Find the module path**, once, per part:
```bash
python3 -c "
import cimgraph.data_profile.cim18gmdm.connectivity as CN
print(CN.__file__)
"
```
Then read the file directly (`Read` tool or `grep -n 'class EnergyConsumer'`)
to see the real class body, docstrings included — docstrings on CIM fields
often state the profile intent in English (e.g. `phaseConnection`: "The type
of phase connection, such as wye or delta").

**(b) Inspect the live dataclass fields**, to get the exact, current, real
attribute set (don't hand-transcribe from reading source — confirm it
programmatically too, since generated code can shift):
```bash
python3 -c "
import cimgraph.data_profile.cim18gmdm.connectivity as CN
import dataclasses
for f in dataclasses.fields(CN.EnergyConsumer):
    print(f.name, '|', f.type, '|', f.metadata.get('inverse'))
"
```

This tells you, in one shot: every field this part actually has (which is
exactly what `set_attr`/`set_assc` check `attr`/`assc` against at runtime —
§2), its type (so you know if it's a `CIMUnit`-wrapped quantity, a plain
scalar, an enum, or an association), and whether it's an association needing
`set_assc` (has an `inverse`) vs. a plain value needing `set_attr` (inverse is
`None`).

---

## 6. Worked walkthrough: adding a new part to an existing builder

Worked example: adding `add_short_circuit` to `EnergyConsumerBuilder`, chosen
because it's a part that **does not exist yet** in `cim18gmdm` — this is
deliberately the harder, more honest case, not a part that's already there.

**Step 1 — does the part module exist at all?**
```bash
$ python3 -c "import cimgraph.data_profile.cim18gmdm.short_circuit"
ModuleNotFoundError: No module named 'cimgraph.data_profile.cim18gmdm.short_circuit'
```
```bash
$ ls /home/ande188/CIM-Graph/cimgraph/data_profile/cim18gmdm/
__init__.py  asset  canonical  connectivity  diagram  electrical  location  marketnode
```
No `short_circuit` submodule. **Stop here.** This confirms §5's rule: this
part genuinely isn't grounded in any real profile source yet, split or
merged. Do not write `add_short_circuit` against a guessed/fabricated `SC`
reference module — there is nothing real to check it against.

**Step 2 — what do you do instead, given the part doesn't exist yet?**
Two honest options, pick based on whether the attributes exist in the
*merged* `cimhub_2026` profile today:
- If `cimhub_2026`'s merged `EnergyConsumer` already has the short-circuit
  attributes (check with `dataclasses.fields`, same technique as §5b, against
  `cimgraph.data_profile.cimhub_2026`) — you can write `add_short_circuit`
  today, but there's no genuine part module to pass as `set_attr`'s/
  `set_assc`'s `part` argument, so the runtime check can't be real either.
  Pass the merged `cimhub_2026` module itself as `part`, with a comment noting
  *why* it buys nothing:
  ```python
  import cimgraph.data_profile.cimhub_2026 as cim  # not a real part - see below

  def add_short_circuit(self, load, *, p0=None):
      # No cim18gmdm.short_circuit module exists yet to check `load` against
      # (checked 2026-09-15, see GRAPH_WRITE_CONTRACT.md §6). Using the merged
      # cimhub_2026 module as `part` here is a no-op check (every field is
      # "in" a merged module) - revisit once cimhub_2026 splits and/or
      # cim18gmdm gains a short_circuit part.
      graph_write.set_attr(load, cim, 'p0', p0)
  ```
- If the attributes don't exist anywhere yet either, this part isn't buildable
  yet — don't write the method at all (YAGNI; matches the standing instruction
  to defer builders/parts without a real, grounded pattern to follow).

**Step 3 — once a real part module exists (either `cim18gmdm` gains one, or
`cimhub_2026` splits — re-run Step 1 then), the full pattern is:**

```bash
# 1. Confirm the module and class exist
python3 -c "import cimgraph.data_profile.cim18gmdm.short_circuit as SC; print(SC.__file__)"

# 2. Inspect the real fields
python3 -c "
import cimgraph.data_profile.cim18gmdm.short_circuit as SC
import dataclasses
for f in dataclasses.fields(SC.EnergyConsumer):
    print(f.name, '|', f.type, '|', f.metadata.get('inverse'))
"
```

Suppose that prints (illustrative, not real until the module exists):
```
name | Optional[str] | None
p0 | Optional[float] | None
```

3. Import the real part module at the top of the builder file (a plain
   import now — it's consulted at runtime, not just for typing) and write the
   method using `set_attr`, passing the part module through:

```python
import cimgraph.data_profile.cim18gmdm.short_circuit as SC

class EnergyConsumerBuilder(ObjectBuilder):
    def add_short_circuit(self, load, *, p0=None) -> None:
        graph_write.set_attr(load, SC, 'p0', p0)
```

4. If the field list had included an association (non-`None` `inverse`),
   use `graph_write.set_assc(load, SC, assc_name, target)` instead of
   `set_attr` — never `setattr` directly, and never `set_attr` on an
   association field (it will raise — §2).

5. Add a test asserting the attribute round-trips correctly (value/unit for
   scalars, both-sides-linked for associations — assert on the reverse side
   too, e.g. `assert load in bv.ConductingEquipment`, not just the forward
   attribute, since that's specifically the bug `set_assc` fixes), **and** a
   test asserting the wrong-part case actually raises (e.g.
   `graph_write.set_attr(load, SC, 'phaseConnection', ...)` should raise,
   since `phaseConnection` belongs to the connectivity part, not short-circuit).

**The naming convention for the method itself:** domain-meaningful, not
profile-part-literal — `add_connectivity`, `add_electrical`, `add_short_circuit`
(not `add_CN`, `add_SSH`, `add_SC`). The mapping from method name to profile
part is documentation (a one-line docstring citing the part), not encoded in
the method name. Decided 2026-09-15: users of this library are domain experts
who think in "connectivity"/"electrical," not IEC document-part numbers.

---

## 7. `ObjectBuilder` shape (ties the above into the class contract)

Decided this session, supersedes `CIMTBL_DESIGN.md §4.1`'s literal code sketch
where it conflicts:

- **Fully stateless.** No `self.obj`. Every `add_<part>` method takes the
  object under construction as an explicit first parameter and returns it (or
  nothing) — never reads or writes an instance attribute holding the object.
  `network`/`container` stay on `self` — those are stable per-builder-instance
  configuration, not per-object state.
- **Why:** bulk `.cimtbl` parsing constructs one builder instance and reuses
  it across every row (thousands of objects, one builder — no per-object
  builder instances to garbage-collect). A future Flask API or PyQt6 desktop
  GUI wizard needs the **CIM object itself** to persist across multiple
  requests/tabs (open a wizard, fill a field, close it) — but the builder
  invoked to mutate it each time is incidental and can be constructed fresh
  per call. Statelessness serves both callers without a class fork: the object
  under construction is the thing with a lifetime; the builder never is.
- **`create()` returns the object directly**, not `self`:
  ```python
  def create(self, *, name: str) -> object:
      cim_cls = getattr(self.network.cim, self.cim_class_name)
      return cim_cls(name=name)
  ```
- **Each `add_<part>` method takes the object as its first parameter**, and
  calls `graph_write.set_attr`/`graph_write.set_assc` with the relevant part
  module (§2, §3) for every field it touches. It does not return the builder
  for chaining (chaining doesn't work once there's no `self.obj` to chain
  through) — it returns `None`, or the object again if that's convenient for
  the call site:
  ```python
  import cimgraph.data_profile.cim18gmdm.connectivity as CN

  def add_connectivity(self, load, *, node: str, container=None, phaseConnection=None) -> None:
      connectivity.add_connectivity(
          self.network, load, node_cols={'node': node},
          container=container if container is not None else self.container,
      )
      graph_write.set_attr(load, CN, 'phaseConnection', phaseConnection)
  ```
- **`add(obj)` (renamed from `build()`)** takes the object explicitly too:
  ```python
  def add(self, obj: object) -> object:
      graph_write.add_to_graph(self.network, obj)
      return obj
  ```
- **`from_table(row)`** stays the bulk-entry-point method, but now reads:
  ```python
  def from_table(self, row: object) -> object:
      load = self.create(name=row.name)
      self.add_connectivity(load, node=row.node, container=...)
      self.add_electrical(load, LoadResponse=row.LoadResponse)
      return self.add(load)
  ```

**Known current bugs this replaces** (present on disk as of 2026-09-15, from
an in-progress hand-edit that hadn't finished the migration): `base.py`'s
`add()` still read `self.obj` (always `None`, since `create()` had already
been changed to return the object rather than assign it); `consumer.py`'s
`add_connectivity` took `load` as a parameter but still called
`connectivity.add_connectivity(self.network, self.obj, ...)` internally
instead of using `load`; `from_table` still called `self.add_electrical(...)`
positionally with no object argument, and referenced a method
(`add_electrical`) that had been renamed to `add_SSH` elsewhere in the same
file. All three are fixed by consistently applying this section's contract:
no `self.obj`, ever, anywhere.

---

## 8. Summary checklist for a new `add_<part>` method

1. Grep/read the real part module (`cim18gmdm`, or `cimhub_2026` once split) —
   never assume field names or which part they belong to (§5).
2. If the part module doesn't exist yet for this class, stop — don't fabricate
   it (§6 step 1-2).
3. Import the real part module at the top of the builder file, as a plain
   (non-`TYPE_CHECKING`) import — it's consulted at runtime (§2).
4. For each field: scalar/Qty → `graph_write.set_attr(load, PART, attr, value)`;
   association (has `.metadata['inverse']`) →
   `graph_write.set_assc(load, PART, assc, target)` (§2, §3). Never call
   `setattr` directly in builder code, and never pass an association to
   `set_attr` or a scalar to `set_assc` — both raise on the mismatch.
5. Method name is domain-meaningful (§6, last paragraph).
6. Object is a parameter, not `self.obj` (§7).
7. Test the round-trip, including the reverse side of any association, and a
   negative test that a wrong-part attribute raises (§6 step 5).
