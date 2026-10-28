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

### Phase 1 — `PowerTransformerBuilder` + `TransformerTankConfigurationBuilder`

**Status: superseded here, see the implementation plan.** The signature
sketched below (one `add_electrical` writing `r`/`x` onto a merged
`PowerTransformerEnd` with a single `z_base`) undercounts the real design —
confirmed against real `.cimtbl` reference models
(`/home/ande188/CIMTBL-Models/distribution/padmount_example.cimtbl`,
`.../IEEE/IEEE13_CDPSM/xfmrcodes.cimtbl`) and real Visio modeling reference
diagrams the user supplied: there are **three coexisting CIM impedance
representations** (PI-direct-on-end for PSS/E, mesh-by-end, and
mesh-by-winding/template for OpenDSS), all living in
`cimprofiles.cim18.cim18v17.electrical_balanced` — not
`electrical_unbalanced`, which has no scalar impedance fields on
`PowerTransformerEnd` at all. The full, corrected, implementation-ready
design (exact method set across two builder classes, confirmed part-module
field locations, and the explicit decision to keep star↔mesh conversion out
of `cimbuilder` entirely) lives in the approved implementation plan at
`/home/ande188/.claude/plans/dreamy-purring-noodle.md` — read that, not the
sketch below, before writing code.

<details>
<summary>Original (superseded) sketch — kept for history</summary>

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
  when `r`/`x` arrive as a relative `Qty` (`%`/`pu`).
- `add_tap_changer(self, xfmr, *, end, highStep=0, lowStep=0, initialDelay=0, ...)` —
  ports `new_tap_changer`'s `RatioTapChanger` construction; folds the tap
  changer into the transformer builder rather than keeping it a separate
  top-level builder (matches `BASELINE.md`'s original call — "folded into
  xfmr"). Still correct in the revised design.
- Fixes `new_power_transformer`'s `catalog_file`-only path (today's function
  returns an undefined `xfmr` if `catalog_file is None` — a real bug, not
  preserved) by making the direct-value path primary; `utils.catalog_parser`-
  based construction can be a later, separate `from_catalog`-style addition.

</details>

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

**Status: done.** Implemented as `cimbuilder/builders/line/base.py`
(`ACLineSegmentBuilder`) + `cimbuilder/builders/line/by_template.py`
(`PerLengthSequenceImpedanceBuilder`, `PerLengthPhaseImpedanceBuilder`),
mirroring Phase 1's instance-tier/template-tier split. Tested end-to-end
against the real `linecodes.cimtbl`/`lines.cimtbl` reference pair
(`tests/builders/test_ac_line_segment.py`, 8 tests, all passing; 30/30 full
suite). Confirmed against real Visio modeling reference diagrams
(`LineModel01-05`) that there are **four** coexisting shapes, not the three
originally scoped here — direct balanced PI, direct zero-sequence PI, and
per-length reference split into *two* template classes
(`PerLengthSequenceImpedance` balanced vs. `PerLengthPhaseImpedance`
matrix), not one. Two real field-location corrections surfaced during
implementation, both confirmed by reading the installed `cimprofiles`
package directly rather than trusting this section's own sketch below:

- **The per-length FK (`ACLineSegment.PerLengthImpedance`) is an
  `electrical_unbalanced` field, not `electrical_balanced`** — the opposite
  of what the sketch below says. `electrical_balanced.ACLineSegment` has
  only the scalar `r`/`x`/`bch`/`gch` fields, no FK at all.
- **`PerLengthImpedance`'s own base-class fields (`calculatedFrequency`,
  `rg`, `xg`) must be written through whichever part module actually
  defines a same-named class for the object's runtime type** —
  `graph_write._part_field` matches by exact class name, not inheritance,
  and `electrical_balanced` has no `PerLengthPhaseImpedance` class at all
  (only `PerLengthSequenceImpedance`). So `PerLengthSequenceImpedanceBuilder`
  uses `electrical_balanced` throughout, while `PerLengthPhaseImpedanceBuilder`
  uses `electrical_unbalanced` throughout for the same three inherited
  fields — two different part modules for fields that look identical on
  the class diagram.
