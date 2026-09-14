# CIM-Builder — Third Redesign: the `.cimtbl` DSL + per-profile Builder core

**Date:** 2026-09-13
**Status:** Design of record (pre-implementation). Supersedes the `feature/23`
builder-refactor phase plan where the two conflict — see §9 "What this replaces."
**Author:** aandersn (with Claude)

---

## 0. One-paragraph summary

CIM-Builder gets **one** user-facing surface built on **one** canonical core.
The surface is offered in two equivalent shapes over the same code:

1. **`.cimtbl`** — a human- and LLM-authorable, CIM-native table syntax
   (`Object` / `Table` / `Import`), parsed by a small **fixed** Lark grammar,
   validated against the active CIM profile by a **LinkML** schema, and executed
   by **per-class Builder** objects.
2. **The fluent Builder API** — the same per-class Builders driven directly in
   Python (`ACLineSegmentBuilder().create(...).add_connectivity(...).add_electrical(...)`)
   for power users and for other libraries (CIMHub converters).

Both shapes route every graph write through a shared **graph-write core** and a
shared **connectivity backend**. The connectivity backend is where the heavy
lifting lives (`node1` → `Terminal` + `ConnectivityNode` + per-phase children;
`bus1` → `TopologicalNode`; `%Z`/`pu`/`ohm` normalization). The front ends stay
skinny.

Design goals, in priority order (from the user): **auditability**,
**understandability**, **ease of use for humans and LLMs**. Everything below is
subordinate to those three.

---

## 1. Why a third redesign

The repo has carried three disagreeing build styles (standalone
`new_<equip>()` functions, class-based substation builders, a
documented-but-absent `*_functions.py` API). None of them is a *format* — they
are all Python call conventions, so a model built with them exists only as a
live graph or as RDF/XML, neither of which a human can read, diff, or hand-edit
comfortably.

The `.cimtbl` sketch (`ieee13.cimtbl`) is the insight that resolves this: **make
the authoring format itself CIM-native and human-readable.** Its column headers
are literally CIM attribute and association names; its units live in the header
(`r (ohm/mile)`); its rows are instances. It is to CIM what a `.dss` file is to
OpenDSS — except the "native format" *is* the profile, so there is no
`native ↔ CIM` mapping to maintain.

This redesign commits to that format as a first-class artifact and rebuilds the
Python API underneath it as a clean, shared, per-class core.

---

## 2. The layered architecture

```
                    ┌───────────────────────────────────────────┐
                    │         ieee13.cimtbl  (human / LLM)         │
                    └───────────────────────────────────────────┘
                              ▲                    │
              WRITER (Phase R)│                    │ Lark grammar (FIXED, tiny)
              cimgraph→.cimtbl│                    ▼   knows only: Object|Table|
                              │         ╔══════════════════════╗  Import, headers,
                              │         ║   Parse → records      ║  (units), cells
                              │         ╚══════════╤═══════════╝
                              │                    ▼
                              │    ┌──────────────────────────────────┐
                              │    │ LinkML validation gate            │  ← is this a
                              │    │ (RDFS-for-XML role; profile-aware) │    legal file?
                              │    └──────────────────────────────────┘
                              │                    │ validated records
        ╔═════════════════════╧════════════════════▼═══════════════════════════╗
        ║                 PER-CLASS BUILDER  (the canonical core)                 ║
        ║   ACLineSegmentBuilder / EnergyConsumerBuilder / PowerTransformerEnd… ║
        ║                                                                        ║
        ║   .from_table(row: <Class>Row)  ← DSL + bulk entry (typed dataclass)   ║
        ║   .create(name=…)              ← power-user entry                      ║
        ║   .add_connectivity(node1=, node2=, phases=)                           ║
        ║   .add_electrical(r=Qty(..), x=Qty(..), bch=Qty(..))   ← %Z/pu→ohm     ║
        ║   .add_short_circuit(…)                                                ║
        ║   .build() -> cim object                                               ║
        ╚═══════════════════╤════════════════════════════╤═══════════════════════╝
                            │                            │
                  plain attrs / FKs                connectivity + phasing + unit ctx
                            ▼                            ▼
        ┌───────────────────────────┐   ┌───────────────────────────────────────┐
        │   graph-write core         │   │   Connectivity backend (shared)         │
        │   set_attr(o, attr, v, u)  │◀──│   node* → ConnectivityNode              │
        │   link(o, assoc, target)   │   │   bus*  → TopologicalNode               │
        │   add_to_graph(o)          │   │   synth Terminal(seq=1,2,…)             │
        │   resolve(name) (deferred) │   │   phases=ABCN → N <Class>Phase children │
        │   reads network.cim once   │   │   auto-vivify undeclared nodes          │
        └───────────────────────────┘   └───────────────────────────────────────┘
```

