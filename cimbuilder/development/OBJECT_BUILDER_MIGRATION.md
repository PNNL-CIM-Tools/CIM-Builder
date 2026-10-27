# Phased Plan: Porting `object_builder/` onto the Real `ObjectBuilder` API

**Status:** plan of record. Written after reconciling every doc in this
directory against the shipped reference implementation
(`cimbuilder/builders/load/consumer.py`), and after surveying the real
downstream consumer (CIMHub_2_0's importer scripts) to prioritize equipment
categories by actual duplicated construction logic rather than by
`substation_builder/`'s narrower internal dependency.

---

## 1. Why this plan, and why this order

### 1a. The target shape (already shipped, not a sketch)

`cimbuilder/builders/base.py`'s `ObjectBuilder` is concrete and stateless:

```python
class ObjectBuilder:
    def __init__(self, network, container=None):
        self.network = network
        self.container = container
        self.cim = network.cim

    def create(self, *, name): ...      # bare cim_cls(name=name)
    def from_table(self, row): ...      # generic .cimtbl row -> object, via cimtables.binder.bind_row
    def add(self, obj): ...             # graph_write.add_to_graph, returns obj
```

A subclass (`EnergyConsumerBuilder` is the reference) defines one
`add_<profile>(self, obj, *, ...)` method per CIM profile part the equipment
type actually has fields for. Each method:

- takes the object as an explicit first parameter and returns `None` — no
  chaining, no `self.obj` instance state;
- imports its own real part module at the top of the file
  (`cimprofiles.cim18.cim18v17.<part>`) and passes it as `graph_write.set_attr`/
  `set_assc`'s `part` argument;
- resolves any by-name FK it owns via `graph_write.resolve`/
  `resolve_any_subclass`, and writes the association itself — there is no
  separate `add_references`/`add_assc` method (see `GRAPH_WRITE_CONTRACT.md`
  §3 and `ARCHITECTURE.md`): an association belongs to whichever profile part
  declares it.

See `ARCHITECTURE.md`, `BUILDER_API.md`, `GRAPH_WRITE_CONTRACT.md` §7 for the
full contract this plan ports every category onto.

### 1b. What's actually being replaced

`cimbuilder/object_builder/` is old-style `new_<equipment>(network, container,
name, ...)` factory functions. All of them:

- hard-import a flat profile module at module scope
  (`cimgraph.data_profile.cimhub_2023 as cim`, immediately shadowed by `cim =
  network.cim` inside the function body — a leftover typing-only import);
- hand-roll terminal/node wiring inline instead of calling a shared
  connectivity function (inconsistently — see the bug list in §1c);
- `setattr` physical quantities directly with no `CIMUnit` wrapping and no
  profile-part check at all.

`cimbuilder/object_builder/__init__.py` only re-exports `new_breaker`,
`new_disconnector`, `new_bus_bar_section`, `new_power_transformer`,
`new_one_terminal_object`, `new_two_terminal_object`, `new_analog`,
`new_discrete` — the rest (load, generator, inverter/EVSE, the commented-out
capacitor/tap-changer lines) exist as files but are dead code today. One file,
`line/line_builder.py`, is not working source at all (undefined names, a
`setattr(..., fields(...), )` call missing an argument, `get_cim_profile()`
called with no args but type-annotated as a module) — it was the original
"eureka probe" and should be treated as a design note, not ported line-for-line.

### 1c. Known inconsistencies this port fixes by construction

Confirmed in `BASELINE.md` §4, still true today:

1. **Double-UUID bug** — `switch/new_disconnector.py` seeds `t1`'s UUID twice
   and never seeds `t2`'s.
2. **Hand-rolled terminal idiom, inconsistent across files** —
   `topology/new_bus_bar_section.py` builds its terminal inline;
   `load/new_energy_consumer.py` calls `t1.uuid(name=...)` after construction;
   `generic/new_two_terminal_obj.py` uses `cim.Terminal(name=..., sequenceNumber=...)`
   directly. Going through `cimtables.connectivity.add_connectivity` for every
   builder (as `EnergyConsumerBuilder.add_connectivity` already does) removes
   this drift — one function builds every terminal, the same way, every time.
3. **No CIMUnit wrapping** — every `new_*` function sets physical quantities
   as bare floats (`load.p = p`). `graph_write.set_attr` is what actually
   constructs the `CIMUnit` from a plain value or `Qty`, so every port must
   switch to it rather than preserving the bare `setattr`.
4. **`utils.get_base_voltage`'s raw comparison** — compares `bv.nominalVoltage
   == base_voltage` against a plain number; once a builder reads it back as a
   `Voltage` CIMUnit this needs `.to('V')` (`UNITS.md`). Fix when a builder
   first calls this helper (Transformer and Load phases, below).

### 1d. Priority: CIMHub_2_0's real importer scripts, not `substation_builder/`

An earlier draft of this plan used `substation_builder/`'s internal call graph
(`new_breaker`/`new_disconnector`/`new_bus_bar_section`/`new_power_transformer`
are the only `object_builder` symbols it calls) to decide port order. That is
the wrong north star: `substation_builder/` is CIM-Builder's own internal
consumer, not the real one. The real consumer is CIMHub_2_0's per-format
importer scripts (`cimhub_<opendss|cyme|gridlabd|raw>/importer/`), which today
hand-roll equipment construction independently, per format, per equipment
type, with no shared builder — `cimhub_core.connectivity`/`.transformations`
already consolidated the *plumbing* (terminal/node wiring, BaseVoltage BFS
propagation, load-response/LRC creation, transformer impedance math) but not
the *equipment construction* itself, which is exactly where the duplication
this plan should remove still lives.

A survey of CIMHub_2_0 (file sizes via `wc -l`, representative code read in
full) ranks equipment categories by real, duplicated construction volume:

| Rank | Category | Evidence |
|---|---|---|
| 1 | **Transformer/PowerTransformer** | Largest files in every format (opendss `transformer.py` 1012 + `autotrans.py` 317 + `xfmrcode.py` 282; cyme 319+163+186+209; raw 474; gridlabd 164+128) and the highest-complexity math (star/mesh impedance, autotransformers, regulators, vector groups) — `cimhub_core.transformations.transformers`/`per_unit` already extracted the math but never assembled into a builder |
| 2 | **Load/EnergyConsumer** | Present in every format (opendss 357, cyme 144+55, gridlabd 63, raw 283); 3+ independently-written phase-splitting + ZIP-model implementations; **partially done already** — `EnergyConsumerBuilder` is the reference implementation |
| 3 | **Line/ACLineSegment** | Largest single opendss file (531 lines, 5 branching impedance-input paths: linecode/sequence/matrix/geometry/spacing); 4 separate cyme converter functions; independent gridlabd/raw equivalents |
| 4 | **Switch/breaker/disconnector/fuse** | Smaller files, duplicated 4+ times (opendss, cyme ×5 variants, raw, gridlabd) with near-identical rated-current/terminal/phase logic — high quick-win ratio |
| 5 | **Capacitor/shunt compensator** | Duplicated 4 times (opendss 358+205 w/ capcontrol, cyme 74, raw 217+187 fixed/switched, gridlabd 93); same susceptance-per-section math reimplemented per format |
| 6 | **Generator/SynchronousMachine + inverter/PEC/EVSE** | Real but smaller/scattered (opendss generator 140 + pvsystem 254 + storage 304; cyme 70+219+94; raw 301+125) — three sub-kinds with less structural overlap between formats |
| — | **Measurement (Analog/Discrete)** | **Zero construction logic found anywhere in CIMHub_2_0** (`grep cim\.Analog\|cim\.Discrete\|cim\.Measurement` → no hits). Not a real signal from this consumer today — deprioritized indefinitely, not phased below |

`cimbuilder`/`cimtables` have zero live import anywhere in CIMHub_2_0 today
(confirmed by repo-wide grep — the one `cimbuilder` hit, in
`test_data/build_container.py`, is entirely commented out) — a clean slate,
no reverse-compatibility constraint on any of this.

Raw input shapes CIMHub_2_0's importers actually have available when they
construct each equipment type (this is what each phase's method signatures
must accept):

- **Loads**: kW/kvar/kVA/pf in any combination (needs derivation), wye/delta
  connection, per-phase breakdowns, a DSS ZIPV 7-tuple, a bus+phase-suffix
  string (not a structured phase list) pre-terminal-wiring.
- **Lines**: (a) a linecode/geometry/spacing name reference to resolve later,
  (b) raw r1/x1/r0/x0/C1/C0 sequence values, (c) rmatrix/xmatrix/cmatrix phase
  matrices, or (d) PSS/E PI-model per-unit on an MVA base — four structurally
  different impedance input shapes, varying by which source fields are
  populated.
- **Transformers**: ratedU/ratedS per winding, %Xsc/%R (DSS) or raw CZ-coded
  per-unit (PSS/E), vector group, tap changer data — per-unit↔ohm conversion
  (already shipped, see §1e) plus star↔mesh (already in
  `cimhub_core.transformations.transformers`).
- **Switches**: rated/breaking current, open/closed state flag, phase list —
  the simplest, most uniform shape of any category.
- **Capacitors**: kvar+kV (scalar) or cmatrix/cuf (per-phase µF arrays), step
  count, connection.
- **Generators/DER**: kVA/kW rating, pf or kvar, connection, and for
  PV/storage, inverter efficiency/kVA limits — the least uniform shape across
  formats.

### 1e. The per-unit engine already exists

Earlier drafts of this repo's docs deferred `pu`/`%` impedance conversion to a
"Phase 11" that was never built as a `cimbuilder`-local module. It has since
shipped in `cimtables.binder.bind_row` / `graph_write.set_attr`'s `z_base`
parameter — see `UNITS.md` and `PERCENT_IMPEDANCE_BASE.md`. Every phase below
that touches relative impedance (Transformer, Line) uses that existing engine;
none of them need to build a new one.

---

## 2. Phases

Each phase ports one equipment category: read the old `new_*` function(s) for
the construction logic (terminal wiring, field names, FK resolution), then
write a stateless `ObjectBuilder` subclass that does the same construction
through `cimtables.connectivity`/`graph_write`. Each phase ends with a test
file mirroring `tests/builders/test_consumer.py`'s pattern (see
`BUILDER_TEST_CREATION.md`) and a verification that `uv run pytest` stays
green.

### Phase 1 — `PowerTransformerBuilder` (+ tap changer)

**Ports:** `object_builder/transformer/new_power_transformer.py`,
`object_builder/transformer/new_tap_changer.py`.
**New file:** `cimbuilder/builders/transformer/power_transformer.py`.

- `create(self, *, name)` — base.py's default is enough; no override needed.
- `add_connectivity(self, xfmr, *, node1, node2, container=None)` — builds a
  `PowerTransformerEnd` + `Terminal` pair per winding (today's function hard-codes
  2 windings; keep that scope for Phase 1, generalize to N windings only if a
  real 3-winding CIMHub input shows up), wires via
  `cimtables.connectivity.add_connectivity`.
- `add_electrical(self, xfmr, *, end1_ratedU=None, end1_ratedS=None, r=None, x=None, ...)` —
  sets `PowerTransformerEnd.ratedU`/`.ratedS` (needed as the `z_base` for a
  relative impedance — see `_winding_z_base` in `cimtables/binder.py`) and the
  impedance itself via `graph_write.set_attr(end, EL, 'r', qty, z_base=...)`
  when `r`/`x` arrive as a relative `Qty` (`%`/`pu`). This is the first real
  caller of the relative-impedance path outside `.cimtbl`-driven `bind_row` —
  confirm `z_base` resolution (ratedU/ratedS on the object's own
  `PowerTransformerEnd`) matches `cimprofiles.cim18.cim18v17.electrical_unbalanced.PowerTransformerEnd`'s
  real fields (confirmed present at the time of writing).
- `add_tap_changer(self, xfmr, *, end, highStep=0, lowStep=0, initialDelay=0, ...)` —
  ports `new_tap_changer`'s `RatioTapChanger` construction; folds the tap
  changer into the transformer builder rather than keeping it a separate
  top-level builder (matches `BASELINE.md`'s original call — "folded into
  xfmr").
- Fixes `new_power_transformer`'s `catalog_file`-only path (today's function
  returns an undefined `xfmr` if `catalog_file is None` — a real bug, not
  preserved) by making `add_electrical`'s direct-value path the primary one;
  `utils.catalog_parser`-based construction can be a later, separate
  `from_catalog`-style addition, not required for this phase.

### Phase 2 — Generalize `EnergyConsumerBuilder`'s already-shipped pattern

`EnergyConsumerBuilder` (`builders/load/consumer.py`) is done — reference
implementation, not a to-do. This phase is about using it as the literal
template for every category below (same method-naming convention: `add_ssh`
for steady-state values, `add_electrical` for electrical-part fields,
`add_connectivity` owning its own by-name FK resolution) and, if CIMHub_2_0's
real `EnergyConsumerPhase`-per-phase construction (opendss/cyme/gridlabd's
three independent phase-splitting implementations) is wanted here too, adding
an `add_electrical`-sibling for per-phase values. Not required to close this
phase; flag as a follow-up once a real per-phase `.cimtbl`/CIMHub caller needs
it.

### Phase 3 — `ACLineSegmentBuilder`

**Ports:** `object_builder/line/line_builder.py` (design intent only — the
file itself is not working source, see §1b), `object_builder/generic/
new_two_terminal_obj.py` (the terminal-wiring pattern it should use instead of
reinventing one).
**New file:** `cimbuilder/builders/line/segment.py`.

- `create`/`add_connectivity` — same two-terminal pattern as
  `new_two_terminal_object`, but through `connectivity.add_connectivity`
  rather than the old inline `utils.terminal_to_node` calls.
- `add_electrical(self, line, *, r=None, x=None, bch=None, gch=None, ...)` —
  balanced scalar impedance via `graph_write.set_attr`, part module
  `cimprofiles.cim18.cim18v17.electrical_unbalanced` (`ACLineSegment` is
  defined there).
- `add_short_circuit(self, line, *, r0=None, x0=None, b0ch=None, g0ch=None)` —
  zero-sequence, part module `cimprofiles.cim18.cim18v17.short_circuit`
  (`ACLineSegment` is defined there too, confirmed at the time of writing).
- **Impedance input shape.** CIMHub's four real input shapes (linecode-by-name,
  sequence r1/x1/r0/x0, rmatrix/xmatrix, or PI-model per-unit) mean this
  builder likely needs more than one `add_electrical`-style method, or one
  method accepting a tagged-union-style set of keyword groups — resolve this
  design question against a real CIMHub line importer (e.g.
  `cimhub_opendss/importer/lines/line.py`) before committing to a signature,
  rather than guessing. This is the one category in this plan that most needs
  a design pass before the port, not just a mechanical translation.
- Per-phase (`ACLineSegmentPhase`/`PerLengthPhaseImpedance`) matrix impedance
  is a later addition once the scalar/sequence path is solid — do not block
  Phase 3 on it.

### Phase 4 — Switch family: `BreakerBuilder`, `DisconnectorBuilder`, (`FuseBuilder`, `RecloserBuilder` as straightforward siblings)

**Ports:** `object_builder/shunt/new_breaker.py`,
`object_builder/switch/new_disconnector.py`.
**New files:** `cimbuilder/builders/switch/breaker.py`,
`cimbuilder/builders/switch/disconnector.py`.

- Fixes the double-UUID bug (§1c.1) by construction — going through
  `connectivity.add_connectivity` for both terminals removes the hand-rolled
  per-terminal seeding entirely.
- `add_connectivity(self, sw, *, node1, node2, open=None, container=None)` —
  `Disconnector`/`Fuse`/`Recloser`/`Breaker`'s open/closed state field lives on
  the `connectivity_unbalanced`/`steady_state_hypothesis` part (confirmed: no
  `electrical_unbalanced` definition of these classes exists), so this
  category needs **no `add_electrical` at all** — simplest category in this
  plan, good first port to validate the pattern before Transformer/Line.
- `Fuse`/`Recloser`/`LoadBreakSwitch` are mechanical siblings of
  `DisconnectorBuilder` once one is done — same shape, different class name;
  worth doing as one short follow-up rather than a separate phase.

### Phase 5 — `LinearShuntCompensatorBuilder` (capacitor)

**Ports:** `object_builder/shunt/new_capacitor.py`.
**New file:** `cimbuilder/builders/shunt/capacitor.py`.

- `add_connectivity` — standard one/multi-terminal wiring depending on
  grounded-wye vs delta (check `new_capacitor.py`'s existing terminal count
  logic before assuming single-terminal).
- `add_electrical(self, cap, *, bPerSection=None, gPerSection=None, ...)` —
  part module `electrical_unbalanced` (`LinearShuntCompensator`).
  CIMHub's four independent susceptance-per-section implementations
  (opendss/cyme/raw fixed+switched/gridlabd) are the real signal this port
  should consolidate — check whether a `kvar`/`kV`-to-`bPerSection` conversion
  helper belongs on the builder or stays a CIMHub-side transformation (lean
  toward the latter unless CIM-Builder already owns an equivalent for another
  category).

### Phase 6 — Generator/inverter family: `SynchronousMachineBuilder`, `PowerElectronicsConnectionBuilder` (+ EVSE siblings)

**Ports:** `object_builder/generator/new_synchronous_generator.py`,
`object_builder/inverter/new_power_electronics_connection.py`,
`object_builder/inverter/new_EVSE*.py` (5 files).
**New files:** `cimbuilder/builders/generator/synchronous_machine.py`,
`cimbuilder/builders/inverter/power_electronics_connection.py`.

- Apply the generator sign convention fix while porting (`UNITS.md`): a
  generator's terminal `p` is negative under the CIM convention; negate a
  "generation MW" input rather than passing it straight through, exactly as
  `new_synchronous_generator.py` should already be doing — confirm/fix in the
  port, don't just translate.
- EVSE family (`new_EVSE`, `new_EVSE_BU`, `new_EVSE_BV`, `new_EVSE_PEC`,
  `new_EVSE_PEU`) is lower-priority than the base PEC/synchronous-machine
  cases per the CIMHub survey (less structural overlap between formats than
  load/line/transformer) — port the shared `PowerElectronicsConnection` shape
  first; treat the EVSE-specific subclasses as a follow-up once a real EVSE
  `.cimtbl`/CIMHub caller exists.

### Not phased: Measurement, `base/new_base_voltage.py`, `deprecated/create_houses.py`

- **Measurement** (`new_analog`, `new_discrete`) — zero real construction
  callers found in CIMHub_2_0 today (§1d). Leave as dead-but-harmless
  `object_builder/measurement/` files until a real caller appears; do not
  spend a phase on this speculatively.
- **`base/new_base_voltage.py`** — not an `ObjectBuilder` candidate; it's a
  lookup/create helper (`utils.get_base_voltage` is its real caller) and
  stays as a plain function, reused by whichever phase's builder needs a
  `BaseVoltage`.
- **`deprecated/create_houses.py`** (779 lines) — already marked deprecated;
  delete whenever a phase's cleanup touches `object_builder/load/`, but don't
  make deleting it a phase goal on its own.

---

## 3. Verification (every phase)

1. New builder's tests pass in isolation (`uv run pytest
   tests/builders/<category>/ -v`), following `BUILDER_TEST_CREATION.md`'s
   `network` fixture pattern (`XMLFile` + `NameIndex`, not a bare
   `GraphModel()`).
2. Full `uv run pytest` stays green — no regression in
   `tests/builders/test_consumer.py` or any other already-passing file.
3. `grep -rn "object_builder\." cimbuilder/ tests/` after a phase's old
   `new_*` function is no longer called anywhere outside its own file —
   decide per-phase whether to delete the old file immediately or leave it
   until every phase lands (leaving it is safe; nothing re-exports it once
   `__init__.py`'s import line for that symbol is removed).
4. Spot-check against a real CIMHub_2_0 input shape for that category (read
   the relevant importer file again after the port, confirm the new
   builder's signature could plausibly replace that file's hand-rolled
   construction — this plan does not require actually wiring CIMHub_2_0 to
   call `cimbuilder`, just confirming the shape fits).

---

## Related documents

- `ARCHITECTURE.md`, `BUILDER_API.md` — the API contract every phase ports
  onto.
- `GRAPH_WRITE_CONTRACT.md` — the `set_attr`/`set_assc` contract, including
  the relative-impedance/`z_base` mechanism Phase 1 and Phase 3 use.
- `UNITS.md` — CIMUnit and per-unit conversion rules.
- `BUILDER_TEST_CREATION.md` — the test pattern every phase's test file
  follows.
- `BASELINE.md` — the original bug/inconsistency inventory this plan fixes
  by construction.