- `PhaseImpedanceData`'s FK back to its matrix is the singular field
  `PhaseImpedanceData.PhaseImpedance` (easy to miss — it's defined after the
  four scalar fields, past where a quick read stops). `set_assc` must be
  called from that singular side, once per row; calling it from the
  `PerLengthPhaseImpedance.PhaseImpedanceData` list side with a list target
  would silently append the whole list as one broken list element.

**Extension — wire geometry reference (shape 5).** Added after the above:
`ACLineSegmentBuilder.add_wire_configuration` references a `WireConfiguration`
template by name (part module `construction`, a singular FK — a third,
distinct part module from shapes 1-4's `electrical_balanced`/`short_circuit`/
`electrical_unbalanced`). The template itself (`WireConfigurationBuilder`,
`by_template.py`) points at one `WireSpacing` — either a
`ConductorDistanceSpacingBuilder`-built `ConductorDistanceSpacing`
(LineModel04, GridLAB-D `line_spacing` equivalent — one `ConductorDistance`
row per described pair) or an `XYSpacingBuilder`-built `XYSpacing`
(LineModel05, OpenDSS `LineSpacing`/`LineGeometry` equivalent — one
`XYConductorPosition` row per conductor). Tested in
`tests/builders/test_wire_spacing.py` (7 tests, 37/37 full suite). Two
field-location surprises confirmed by reading `construction.py` directly:

- `ConductorDistance` carries **two** pairs of sequence-number fields:
  `sequenceNumber1`/`sequenceNumber2` (the real CIM101 fields, documented,
  matching the diagram) and `fromSequenceNumber`/`toSequenceNumber` (an
  undocumented gridappsd-extension duplicate with empty docstrings). The
  builder uses the former; the latter looks like a plausible alternate name
  and is a trap for a future reader skimming the class body top-to-bottom.
- `WireSpacing`/`ConductorDistanceSpacing`/`XYSpacing` carry no impedance or
  geometry data themselves — only list FKs back to their children
  (`ACLineSegment`, `WireConfiguration`, `ConductorDistance`/
  `XYConductorPosition`). Every one of those is set from the *child's*
  singular FK side (`ConductorDistance.ConductorDistanceSpacing`,
  `XYConductorPosition.XYSpacing`), same "singular side owns the call,
  inverse auto-populates the list" pattern Phase 1/3's earlier corrections
  already established — never set_assc'd from the list side directly.

The rest of this section (kept for history) was the resolved design going
into implementation — accurate except for the `EL_BAL`/`EL_UNBAL` mix-up
noted above.

**Ports:** `object_builder/line/line_builder.py` (design intent only — the
file itself is not working source, see §1b), `object_builder/generic/
new_two_terminal_obj.py` (the terminal-wiring pattern it should use instead of
reinventing one).
**New file:** `cimbuilder/builders/line/segment.py`.

**Impedance design — resolved.** A research pass read every real CIMHub_2_0
line importer in full
(`cimhub_opendss/importer/lines/line.py::_set_line_impedance`, all 4 cyme
converter functions, `cimhub_raw/importer/lines/branch.py`) and cross-checked
against what the shipped profile actually has. Two findings drove the final
shape:

1. **The four input shapes collapse to only two terminal CIM writes, never
   four.** opendss's `_set_line_impedance` is a 5-way if/return cascade where
   4 of 5 branches (linecode, rmatrix/xmatrix, geometry, spacing) end in
   "resolve/build a `PerLengthImpedance`-family object and set
   `line.PerLengthImpedance` by reference" — only the sequence-value branch
   (`r1/x1/r0/x0/C1/C0`) sets scalars directly. All 4 cyme converter functions
   go by-reference, never scalar. `raw/branch.py`'s PSS/E per-unit path
   converts `pu`→ohms once (`z_base = kV²/MVA`) and then itself dispatches
   into the *same* two terminal shapes depending on whether `length_km` is
   known — PI-model per-unit is a CIMHub-side unit-conversion front end, not
   a fifth CIM representation.
2. **`electrical_unbalanced.ACLineSegment` (the part module every other
   builder in this plan targets) has no scalar r/x/bch fields at all** —
   confirmed by reading `cimprofiles/cim18/cim18v17/electrical_unbalanced/
   electrical_unbalanced.py`: only `PerLengthImpedance`/`WireConfiguration`
   associations. The balanced scalar fields (`r`, `x`, `bch`, `gch`) live in
   `electrical_balanced.ACLineSegment` instead — a genuinely different part
   module than this builder's other methods use. `PerLengthSequenceImpedance`
   (r0/x0/b0ch/g0ch) lives in `short_circuit` and `electrical_balanced`, not
   `electrical_unbalanced`.