### 2.1 The load-bearing decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Grammar scope** | Fixed, profile-agnostic, ~40 lines. Knows only `Object`/`Table`/`Import`, header tokens, `(unit)` suffixes, cells, comments, blank = unset. Knows **no** CIM class name. | Immortal across profile changes (`cimhub_2023` → `cgmes_3_0_0` → `cimhub_2026`). |
| **Runtime synthesis** | **Python, in the per-class Builder.** The Builder turns `node1` into terminal + phasing. | User's call: "parser-based for actual run-time (most robust)." Debuggable, auditable — you read code, not a YAML interpreter. |
| **LinkML's role** | **Validation + documentation, not execution.** Answers "is this a legal `.cimtbl` for this profile?" before the graph is touched. Never read inside the synthesis hot path. | User's call: "LinkML provides us file validation like RDFS does for the XML files." Keeps the two jobs separate. |
| **Parse target** | Two-phase: parse → LinkML-validated **dataclass** (`<Class>Row`, via **gen-python**) → Builder consumes it → dataclass discarded. | Fails at **parse time, not construction time** (line-numbered rejection before any graph mutation); and separates reader from converter exactly like `cimhub_opendss` (`dss.Line` → `convert_line`). Runtime cost is <1% of parse-to-graph (dataclass alloc ≪ CIMUnit/`pint` + `add_to_graph`); the only real cost is regen discipline on profile change. |
| **Cell delivery** | Builder `from_table` receives a **typed `<Class>Row` dataclass** (str→float/int/enum already coerced + LinkML-validated), not raw strings. | Clean, typed builder internals; no parsing inside builders; structurally mirrors `convert_line(dss_line: dss.Line)` — the Phase 8 thesis. |
| **Value+unit** | A **`Qty(value, unit, base=?)`** carrier (see §4.3). Every impedance/admittance field takes its own `Qty` — no shared `unit=` param. | User caught the ambiguity: one `unit=` can't cover `r`(ohm)/`x`(ohm)/`bch`(S). `Qty` binds value+unit indivisibly, mirroring the `.cimtbl` header `r (ohm)`. |
| **Reflection** | Plain scalar attrs, plain FKs, and units are resolved reflectively against `network.cim`. Only *synthesis* (terminals, node-vs-bus, per-phase children, templates) is hand-coded per class. | Generic across profiles for the 90% case; explicit code only where CIM structure can't be inferred. |
| **Unit context** | `%Z` / `pu` → ohm normalization lives **once, in the Builder**; `Qty` is a dumb carrier and defers relative-unit conversion to the builder, which supplies `z_base`. Base kind (system vs winding) is **declared PSSE-`CZ`-style**, not inferred. | User's top motivation ("tired of %Z→ohm by hand") + user's refinement (base must be explicit like RAW `CZ`, never guessed from whether a row has `ratedU`/`ratedS`). |
| **Front-end unification** | **One** user-facing API, full breaking change. `from_catalog` → `from_dsl`; top-level `FeederBuilder` / `SubstationBuilder` become DSL parsers. | User's call. Cascading parse: `Table ACLineSegment` invokes `ACLineSegmentBuilder`. |
| **Name lookup** | **CIM-Builder owns a `NameIndex`** (§5.5) — `dict[type, dict[str, object]]`, updated at the same call site as `add_to_graph`. Uniqueness enforced **within a class, not globally.** | `network.graph` is UUID-keyed only (linear scan today, `utils/utils.py:12-13`); cim-graph has no name index and no uniqueness check (issue [#81](https://github.com/PNNL-CIM-Tools/CIM-Graph/issues/81), stalled). `.cimtbl`'s FK-by-name model (§3.3) makes this the hot path — CIM-Builder can't wait on upstream. |

---

## 3. The `.cimtbl` format (as specified by `ieee13.cimtbl`)

### 3.1 Record forms

- **`Object <Class>: k=v, k=v, …`** — one instance, inline attributes.
- **`Table <Class>: col, col, … <newline> rows`** — a header row of column names
  (CIM attribute or association names), then whitespace/comma-delimited data
  rows. Same underlying CIM class as `Object`, chosen by cardinality.
- **`Import <file>.cimtbl`** — textual composition (catalogs, wire infos).
- **`# comment`** — line comment.
- **Blank cell** — attribute unset (`load_634` with empty `p`,`q`).

**`Object` vs `Table` is a cardinality choice, not a raggedness one.** Use
`Object` when the file declares **exactly one** instance of that class in that
context (`EnergySource`, `BaseFrequency`, `BasePower`, the one `PowerTransformer`
a `Template` line hangs off of). Use `Table` when there are **many** instances —
even if their attribute sets are ragged (blank cells are already legal in a
`Table`, per `load_634`/`load_646` above). A one-row `Table` is never wrong, but
`Object` reads better for a true singleton because the CLASS name and the sole
instance's data sit on one line — there's nothing to align into columns. This
also settles the writer's inverse (§6): the writer emits `Object` for a class
with exactly one instance in the model and `Table` for every class with more
than one, independent of how many attributes are populated.

### 3.2 Units live on the column header

`basePower (MVA)=100`, `r (ohm/mile)`, `length (ft)`, `nominalVoltage (V)`,
`r (pu)`, `r (percent)`. The unit is metadata on the **column**, applied to every
cell in it. This maps directly onto the CIMUnit `input_unit` rule
(`~/.claude/CLAUDE.md` units guide) and onto the Builder's `unit=` parameter.

### 3.3 References are by name

FK columns (`PhaseImpedance`, `PowerTransformer`, `EnergyConsumer`,
`LinearShuntCompensator`, `BaseVoltage`, `Template`) hold the `name` of a
previously- or later-declared object. Resolution is a **second pass**, so
forward references and reordering are legal.

### 3.4 Same class, multiple header shapes

`ACLineSegment` appears twice in `ieee13.cimtbl`:
- per-unit / sequence: `name, bus1, bus2, circuitNumber, r (pu), x (pu), b (pu), BaseVoltage`
- per-length / phase: `name, node1, node2, phases, length (ft), PerLengthImpedance, BaseVoltage`

The **header disambiguates** which physical representation is being built. The
`ACLineSegmentBuilder` inspects which columns are present and dispatches — exactly
as `line.py::_set_line_impedance` dispatches across sequence/matrix/geometry
today, but as a reusable method instead of importer-private code.

### 3.5 The connectivity vocabulary (the one non-reflective naming rule)

A small fixed vocabulary of column names means "make a Terminal and wire it":

| Column(s) | Meaning |
|---|---|
| `node`, `node1`, `node2` | Terminal → **ConnectivityNode** (node-breaker / detailed) |
| `bus`, `bus1`, `bus2` | Terminal → **TopologicalNode** (bus-branch / transmission) |

Terminal count = number of connectivity columns present. `sequenceNumber`
follows column order. This vocabulary is documented in the LinkML schema and
enforced by the connectivity backend; it is the single naming convention the
system relies on.

### 3.6 `phases` → per-phase child synthesis

A `phases` column (`ABCN`, `BC`) drives creation of the per-phase
child objects for that class:

| Parent | Child | Seen in `ieee13.cimtbl` |
|---|---|---|
| `ACLineSegment` | `ACLineSegmentPhase` | line 73–77 |
| `EnergyConsumer` | `EnergyConsumerPhase` | line 79–89 |
| `LinearShuntCompensator` | `LinearShuntCompensatorPhase` | line 91–96 |
| `Switch` family | `SwitchPhase` | line 106–107 |

The child rows may *also* be given explicitly as their own `Table` (e.g.
`EnergyConsumerPhase` with an `EnergyConsumer` FK). Both paths converge on the
same synthesis code in the backend. This is exactly `line.py::_create_line_phases`
generalized.

Note that `D` `Y` phaseConnection objects are enumerations of wye vs delta and not actual phase designations.

### 3.7 `Template` — true by-association, keyed on `endNumber`

`Object PowerTransformer: name=padmount_2341, Template=padmount_template`
instantiates from a `TransformerAssembly`. `TransformerAssembly` is a **proposed
CIM18 WG13 EQ construct** the user intends to standardize ("filibuster through at
the next in-person IEC meeting"), not today's AssetInfo.

**End-goal semantics (locked): a true by-association, the same way
`TransformerTankInfo` worked for `XfmrCode` conversion — but as a *pure
template*.** The instance references the template by association (no clone), and
the binding is keyed on **`endNumber`**:

```
INSTANCE                                    TEMPLATE (TransformerAssembly)
PowerTransformer padmount_2341              TransformerTank padmount
  PowerTransformerEnd pad_2341_1 ──┐          TransformerTankEnd pad_end_1
     endNumber = 1  ───────────────┼──match──▶   endNumber = 1  (phaseNeutralU=2400, …)
  PowerTransformerEnd pad_2341_2 ──┘          TransformerTankEnd pad_end_2
     endNumber = 2  ───────────────────match──▶  endNumber = 2
```

The instance rows carry only `name`, `node`, `endNumber` (see `ieee13.cimtbl`
lines 136–138); every electrical/construction attribute is resolved **by
association** from the template's `TransformerTankEnd` whose `endNumber` matches.

- The **grammar** treats `Template` as an ordinary FK column. No special syntax.
- The **builder** resolves the association and matches instance
  `PowerTransformerEnd.endNumber` ↔ template `TransformerTankEnd.endNumber`.
  This replaces the earlier "clone-or-reference flag" — the decision is made:
  **by-association, matched on `endNumber`.**

### 3.8 Matrix data is literal; compact `rmatrix`/`xmatrix` sugar is declined

`PhaseImpedanceData` rows map 1:1 to CIM `PhaseImpedanceData` objects (one per
lower-triangle matrix element), FK'd to their `PerLengthPhaseImpedance` (user's
call: "Literal CIM rows"; see `ieee13.cimtbl` lines 15–26).

**Compact `rmatrix`/`xmatrix` sugar (the OpenDSS triangular form in `API.MD`) is
explicitly declined and will not be offered.** The literal element-per-row form
is the only supported representation — it keeps the format purely reflective and
auditable (every matrix element is a visible, addressable row).

### 3.9 `Profile=` keyword sets the active CIM profile

The target profile is **`cimhub_2026`**. Because the entire reflective binder and
the editor dictionary are generated from `network.cim`, the profile must be
unambiguous *before* any row is bound. A `.cimtbl` declares it inline:

```
Profile = cimhub_2026
```

- The parser reads `Profile=` first and sets the **`CIMG_CIM_PROFILE`** env var
  (the cim-graph profile-selection mechanism) before resolving the connection's
  `network.cim`. The profile is thus fixed once, at the top of the file, and the
  whole document binds against it.
- One `Profile=` per file (or per top-level `Import` chain); a mismatch between an
  `Import`ed catalog's profile and the importing file is a fail-fast error.
- If absent, fall back to the environment's existing `CIMG_CIM_PROFILE`, or
  default to `cimhub_2026`.

This makes a `.cimtbl` **self-describing**: the file itself declares which CIM
profile its column names project, so the reader, the LinkML validator, and the VS
Code linter all agree on the class/attribute universe without out-of-band config.

---

## 4. The per-class Builder core

### 4.1 The contract every Builder presents

```python
class ObjectBuilder(ABC):
    """One CIM class, built one profile-part at a time. Stateless except for
    the object under construction. Reads network.cim; never re-derives the profile."""

    def __init__(self, network, container=None): ...

    # --- two entry points, same object ---
    def create(self, *, name: str) -> Self: ...          # power-user start
    def from_table(self, row: "<Class>Row") -> Self:  # DSL / bulk start
        """Skinny adapter: unpack a validated, typed row dataclass (§12.1 —
        NOT a dict; produced by Phase 2's LinkML gen-python) into the
        create()/add_*() calls below. This is where a Table row lands."""

    # --- profile-part population, each returns self ---
    def add_connectivity(self, **node_cols) -> Self: ...  # → connectivity backend
    def add_electrical(self, *, unit: str = 'ohm', **vals) -> Self: ...  # → %Z/pu/ohm norm
    def add_short_circuit(self, **vals) -> Self: ...
    # …one add_<profile> per CIM profile-part this class touches

    def build(self) -> "cim object": ...  # add_to_graph + return
```

### 4.2 `from_table` is the seam between DSL and core

The DSL parser does **not** know how to build an `ACLineSegment`. It parses a
`Table ACLineSegment` block into **typed `ACLineSegmentRow` dataclasses**
(LinkML `gen-python`, str→float/int/enum coerced and validated *at parse time*,
exact shape pinned in §12.1) and hands each to
`ACLineSegmentBuilder().from_table(row).build()`. All CIM knowledge lives in the
Builder. This is the "cascading parse" the user described, and it mirrors
`cimhub_opendss`'s `convert_line(dss_line: dss.Line)` exactly:

```
Table ACLineSegment ─parse+validate─▶ [ACLineSegmentRow, …] ─dispatch─▶ ACLineSegmentBuilder.from_table(row)
                                                                             │
                                             create() ─ add_connectivity() ─ add_electrical() ─ build()
```

### 4.3 The `Qty` carrier and the `%Z` / `pu` / `ohm` story (the payoff)

**`Qty` is a pure value+unit carrier** — it does *not* self-convert relative
units, because `pu`/`percent` need a base (`z_base`) that lives on other columns
of the row or on the system base, not in `Qty`. Absolute units pass straight
through; relative units are resolved **in the builder**, which has the context.
Base kind (system vs winding) is declared PSSE-`CZ`-style, never inferred.

```python
@dataclass(frozen=True)
class Qty:
    """Value + unit carrier. Mirrors the .cimtbl header 'r (ohm)'.

    base: which base a RELATIVE unit (pu/percent) is against.
      None → sensible default per unit (percent→'winding', pu→'system');
      a table-level baseKind sets the default, and this field OVERRIDES it.
    """
    value: float
    unit: str
    base: str | None = None      # 'system' | 'winding' | None

    def is_relative(self) -> bool:
        return self.unit in ('pu', 'percent')

    def to_cimunit(self, cim_cls, *, z_base=None):
        if not self.is_relative():
            return cim_cls(self.value, self.unit)      # ohm, S, ohm/mile → straight through
        if z_base is None:                             # fail fast, never silently wrong
            raise ValueError(f"{self.unit!r} value needs a base; builder supplied none")
        ohm = self.value * z_base if self.unit == 'pu' else self.value / 100 * z_base
        return cim_cls(ohm, 'ohm')


def add_electrical(self, *, r: Qty, x: Qty, bch: Qty | None = None,
                   base: str | None = None):     # table-level baseKind default
    z_base = self._resolve_z_base(r.base or base)  # 'winding' → ratedU²/ratedS
                                                   # 'system'  → base_kv²/base_mva
    self._set('r', r.to_cimunit(cim.Resistance, z_base=z_base))
    self._set('x', x.to_cimunit(cim.Reactance,  z_base=z_base))
    if bch is not None:
        self._set('bch', bch.to_cimunit(cim.Susceptance))   # S: no base needed
```

Every impedance field carries **its own** `Qty` — no shared `unit=` (the
ambiguity the user caught: `r`/`x` are ohm, `bch` is siemens). The `.cimtbl`
header `r (ohm)` and the Python `Qty(0.01, 'ohm')` are the same thing.

- `sub3_end1` (`r (ohm)`) → absolute, straight through.
- `xfm_end1` (`r (percent)`) → relative, `base='winding'` → `z_base = ratedU²/ratedS`.
- `line_1_2` (`r (pu)`) → relative, `base='system'` → `z_base = base_kv²/base_mva`
  from the row's `BaseVoltage` FK and the file's `Object BasePower`.

The user hand-authors `%Z` or `pu`; the backend does the algebra **once**, for the
DSL and for a Python power user alike. **Fail-fast**: a relative unit reaching
conversion with no resolvable base raises with the class/field named — never a
silent wrong write (per `BUILDER_API.md` error rules).

**Base-kind declaration (PSSE `CZ` analog).** Base is declared, not guessed:
- **Table/row level** — an optional `baseKind` column (or an `add_electrical(base=)`
  param) sets the default for all relative values in that table, the way RAW puts
  `CZ` once per transformer.
- **Carrier level** — a `Qty(..., base='winding')` **overrides** the table default
  for the one value that differs.
- **Default per unit** when neither is given: `percent`→`winding`, `pu`→`system`.

### 4.4 Builder modules are packages, split by construction style

**Problem this fixes.** `cimhub_opendss/importer/lines/line.py` is 531 lines with
one public entry point (`convert_line`) and ten private module-level `_helpers`
covering four genuinely different construction styles (per-length + matrix
impedance, per-length + wire/spacing geometry, sequence/pu impedance, earth
resistivity) with no structural grouping between them — a reader has to hold the
whole file in their head to find which `_functions` belong to which style. This
is exactly the readability problem the design goals (§0) rule out.

**The fix: a Builder is a *package*, not a module — one file per construction
style, imported into a thin class body.** Each CIM class that has multiple
`.cimtbl` header shapes (§3.4) gets one file per shape, plus a `base.py` holding
the class itself:

```
builders/
  line/
    __init__.py          # re-exports ACLineSegmentBuilder
    base.py               # class ACLineSegmentBuilder(ObjectBuilder): create/build/from_table dispatch
    by_matrix.py           # add_electrical() for PerLengthPhaseImpedance / PhaseImpedanceData rows
    by_sequence.py          # add_electrical() for bus1/bus2 + r,x,b (pu) rows
    by_geometry.py           # add_electrical() for wire + ConductorDistanceSpacing rows (future)
  transformer/
    __init__.py
    base.py                # class PowerTransformerBuilder(ObjectBuilder)
    by_end_data.py          # add_electrical() from literal PowerTransformerEnd rows (ohm/percent)
    by_template.py           # Template=/TransformerAssembly resolution (§3.7, endNumber match)
```

`base.py` holds the class declaration and the dispatch: `from_table` inspects
which columns are present (§3.4) and calls the one `add_electrical` variant that
applies — imported as a plain function from the sibling module and bound as a
method, or mixed in via a small `Mixin` class per file (whichever reads more
like ordinary Python; no metaclass machinery either way, per `~/.claude/CLAUDE.md`
KISS/no-over-abstraction). The point is **one file, one construction style,
readable start to finish** — never "scroll past nine unrelated `_helpers` to find
the one that handles matrices."

This directly abstracts `line.py`: `_set_line_impedance`'s three-way dispatch
(sequence/matrix/geometry) becomes the `base.py` dispatch, and each branch's
body becomes its own `by_*.py`. Applies to any class with >1 header shape
(`ACLineSegment`, `PowerTransformerEnd` ohm-vs-percent-vs-template); a class with
only one shape (`EnergyConsumer`, `LinearShuntCompensator`) stays a single file —
this is a split for genuine construction-style variety, not a mandatory pattern
per class (YAGNI).

---

## 5. The connectivity backend (the heavy component)

One module, shared by every Builder and both front ends. Responsibilities:

1. **Semantic disambiguation** — `node*` → `ConnectivityNode`, `bus*` →
   `TopologicalNode`. This is the one thing the parser can't infer from the
   profile; it lives here explicitly.
2. **Auto-vivification** — a referenced node/bus name that was never declared is
   created on first use (IEEE13 never declares its buses). Reorder-tolerant
   because resolution is deferred to the second pass.
3. **Terminal synthesis** — one `Terminal` per connectivity column, correct
   `sequenceNumber`, wired to the resolved node. Wraps existing
   `utils.terminal_to_node()`.
4. **Per-phase child synthesis** — `phases=ABCN` on an `ACLineSegment` →
   4 `ACLineSegmentPhase` with correct `SinglePhaseKind` and `sequenceNumber`.
   Generalizes `line.py::_create_line_phases` / `_attach_wire_phases`.

### 5.5 The name/mRID index (CIM-Builder owns it, since cim-graph doesn't)

**Every** FK cell in `.cimtbl` (§3.3) — `node1`, `bus1`, `PerLengthImpedance`,
`BaseVoltage`, `Template`, `EnergyConsumer`, … — is a **name-based lookup**
against the live graph. That lookup is the load-bearing operation of the whole
format, and today it's expensive:

- `network.graph` is `dict[type, dict[UUID, object]]` (cim-graph
  `GraphModel.graph`, `cimgraph/models/graph_model.py:18,26`) — keyed by UUID,
  **not** by name. A name lookup is a **linear scan** over one class's dict
  (`utils/utils.py:12-13` already does exactly this: `for node_obj in
  network.graph[cim.ConnectivityNode].values(): if node_obj.name == node`).
  With `Import`-composed catalogs (§3.3) and templates resolved per-row (§3.7),
  this scan runs on the hot path of every parse, repeatedly, per class.
- `add_to_graph` (`graph_model.py:51-57`) keys strictly on `(type(obj),
  obj.identifier)` and **silently no-ops on a UUID collision** — line 56 is `if
  obj.identifier not in graph[type(obj)]:`, so a second object with a
  colliding UUID is dropped with no error, no warning. There is no name or
  mRID uniqueness check anywhere in cim-graph today.
- The UUID itself is already deterministic from name — `identity.py`'s
  `UUID_Meta.generate_uuid` seeds `Random(seed).getrandbits(128)` from
  `f'{ClassName}:{name}'` when no explicit mRID/URI is given
  (`identity.py:293-294,120-121`). So **within one class, `name` already
  determines the UUID** — the missing piece is a fast reverse index
  (`name → UUID`/object) and a check that catches a second, different `name`
  that happens to collide, or the same `name` reused for two different
  intended objects.

**This was raised upstream and stalled: cim-graph issue
[#81](https://github.com/PNNL-CIM-Tools/CIM-Graph/issues/81)** ("create a UUID
manager class that can keep track of master set of uuids for uniqueness and
also whether a certain object has been queried for") — filed by the user,
unassigned in practice, not a cim-graph dev priority.

**Decision: CIM-Builder owns this, not cim-graph.** `.cimtbl` is what actually
needs it on every parse; cim-graph's own callers (SPARQL/RDF hydration) don't
lean on name lookups the way a name-native authoring format does. Rather than
wait on upstream, add an index **alongside** `network.graph`, populated by the
same `add_to_graph` call every Builder already makes:

```python
# core/graph_write.py — one new structure, updated at the same call site as add_to_graph()

@dataclass
class NameIndex:
    """name -> object, scoped per class. Built incrementally as objects are
    added; not a cim-graph change — CIM-Builder maintains this next to
    network.graph, the same way network.graph itself is populated."""
    by_class: dict[type, dict[str, object]] = field(default_factory=dict)

    def add(self, obj) -> None:
        bucket = self.by_class.setdefault(type(obj), {})
        existing = bucket.get(obj.name)
        if existing is not None and existing.identifier != obj.identifier:
            raise ValueError(
                f"duplicate name {obj.name!r} within {type(obj).__name__}: "
                f"{existing.identifier} vs {obj.identifier}")
        bucket[obj.name] = obj

    def get(self, cim_cls: type, name: str) -> object | None:
        return self.by_class.get(cim_cls, {}).get(name)   # O(1), vs O(n) scan today
```

- Lives on the network/model object as `network.name_index` (or
  `network.mrid_map` — naming TBD, not load-bearing) built and maintained by
  CIM-Builder's `graph_write.add_to_graph()` wrapper, which calls both
  `network.add_to_graph(obj)` **and** `name_index.add(obj)` in one place — every
  Builder already routes through this wrapper (§2 diagram), so there's exactly
  one call site to update, not one per builder.
- **Uniqueness scope: within a class, not global (locked).** Two different
  classes may legitimately share a `name` string in real feeders (a
  `LoadResponseCharacteristic` named the same as an `EnergyConsumer`, say);
  nothing in `.cimtbl` or CIM requires cross-class uniqueness, and enforcing it
  would reject legal files. `NameIndex` is scoped `dict[type, dict[str, object]]`
  to match — same granularity as `network.graph` itself. **User's call:**
  "arguably sloppy, but matches how power engineers think" — a `name` is only
  ever disambiguated by its class in practice (nobody confuses a bus named
  `634` with a device named `634`), so the index should mirror that mental
  model rather than impose a stricter global namespace no one asked for.
- Every FK resolution in the connectivity backend and in `from_table` routes
  through `name_index.get(cls, name)` instead of a `.values()` scan. This is a
  straight drop-in for `utils/utils.py`'s existing scan and every future FK
  lookup — no behavior change, only complexity (`O(1)` vs `O(n)` per lookup).
- **Duplicate-name detection is a byproduct, not the primary goal** — but a
  fail-fast one: two `.cimtbl` rows of the same class emitting the same `name`
  with different data now raises immediately (`NameIndex.add`) instead of
  silently colliding in `network.graph` per `add_to_graph`'s current no-op.
- If cim-graph #81 ever ships, `NameIndex` becomes a thin wrapper delegating to
  it; CIM-Builder is not blocked waiting for that, and nothing above is
  cim-graph-version-sensitive (it never reaches into cim-graph internals beyond
  the existing `obj.identifier`/`obj.name`/`type(obj)` contract).

This backend is the direct abstraction of the CIM-construction helpers currently
buried in `cimhub_opendss/importer/lines/line.py`
(`create_terminals_for_equipment`, `_create_line_phases`, `_attach_wire_phases`,
`_PHASE_LABEL_TO_KIND`, `_link_per_length_impedance`). Those ~530 lines are ~80%
CIM-assembly logic that has nothing to do with OpenDSS.

---

## 6. Round-trip: the `cimgraph → .cimtbl` writer (Phase R)

A writer that serializes a live `cimgraph` model back to `.cimtbl`. This makes
`.cimtbl` a **round-trippable** representation, which is what unlocks the
strategic options in §7.

**Multi-file emission, ordered by package/dependency.** The writer does not emit
one flat file — it emits a **set** of `.cimtbl` files ordered so that every file's
references are already declared by an earlier `Import`. The order follows the
reference-dependency (catalog → template → instance) topology:

```
asset_infos.cimtbl     # OverheadWireInfo, cable infos, PowerTransformerInfo (no deps)
templates.cimtbl       # TransformerAssembly / TransformerTank(+Ends+Windings)  → Imports asset_infos
per_length.cimtbl      # PerLengthPhaseImpedance + PhaseImpedanceData, spacings
lines.cimtbl           # ACLineSegment(+Phase)                → Imports per_length
transformers.cimtbl    # PowerTransformer(+End)               → Imports templates
loads.cimtbl           # EnergyConsumer(+Phase)
shunts.cimtbl          # LinearShuntCompensator(+Phase)
switches.cimtbl        # Switch / Fuse / Sectionaliser(+SwitchPhase)
inverters.cimtbl       # PowerElectronicsConnection (+PV/Battery)
<feeder>.cimtbl        # top-level: Profile=, EnergySource, BaseVoltage/Freq/Power,
                       #            and Import lines for all of the above
```

The by-package split mirrors how the *reader* composes via `Import`, and matches
CIM-Asset-Manager's output (§7.1) — `asset_infos.cimtbl` and `templates.cimtbl`
are the files a datasheet-extraction pipeline produces and a feeder `Import`s.

Design notes:
- **Group by class, by cardinality (§3.1).** A class with exactly one instance in
  the model emits as `Object`; a class with more than one emits as `Table` —
  raggedness (blank cells) never forces a split, since `Table` already tolerates
  blanks. (Mirrors the reader's two forms; not a heuristic, a fixed rule.)
- **Units on export** via `.to(header_unit)` — never manual scaling
  (`~/.claude/CLAUDE.md`). The writer picks a canonical display unit per attribute
  (kV, MW, ohm) and emits it in the header.
- **Connectivity inverse** — emit `node1`/`node2` columns by walking
  `Terminal → ConnectivityNode.name`, collapsing synthesized terminals/phases
  back to the compact `phases` column where they match the synthesis rule.
- **Determinism** — stable, documented order: **file order by package
  dependency**, then within each file by class, then by name. Two writes of the
  same model are byte-identical. Hard requirement for the diff/lint use case.

Round-trip test: `.cimtbl → graph → .cimtbl` is byte-identical for `ieee13` and
`ieee14`; `graph → .cimtbl → graph` is graph-isomorphic.

---

## 6.5 The VS Code extension (`cimtbl-vscode`, Phase V)

A VS Code language extension for `.cimtbl`, modeled on **PNNL-dss**
(`~/PNNL-dss`) — the same proven architecture, retargeted at our format.

### 6.5.1 What PNNL-dss does, and why its shape fits us

PNNL-dss is **fully data-driven**. The TypeScript is generic; all the
intelligence lives in a generated JSON dictionary:

```
OpenDSS JSON schema ──config_generator.py──▶  resources/opendss-elements.json
                                                      │
                                    ┌─────────────────┼─────────────────┐
                                    ▼                 ▼                 ▼
                             validator.ts       hover.ts       completion.ts
                          (diagnostics)     (descriptions)   (IntelliSense)
                                    ▲
                       syntaxes/opendss.tmLanguage.json  (TextMate highlighting)
```

The validator (`opendss-validator.ts`) parses each line, looks the element up in
the dictionary, and emits `vscode.Diagnostic`s for: unknown element, unknown
parameter, missing required parameter, wrong type/range/enum, and parameter-order
violations. Hover and completion read the **same** dictionary.

### 6.5.2 The key adaptation: our dictionary is generated from the profile

PNNL-dss hand-generates its dictionary from OpenDSS's schema. **We already have
the schema** — it's `network.cim` plus the LinkML synthesis annotations from
Phase 2. So the `.cimtbl` extension's dictionary is a *build artifact*, not a
hand-maintained file:

```
network.cim (profile)  +  LinkML schema (§8.1 dsl/schema/)
                    │
        cimbuilder export-editor-schema        ← new CLI (Phase V)
                    ▼
        cimtbl-elements.json   { "ACLineSegment": { attributes: {...}, associations: {...},
                                                     connectivity_cols: [...], phase_child: ... }, ... }
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   validator    hover      completion       (TypeScript, generic — ported from PNNL-dss)
        ▲
   cimtbl.tmLanguage.json  (Object|Table|Import keywords, class names, (unit) suffix, comments)
```

**This is the payoff of the LinkML-as-validator decision (§2.1):** the *same*
schema that gates the file server-side (Phase 2 Python) drives the editor linter
(Phase V TypeScript). The two validators agree **by construction** — an
`.cimtbl` that lints clean in the editor validates clean in the loader, because
both consume one generated dictionary. No drift.

### 6.5.3 What the linter checks (`.cimtbl`-specific diagnostics)

Beyond PNNL-dss's element/parameter/type/enum checks, the `.cimtbl` linter adds
diagnostics that only make sense for our format:

- **Unknown CIM class** after `Object`/`Table` (dictionary lookup against the profile).
- **Unknown column** — attribute or association not on that CIM class; suggest the
  closest valid name (mirrors the Phase 2 fail-fast message).
- **Unit sanity** — `(unit)` in a header must be a unit `pint` accepts for that
  attribute's dimension (`r (kV)` on a resistance column is an error; `r (percent)`
  / `(pu)` / `(ohm)` are all valid resistance inputs).
- **Table arity** — a data row's cell count must match its header column count.
- **Unresolved reference** — an FK cell (`PerLengthImpedance=mtx601`) whose target
  `name` is declared nowhere in this file or its `Import`s → warning (it may be
  auto-vivified, or a typo — same judgment as the connectivity backend).
- **Duplicate name** within a class.
- **`Import` target missing** on disk.

### 6.5.4 Extension features (parity with PNNL-dss + our additions)

| Feature | PNNL-dss | `cimtbl-vscode` |
|---|---|---|
| Syntax highlighting | TextMate grammar | TextMate grammar (`Object`/`Table`/`Import`, class names, headers, units, comments) |
| Diagnostics | element/param/type/enum/order | §6.5.3 (profile-aware) |
| Hover | element + param descriptions | CIM class + attribute descriptions **from the profile's own docstrings** + CIMUnit dimension |
| Completion | element types, params | class names after `Object`/`Table`; column names in a header; enum values; `Import` file paths |
| Theme | OpenDSS Dark | reuse / adapt |
| **Format** | — | **`.cimtbl` formatter** — align table columns, canonical spacing (leans on the deterministic writer's rules) |
| **Go-to-definition** | — | jump from an FK cell to the row that declares that `name` |

### 6.5.5 Repo placement

Standalone repo `cimtbl-vscode` (like PNNL-dss is its own repo), **not** vendored
into CIM-Builder — a TS/npm project has a different toolchain and release cadence
(`vsce package` → VSIX → marketplace). CIM-Builder owns the `export-editor-schema`
CLI that *produces* the dictionary; the extension *consumes* a committed copy of
it (regenerated when the profile or LinkML schema changes). One-way dependency,
same direction as everything else.

---

## 7. Strategic option: `.cimtbl` as a convergence / repair target

> **Status: strategic option, NOT committed in this plan.** Recorded here because
> it changes how much the writer's fidelity matters. Decide after Phase R proves
> the round-trip.

Two downstream possibilities the round-trip opens up:

### 7.1 Converters target `.cimtbl` (CIMHub Phase 2)

The committed near-term win (§8 Phase 2): CIMHub importers stop hand-constructing
CIM objects and instead call the CIM-Builder core
(`ACLineSegmentBuilder`, etc.). `line.py`'s ~530 lines become ~80 lines of
DSS-specific mapping + Builder calls.

The *further* option: an importer could emit `.cimtbl` as an intermediate,
inspectable artifact (`dss → .cimtbl → graph`) instead of going straight to a
live graph — giving every conversion a diffable, reviewable checkpoint.

### 7.1b CIM-Asset-Manager emits `.cimtbl` (committed retarget)

**Decision (user):** retarget CIM-Asset-Manager so its extraction target is
`.cimtbl`, not JSON or Parquet. PDF datasheets extract into `.cimtbl` files —
specifically the catalog/template files the writer already defines in §6:
`asset_infos.cimtbl` (`OverheadWireInfo`, cable infos, `PowerTransformerInfo`)
and `templates.cimtbl` (`TransformerAssembly`/`TransformerTank`). A datasheet
becomes a small, human-checkable table that a feeder `Import`s.

Why this is the right target rather than JSON/Parquet:
- **Auditability** — an extracted datasheet is a diffable table a domain expert
  reads directly; a reviewer can compare it to the PDF line by line. JSON/Parquet
  are neither hand-readable nor `git diff`-friendly.
- **One schema, no adapter** — the extracted `.cimtbl` is validated by the *same*
  Phase 2 LinkML gate and linted by the *same* Phase V editor extension as any
  hand-authored file. Extraction correctness is checked by the loader we already
  build; there is no separate JSON→CIM mapping layer to maintain.
- **Direct consumption** — the output `Import`s straight into a feeder with no
  conversion step. The asset library *is* CIM-Builder input.

This makes CIM-Asset-Manager a *producer* on the same one-way dependency as every
other component: it writes `.cimtbl`; CIM-Builder reads it. Fidelity bar is the
`asset_infos`/`templates` subset of the round-trip test (§6, Phase R).

### 7.2 CIM-Repair targets `.cimtbl` instead of live RDF/XML

CIM-Repair (`~/CIM-Repair`) today repairs **live CIM graphs** and its ROADMAP
explicitly scopes round-trip *out* ("Export to anything but CIM XML (round-trip
stays a `cimhub_*` concern)", line 266). The possibility the user raised: a
textual, diffable, lintable `.cimtbl` could be a better repair substrate than
live RDF/XML — you can `git diff` a repair, a human can eyeball a 25,046-instance
defect as a table, and a journal entry can point at a line number.

**Honest tension to resolve before adopting this:**
- CIM-Repair's ROADMAP is a measured "plan of record" with numeric exit criteria
  on *live models*; retargeting to `.cimtbl` is a real scope change, not a free
  win. It would need buy-in from that repo's owner and a re-examination of line
  266.
- The plausibility gate (Stage 6) needs a **solver** on a real network, so
  `.cimtbl` would be the *edit/inspect* representation, with the graph still
  materialized for solving. `.cimtbl` complements the graph; it doesn't replace
  the solver path.
- Fidelity bar: `.cimtbl` must round-trip **losslessly** for the classes
  CIM-Repair touches, or a repair could silently drop data. Phase R's byte-
  identical test is the precondition.

**Recommendation:** build the writer (Phase R) and the lossless round-trip test
first. *Then* open the CIM-Repair conversation with a working artifact in hand,
rather than committing either repo to it now.

---

## 8. The multi-phase plan (one week)

Phases are dependency-ordered, each a self-contained unit of work with a concrete
exit criterion measured on `ieee13.cimtbl` / `ieee14.cimtbl` (real feeders, not
toys). Lettered sub-phases can run same-day. **The exact data shape each phase
hands to the next — not just its exit criterion — is pinned in §12; implement
against §12, not just this table.**

| Phase | Name | Depends on | Exit criterion (measured) |
|---|---|---|---|
| **0** | Design lock + repo scaffold | — | This doc reviewed; new package tree (§8.1) created; `uv sync` clean; empty modules import. |
| **1** | Lark grammar → records | 0 | `ieee13.cimtbl` **and** `ieee14.cimtbl` parse to the intermediate record list; every `Object`/`Table`/`Import`/comment/blank-cell/`(unit)` case covered by a grammar test; ambiguity check passes. No CIM yet. |
| **2** | LinkML validation gate + dataclass | 1 | LinkML schema for the `ieee13` class set; every record validates or fails with a profile-anchored message; a deliberately-broken column name fails fast naming the closest valid attribute. Records → validated dataclasses. |
| **3** | Graph-write core + reflective binder + `NameIndex` | 2 | Simplest real classes end-to-end into a live `cimgraph` model: `BaseVoltage`, `BaseFrequency`, `BasePower`, `EnergySource`. `network.cim` read once; plain scalar attrs + units land correctly (verified via `.to()`); `NameIndex` (§5.5) populated at the same `add_to_graph` call site, O(1) name lookup proven, duplicate-name-same-class raises. |
| **4** | Connectivity backend | 3 | `ACLineSegment` with `node1`/`node2`/`phases` → terminals + N `ACLineSegmentPhase`; undeclared nodes auto-vivified; `bus*` → `TopologicalNode` disambiguation proven on the `line_1_2` sequence row. **This is the make-or-break phase.** |
| **5** | Per-class Builders — PDE/PCE breadth | 4 | Builders for the `ieee13` population: `ACLineSegment`, `EnergyConsumer`(+Phase), `LinearShuntCompensator`(+Phase), `PowerTransformer`/`PowerTransformerEnd`, `Switch`/`Fuse`/`Sectionaliser`(+`SwitchPhase`), `PowerElectronicsConnection`(+PV/Battery). Each has `from_table`. |
| **5b** | `%Z`/`pu`/`ohm` normalization | 5 | `xfm_end1` (`r (percent)`) and `sub3_end1` (`r (ohm)`) both produce correct ohms via one `add_electrical`; `pu` without base fails fast. |
| **6** | Catalog + matrix + templates | 5 | `PerLengthPhaseImpedance` + literal `PhaseImpedanceData` rows; `Import wire_infos.cimtbl`; `Template`/`TransformerAssembly` instantiation (clone-or-ref flag). `ieee13.cimtbl` builds a **complete** feeder graph. |
| **7** | `cimbuilder/__init__.py` public surface + `from_dsl` | 5b, 6 | `from cimbuilder import load_cimtbl, ACLineSegmentBuilder, …` works; `FeederBuilder`/`SubstationBuilder` reworked as DSL parsers; old `new_*`/`from_catalog` surface removed (breaking, per user). `ieee13.cimtbl` loads via the public API in one call. |
| **R** | `cimgraph → .cimtbl` writer | 6 | `ieee13.cimtbl → graph → .cimtbl` **byte-identical**; `graph → .cimtbl → graph` isomorphic; deterministic across two runs. |
| **V** | VS Code extension (`cimtbl-vscode`) + `export-editor-schema` CLI | 2 (schema), 7 (CLI) | `cimbuilder export-editor-schema` emits `cimtbl-elements.json` from the profile+LinkML; extension (ported from PNNL-dss) highlights `ieee13.cimtbl`, flags an injected unknown-column / bad-unit / arity error, offers class + column completion; editor diagnostics **agree with** the Phase 2 loader on the same file. |
| **8** | CIMHub proof-of-value (spike) | 7 | A branch of `cimhub_opendss` `line.py` rewritten to call `ACLineSegmentBuilder`; DSS-specific code shrinks measurably (target: ~530 → <150 lines) with importer tests still green. Validates the "converters use the builder" thesis. |

Phases 0–7 + R are the CIM-Builder deliverable for the week. **Phase V** (the VS
Code linter) is parallelizable once Phase 2's LinkML schema exists — the extension
is a separate TS repo, so it doesn't block the Python phases and can be built by a
different track. Phase 8 is the spike that proves the CIMHub Phase 2 in §7.1 is
real; the full CIMHub migration is separate, later work.

### 8.1 Proposed repo structure

```
cimbuilder/
  __init__.py                 # Phase 7: public surface (load_cimtbl, *Builder, writer)
  dsl/
    grammar.lark              # Phase 1: FIXED grammar
    parser.py                 # Phase 1: Lark → records
    records.py                # Phase 1: intermediate record dataclasses
    validate.py               # Phase 2: LinkML gate
    writer.py                 # Phase R: cimgraph → .cimtbl
    schema/                   # Phase 2: LinkML schemas (validation + docs)
      main.yaml
      classes/                #   one YAML per CIM class family
      types/                  #   shared units + enums
  core/
    graph_write.py            # Phase 3: set_attr / link / add_to_graph / resolve
    name_index.py             # Phase 3: NameIndex (§5.5) — name->object, per class
    binder.py                 # Phase 3: reflective column → attr/assoc/synthesis
    connectivity.py           # Phase 4: THE backend (node/bus/terminal/phase)
    units.py                  # Phase 5b: %Z / pu / ohm normalization helpers
  builders/                   # Phase 5: one module OR package per CIM class family
    base.py                   #   ObjectBuilder ABC + builder_base mixin
    line/                      #   ACLineSegmentBuilder — package (§4.4): >1 header
      __init__.py              #     shape (matrix/sequence/geometry) → one file
      base.py                  #     per construction style, not one 500-line file
      by_matrix.py
      by_sequence.py
    consumer.py               #   EnergyConsumerBuilder
    shunt.py                  #   LinearShuntCompensatorBuilder
    transformer/               #   PowerTransformer/End — package (§4.4): ohm vs
      __init__.py               #     percent vs Template differ in construction
      base.py
      by_end_data.py
      by_template.py
    switch.py                 #   Switch / Fuse / Sectionaliser
    inverter.py               #   PowerElectronicsConnection family
    source.py                 #   EnergySource / base objects
  assembly/                   # substation / feeder orchestration (was substation_builder/)
    feeder.py                 # Phase 7: FeederBuilder as DSL parser
    substation.py             # Phase 7: SubstationBuilder as DSL parser
  utils/                      # kept: terminal_to_node, get_base_voltage, get_source_bus
  development/                # these docs
tests/
  dsl/  core/  builders/  roundtrip/
  fixtures/  ieee13.cimtbl  ieee14.cimtbl  wire_infos.cimtbl
```

---

## 9. What this replaces

- The `feature/23` phase roadmap (phases 0–11, one add-per-profile builder) is
  **superseded** where it conflicts. The `ObjectBuilder` / `add_<profile>`
  *contract* survives (§4); the *phasing* and the "DSL-less" assumption do not.
- `from_catalog` → **`from_dsl`** (user's call).
- `object_builder/` `new_*()` functions → **removed**; their bodies are the
  blueprint for the Builder methods, then deleted (breaking change, per user).
- `substation_builder/` classes → **`assembly/`**, reworked as DSL parsers,
  still class-based (a substation is a composition, not one profile-built object).
- `catalog_parser.py` (legacy JSON) → replaced by `dsl/` + `Import`.

---

## 10. Open questions (decide before or during the phase they gate)

1. **LinkML generation — RESOLVED.** `gen-python` the validation dataclasses from
   the schema (CIMHub pattern) — one generated dataclass per CIM class, shape
   pinned in §12.2. Not hand-written; regenerated on profile/schema change.
2. **Writer table-grouping — RESOLVED.** Not a raggedness heuristic: `Object` for
   a class with exactly one instance, `Table` for a class with more than one
   (§3.1, §6). Deterministic by construction; nothing left to decide.
3. **`.cimtbl` as CIM-Repair target** — §7.2. Needs the CIM-Repair owner and a
   re-examination of ROADMAP line 266. *Recommendation: defer until Phase R.*
4. **Profile pin — RESOLVED.** Target profile is **`cimhub_2026`** (matches
   `line.py`, the Phase 8 abstraction target). Each `.cimtbl` is self-describing:
   a top-level **`Profile = cimhub_2026`** keyword (§3.9) sets `CIMG_CIM_PROFILE`
   before binding, so the file names its own profile and the loader resolves
   `network.cim` once from it. *Remaining verification (not an open decision):*
   confirm `ieee13`'s class set — esp. `TransformerAssembly`, `EnergyConsumerPhase`,
   `PhaseImpedanceData` — exists under `cimhub_2026` before Phase 5, and update the
   `ieee13.cimtbl` sample (which still carries some `cimhub_2023`-era spellings) to
   the `cimhub_2026` names.
5. **`NameIndex` attribute name and upstream path** — §5.5 owns the mechanism
   (`dict[type, dict[str, object]]`, class-scoped uniqueness); not yet decided:
   (a) exposed as `network.name_index` or `network.mrid_map` — cosmetic, pick at
   Phase 3; (b) whether to eventually upstream it into cim-graph as a resolution
   to issue #81 once it's proven here, or keep it a CIM-Builder-only layer
   permanently — no need to decide before Phase 3, cim-graph's `add_to_graph`
   contract is untouched either way.

---

## 11. Related documents

- `BUILDER_API.md` — the fluent chain (this doc extends it with `from_table`/`from_dsl`).
- `ARCHITECTURE.md` — `ObjectBuilder` contract and profile-identity rule.
- `PROFILE_TYPING.md` — per-method profile-scoped typing.
- `UNITS.md` — CIMUnit in `add_electrical`; per-unit context.
- `ASSET_ENRICHMENT_CONCEPT.md` — the AssetInfo/enrichment layer (adjacent, not this).
- `~/CIMHub_2_0/cimhub_core/.../LINKML_TEMPLATE.md` — LinkML annotation vocabulary.
- `~/CIMHub_2_0/cimhub_opendss/.../importer/lines/line.py` — the ~530 lines Phase 8 abstracts.
- `~/CIM-Repair/.development/ROADMAP.md` — §7.2 strategic-option target (line 266 tension).
- [`CIM-Graph#81`](https://github.com/PNNL-CIM-Tools/CIM-Graph/issues/81) — the
  stalled upstream UUID-manager ask that §5.5's `NameIndex` addresses locally.
- `~/CIM-Graph/cimgraph/data_profile/identity.py` — deterministic
  name→UUID seeding (`UUID_Meta.generate_uuid`, §5.5) that `NameIndex` builds on.
- `~/CIM-Graph/cimgraph/models/graph_model.py` — `GraphModel.graph` (UUID-keyed
  only) and `add_to_graph`'s silent-no-op-on-collision behavior (§5.5).
- `~/PNNL-dss/` — the VS Code extension template for §6.5 / Phase V. Key files:
  `package.json` (manifest: `languages`/`grammars`/`themes` contributions),
  `src/opendss-validator.ts` (diagnostics from a JSON dictionary),
  `src/extension.ts` (activation + document listeners),
  `syntaxes/opendss.tmLanguage.json` (TextMate grammar),
  `script/config_generator.py` (schema → dictionary — the analog of our
  `export-editor-schema` CLI).

---

## 12. Interface contracts between phases (the handshakes)

**Why this section exists.** §8's phase table pins *exit criteria* (what must
work), not *call signatures* (what shape phase N hands to phase N+1). Two phases
built independently against only the prose above could each make a locally
reasonable but mutually incompatible choice — e.g. Phase 1 emitting an untyped
record and Phase 5 expecting a typed dataclass. This section is the literal
contract, written once, so every phase is implemented against the same shape.
Nothing here is a new decision — it is §3/§4/§5's decisions made executable.
**Any surviving `row: dict` or informal `<Class>Row` mention elsewhere in this
doc is prose shorthand for the exact shapes below**, not a competing spec.

### 12.1 Phase 1 → Phase 2 : parser output

```python
# dsl/records.py

@dataclass
class RawRecord:
    """One Object/Table row, straight off the grammar. Every cell is still a
    str (or None for a blank cell) — no CIM knowledge, no coercion. Phase 2
    is the only consumer."""
    form: Literal['Object', 'Table']
    cim_class: str                       # e.g. "ACLineSegment" — not yet resolved
                                          # against network.cim; just the grammar token
    fields: dict[str, str | None]        # column/key -> raw cell text, blank = None
    units: dict[str, str | None]         # column -> unit suffix text, e.g. {"r": "ohm"}
    source_file: str
    source_line: int                     # for fail-fast, line-numbered errors (§2.1)
```

`Import` records resolve inline during parsing (textual composition, §3.3) and
never reach Phase 2 as their own `RawRecord` — by the time Phase 1 returns, the
record list is already the fully-composed file. `Profile=` (§3.9) is consumed
even earlier, before any `RawRecord` is built, since it must be known to resolve
`network.cim`.

### 12.2 Phase 2 → Phase 3/5 : the validated row

```python
# generated per CIM class by LinkML gen-python, e.g. dsl/schema/generated/ac_line_segment.py

@dataclass
class ACLineSegmentRow:
    """One validated ACLineSegment record. Every field is already the correct
    Python type (str/float/int/enum) and passed the LinkML schema — Phase 2's
    output, Phase 5's Builder input. Units are pre-bound into Qty for any
    field the schema marks as a physical quantity (§4.3); plain scalars and
    FK-name strings pass through untyped-for-CIM (resolution is Phase 4/5's job,
    not Phase 2's)."""
    name: str
    # --- header-shape-dependent fields (§3.4): only the columns present in
    # THIS record's header are non-None; absent columns are None, not missing
    # attributes -- one generated dataclass per CIM class, shared across all
    # header shapes of that class.
    node1: str | None = None
    node2: str | None = None
    bus1: str | None = None
    bus2: str | None = None
    phases: str | None = None
    length: Qty | None = None
    r: Qty | None = None
    x: Qty | None = None
    b: Qty | None = None
    PerLengthImpedance: str | None = None     # FK by name, unresolved
    BaseVoltage: str | None = None            # FK by name, unresolved
    circuitNumber: int | None = None
    source_file: str = ''
    source_line: int = 0
```

This is the seam named in §4.1/§4.2/§4.4 as `"<Class>Row"` — one generated
dataclass per CIM class (not per header shape). `from_table(row)` receives
exactly this and is solely responsible for inspecting which optional fields are
populated to select the right `by_*.py` construction style (§3.4/§4.4) — the
dataclass itself carries no "which shape am I" flag; presence/absence of fields
*is* the dispatch signal, same as today's `line.py::_set_line_impedance`.

FK fields (`PerLengthImpedance`, `BaseVoltage`, `node1`, …) are **plain
`str | None`** at this stage — Phase 2 validates that the referenced name syntax
is legal, not that the reference resolves (resolution is deferred, §3.3). Phase
3/5's `NameIndex.get(cls, name)` (§5.5) is the only thing that turns these
strings into live objects, and it does so lazily, inside `add_connectivity`/
`from_table`, never inside Phase 2.

### 12.3 Phase 3 → Phase 4/5 : the graph-write core surface

```python
# core/graph_write.py — the ONLY functions a Builder or the connectivity
# backend may call to mutate network state. No Builder touches
# network.add_to_graph or network.graph directly.

def set_attr(obj: object, attr: str, value: Qty | str | int | float | None) -> None: ...
def link(obj: object, assoc: str, target: object) -> None: ...
def add_to_graph(network, obj: object) -> None:
    """network.add_to_graph(obj) + name_index.add(obj) (§5.5), one call site."""
def resolve(network, cim_cls: type, name: str) -> object | None:
    """NameIndex.get(cim_cls, name) — §5.5. Returns None if not (yet) declared;
    caller (connectivity backend) decides whether that means auto-vivify or
    error. Never raises on a missing name — only add_to_graph raises, and only
    on a genuine duplicate (§5.5)."""
```

Phase 4 (connectivity backend) and every Phase 5 Builder are written **only**
against these four functions plus `NameIndex.get` — never against
`cimgraph.GraphModel` internals directly. This is what makes §5.5's "if #81
ever ships, `NameIndex` becomes a thin wrapper" exit ramp real: only
`graph_write.py` would need to change.

### 12.4 Phase 4 → Phase 5 : the connectivity backend surface

```python
# core/connectivity.py

def add_connectivity(network, obj: object, *, node_cols: dict[str, str]) -> list["Terminal"]:
    """node_cols is the already-disambiguated {'node1': 'busA', 'bus2': 'busB', ...}
    slice of a <Class>Row (§12.2) — the Builder picks which of its row's fields
    are connectivity columns per §3.5's fixed vocabulary and passes only those.
    Auto-vivifies any name not found via resolve() (§12.3). Returns Terminals in
    column order (sequenceNumber = list index + 1) so the Builder can attach
    per-phase children (§12.5) to the right terminal."""

def add_phase_children(network, obj: object, terminals: list["Terminal"],
                        *, phases: str, phase_cls: type) -> list[object]:
    """phases='ABCN' -> phase_cls (e.g. ACLineSegmentPhase) instances per §3.6,
    wired to obj and given correct SinglePhaseKind + sequenceNumber."""
```

A Builder's `add_connectivity` method (§4.1) is a thin wrapper: pull the
connectivity/phase columns off its `<Class>Row`, call these two functions, keep
the returned terminals if a later `add_electrical` needs them (e.g. per-terminal
ratings). No Builder re-implements node-vs-bus disambiguation or phase synthesis
— that logic exists exactly once, here.

### 12.5 Phase 5 → Phase 6/7 : the Builder surface (recap, now literal)

Already fully specified in §4.1 as the `ObjectBuilder` ABC — restated here only
to close the chain: `from_table(row: <Class>Row) -> Self` (§12.2's dataclass),
`build() -> object` returns the live cim-graph instance (already past
`graph_write.add_to_graph`, §12.3). Phase 6 (catalogs/templates) and Phase 7
(public surface) consume `build()`'s return value and nothing lower-level — a
package/CLI author never needs `graph_write.py` or `connectivity.py` directly.

### 12.6 Phase 6/7 → Phase R : nothing new, the writer reads the graph directly

The writer (Phase R) does **not** consume any of §12.1–12.5 — it reads
`network.graph`/`network.name_index` (§5.5) directly and produces `.cimtbl`
text, the inverse direction. Called out explicitly so it's clear Phase R has no
dependency on the Row dataclasses; a schema change that only touches parsing
(e.g. a new column) does not require writer changes unless the writer also
needs to *emit* that column.
```
