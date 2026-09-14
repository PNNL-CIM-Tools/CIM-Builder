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
| `from`, `to` | alias pair, context-dependent |

Terminal count = number of connectivity columns present. `sequenceNumber`
follows column order. This vocabulary is documented in the LinkML schema and
enforced by the connectivity backend; it is the single naming convention the
system relies on.

### 3.6 `phases` → per-phase child synthesis

A `phases` column (`ABCN`, `BC`, `D`, `Y`) drives creation of the per-phase
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
    def from_table(self, row: dict, header: Header) -> Self:  # DSL / bulk start
        """Skinny adapter: unpack a validated .cimtbl row + header (with units)
        into the create()/add_*() calls below. This is where a Table row lands."""

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
(LinkML `gen-python`, str→float/int/enum coerced and validated *at parse time*)
and hands each to `ACLineSegmentBuilder().from_table(row).build()`. All CIM
knowledge lives in the Builder. This is the "cascading parse" the user described,
and it mirrors `cimhub_opendss`'s `convert_line(dss_line: dss.Line)` exactly:

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
- **Group by class → `Table`.** Objects of the same class with the same populated
  attribute set become one `Table` block; singletons or ragged sets become
  `Object` lines. (Mirrors the reader's two forms.)
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
toys). Lettered sub-phases can run same-day.

| Phase | Name | Depends on | Exit criterion (measured) |
|---|---|---|---|
| **0** | Design lock + repo scaffold | — | This doc reviewed; new package tree (§8.1) created; `uv sync` clean; empty modules import. |
| **1** | Lark grammar → records | 0 | `ieee13.cimtbl` **and** `ieee14.cimtbl` parse to the intermediate record list; every `Object`/`Table`/`Import`/comment/blank-cell/`(unit)` case covered by a grammar test; ambiguity check passes. No CIM yet. |
| **2** | LinkML validation gate + dataclass | 1 | LinkML schema for the `ieee13` class set; every record validates or fails with a profile-anchored message; a deliberately-broken column name fails fast naming the closest valid attribute. Records → validated dataclasses. |
| **3** | Graph-write core + reflective binder | 2 | Simplest real classes end-to-end into a live `cimgraph` model: `BaseVoltage`, `BaseFrequency`, `BasePower`, `EnergySource`. `network.cim` read once; plain scalar attrs + units land correctly (verified via `.to()`). |
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
    binder.py                 # Phase 3: reflective column → attr/assoc/synthesis
    connectivity.py           # Phase 4: THE backend (node/bus/terminal/phase)
    units.py                  # Phase 5b: %Z / pu / ohm normalization helpers
  builders/                   # Phase 5: one module per CIM class family
    base.py                   #   ObjectBuilder ABC + builder_base mixin
    line.py                   #   ACLineSegmentBuilder (+ PerLengthImpedance)
    consumer.py               #   EnergyConsumerBuilder
    shunt.py                  #   LinearShuntCompensatorBuilder
    transformer.py            #   PowerTransformer / PowerTransformerEnd
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

1. **LinkML generation** — do we `gen-python` the validation dataclasses from the
   schema (CIMHub pattern), or hand-write dataclasses and use LinkML only as the
   validation ruleset? (Gates Phase 2.) *Leaning: LinkML-as-validator only; the
   real typed objects are `network.cim` classes, so generated dataclasses would
   duplicate the profile.*
2. **Writer table-grouping heuristic** — how ragged an attribute set still shares
   a `Table` vs. splits to `Object` lines? (Gates Phase R determinism.)
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
- `~/PNNL-dss/` — the VS Code extension template for §6.5 / Phase V. Key files:
  `package.json` (manifest: `languages`/`grammars`/`themes` contributions),
  `src/opendss-validator.ts` (diagnostics from a JSON dictionary),
  `src/extension.ts` (activation + document listeners),
  `syntaxes/opendss.tmLanguage.json` (TextMate grammar),
  `script/config_generator.py` (schema → dictionary — the analog of our
  `export-editor-schema` CLI).
```