Three methods, one per CIM target shape — not one tagged-union method —
matching the real importers' own structure (each picks a shape with an
early-return/separate-function, never branches two shapes inside one call)
and the `EnergyConsumerBuilder` precedent of one method per profile part:

```python
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.short_circuit as SC

def add_electrical(self, line, *, r=None, x=None, bch=None, gch=None) -> None:
    """Balanced scalar impedance. electrical_balanced.ACLineSegment.r/x/bch/gch
    (NOT electrical_unbalanced — it has no scalar fields on ACLineSegment).
    Mirrors opendss line.py's r1/x1/C1 branch and raw branch.py's
    length_km<=0 branch."""
    graph_write.set_attr(line, EL_BAL, 'r', r)
    graph_write.set_attr(line, EL_BAL, 'x', x)
    graph_write.set_attr(line, EL_BAL, 'bch', bch)
    graph_write.set_attr(line, EL_BAL, 'gch', gch)

def add_short_circuit(self, line, *, r0=None, x0=None, b0ch=None, g0ch=None) -> None:
    """Zero-sequence. short_circuit.ACLineSegment.r0/x0/b0ch/g0ch.
    Mirrors opendss line.py's r0/x0/C0 half of the same branch."""
    graph_write.set_attr(line, SC, 'r0', r0)
    graph_write.set_attr(line, SC, 'x0', x0)
    graph_write.set_attr(line, SC, 'b0ch', b0ch)
    graph_write.set_attr(line, SC, 'g0ch', g0ch)

def add_per_length_impedance(self, line, *, PerLengthImpedance) -> None:
    """By-reference impedance — the majority real-world path (4/5 opendss
    branches, all 4 cyme converters, raw's length_km>0 branch). Resolves an
    already-built PerLengthImpedance/PerLengthSequenceImpedance/
    PerLengthPhaseImpedance by name and sets both sides of the association,
    mirroring opendss's _link_per_length_impedance."""
    target = graph_write.resolve_any_subclass(self.network, self.cim.PerLengthImpedance, PerLengthImpedance)
    if target is None:
        raise ValueError(f"{line.name!r}: PerLengthImpedance {PerLengthImpedance!r} not found in graph")
    graph_write.set_assc(line, EL_BAL, 'PerLengthImpedance', target)
```

- `create`/`add_connectivity` — same two-terminal pattern as
  `new_two_terminal_object`, but through `connectivity.add_connectivity`
  rather than the old inline `utils.terminal_to_node` calls.
- A caller (or `from_table`'s field-presence dispatch, per `CIMTBL_DESIGN.md`
  §12.2) picks whichever of the three impedance methods matches the input it
  has — there is no silent precedence rule to resolve if more than one is
  called, since each just writes its own fields/association independently;
  the choice of *which one to call* is the caller's, exactly as it is in every
  real importer today.
- Geometry/spacing (opendss cases 4/5) produces no impedance call on
  `ACLineSegmentBuilder` at all — it's `ACLineSegmentPhase` + `WireSpacingInfo`/
  `WireInfo` construction, which belongs to connectivity/phase synthesis or a
  separate `PerLengthPhaseImpedanceBuilder`, not this builder. Per-phase
  matrix impedance (`PerLengthPhaseImpedance`/`PhaseImpedanceData`, already
  locked in `CIMTBL_DESIGN.md` §3.8 as literal element-per-row) is likewise a
  separate builder `ACLineSegmentBuilder.add_per_length_impedance` only ever
  *references* by name — do not block Phase 3 on building it.

### Phase 4 — Switch family: `BreakerBuilder`, `DisconnectorBuilder`, (`FuseBuilder`, `RecloserBuilder` as straightforward siblings)

**Status: done.** `cimbuilder/builders/switch/switch.py`,
`tests/builders/test_switch.py` (8 tests, 45/45 full suite). Ports
`object_builder/shunt/new_breaker.py`, `object_builder/switch/new_disconnector.py`.

Resolved against the Visio modeling reference diagram (Switch), which shows a
real subclass chain — `Wires::Switch` → `Wires::ProtectedSwitch` →
`Wires::Breaker`/`Wires::Recloser`/`Wires::LoadBreakSwitch`, plus
`Wires::Disconnector` as a `Switch` sibling. Built as a matching Python
subclass chain: `SwitchBuilder` (base) → `ProtectedSwitchBuilder(SwitchBuilder)`
→ `BreakerBuilder`/`RecloserBuilder`/`LoadBreakSwitchBuilder(ProtectedSwitchBuilder)`,
with `DisconnectorBuilder`/`FuseBuilder(SwitchBuilder)` as direct siblings.
Every leaf except `BreakerBuilder` (which adds `add_breaker_rating` for its
own `inTransitTime`) is a **pure `cim_class_name` override with zero new
code** — every inherited `add_*` method works unchanged because each one
only touches fields keyed off the object's own runtime type
(`graph_write.set_attr`'s `_part_field` exact-class-name match), never off
which builder subclass built it. This is the same reason `ObjectBuilder.create()`
(`cimbuilder/builders/base.py`) needs no override per subclass either.

Fixes the double-UUID bug (§1c.1) by construction — `add_connectivity` goes
through the existing generic `cimtables.connectivity.add_connectivity` for
both terminals, removing the hand-rolled per-terminal seeding
(`new_disconnector.py` seeded `t1`'s UUID twice and never seeded `t2`'s)
entirely. No `add_electrical` at all — correct, matching this plan's
original call — but the real split confirmed by reading every switch class's
body directly (not just grepping for a field name, which under-counted on an
earlier, too-narrow `sed` line range) is less even than first assumed:

- `open`/`normalOpen`/`retained`/`areaBoundary`/`topologicalUsage`/
  `gangOperated`/`motorOperated`/`remotelyOperated` are available on **every**
  leaf type (`Disconnector`/`Fuse`/`Breaker`/`LoadBreakSwitch`/`Recloser`),
  because `connectivity_unbalanced` and `steady_state_hypothesis` are the two
  part modules that define a same-named class for every one of them. `open`
  specifically lives in `steady_state_hypothesis`, not alongside the rest in
  `connectivity_unbalanced` — a different part module despite both classes
  sharing a word-for-word identical docstring. `add_switching` covers this
  shared set.
- `ratedCurrent` is **not** available on every leaf — it exists only in
  `electrical_balanced.Switch` and `electrical_unbalanced.Switch`, and
  neither of those part modules defines a `Disconnector`, `Fuse`, or
  `Recloser` class at all (only `Switch`/`ProtectedSwitch`/`Breaker`, plus
  `LoadBreakSwitch` in `electrical_unbalanced`). So `ratedCurrent` is only
  settable on `Switch`/`ProtectedSwitch`/`Breaker`/`LoadBreakSwitch`
  instances — deliberately left out of `add_switching` rather than offered
  and silently failing on half the leaves.
- `breakingCapacity` (`ProtectedSwitch`'s own field, `electrical_unbalanced`)
  has the identical gap one level up: `electrical_unbalanced` defines
  `ProtectedSwitch`/`Breaker`/`LoadBreakSwitch` but not `Recloser`, so
  `add_protection` (inherited by `RecloserBuilder`) raises on an actual
  `Recloser` instance — confirmed and locked in as a test
  (`test_recloser_builder_breaking_capacity_not_reachable`), not treated as a
  bug to route around, since it accurately reflects what this profile build
  supports today.
- `locked`/`loadBreak` (shown on the diagram's `WiresEXT::Switch`
  `ShadowExtension,GridAPPSD` box) don't exist anywhere in the installed
  package (`locked` only exists on the unrelated DC-system `DCSwitch`) — not
  set by this builder.
- `SwitchPhase` (the diagram's phase-level box) has no `sequenceNumber`; the
  existing generic `cimtables.connectivity.add_phase_children` already
  special-cases this shape (`phaseSide1`/`phaseSide2`, both set to the same
  `SinglePhaseKind`, in written-phase order) — reused unchanged via
  `add_connectivity(phases=...)`, same as `ACLineSegmentBuilder`.

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
