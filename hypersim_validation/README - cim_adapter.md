# cim_adapter.py — CIM to GLM Model Translation

## Purpose

`cim_adapter.py` is a translation layer that reads a CIM XML network file and exposes its content as an in-memory Python
dictionary that matches the module-level interface produced by `glmanip`. This
allows `Interpreter.py` to consume CIM-formatted power-system models through
the same `g.model[type][name][param]` access pattern it uses for native GLM
(GridLAB-D Model) input, without modification.

---

## Module-Level Data Structures

The module exposes the following top-level names, mirroring `glmanip`:

| Name | Type | Content |
|---|---|---|
| `model` | `dict` | Nested dict: `model[object_type][name][param]` |
| `coordinates_csv` | `str` | Path to generated bus-coordinate CSV, or `None` |

After a successful `ingest()` call, `model` contains keys for each modeled
object type: `node`, `load`, `overhead_line`, `underground_line`, `capacitor`,
`transformer`, `transformer_configuration`, `regulator`,
`regulator_configuration`, and `switch`.

---

## Main Components

### `ingest(fn, basedir='.')`

The primary entry point. Loads a CIM XML file, builds the internal
`cimgraph.models.FeederModel`, and then calls each component-specific
population function in sequence. The CIM17v40 profile is enforced via the
`CIMG_CIM_PROFILE` environment variable.

### `reset()`

Clears all module-level state back to empty defaults, allowing a fresh ingest
without restarting the interpreter.

### Component Population Functions

The adapter is organized around a central `model` dictionary and a set of element-specific ingestion functions, each responsible for one class of power system equipment. Each function below queries the `FeederModel` for a specific CIM class, maps its attributes to GLM field names, and writes entries into `model`:

| Function | CIM Source Class(es) | GLM Target Type(s) |
|---|---|---|
| `_add_nodes` | `ConnectivityNode`, `EnergySource` | `node` |
| `_add_loads` | `EnergyConsumer`, `EnergyConsumerPhase` | `load` |
| `_add_lines` | `ACLineSegment`, `ACLineSegmentPhase`, `PerLengthPhaseImpedance`, `PerLengthSequenceImpedance` | `overhead_line`, `underground_line` |
| `_add_capacitors` | `LinearShuntCompensator`, `LinearShuntCompensatorPhase` | `capacitor` |
| `_add_transformers` | `PowerTransformer`, `PowerTransformerEnd`, `TransformerMeshImpedance` | `transformer`, `transformer_configuration` |
| `_add_regulators` | `RatioTapChanger`, `TransformerTankEnd`, `TransformerTank` | `regulator`, `regulator_configuration` |
| `_add_switches` | All `Switch` subclasses, `SwitchPhase` | `switch` |
| `_generate_coordinates_csv` | `Location`, `PositionPoint` | CSV file |

- **`_add_nodes`** maps CIM `ConnectivityNode` objects to GLM `node` entries, resolving per-node voltage (line-to-neutral, derived from `BaseVoltage`) and phase membership (derived from `ACLineSegmentPhase` and `EnergyConsumerPhase` records). Nodes connected to an `EnergySource` are marked as swing buses.
- **`_add_loads`** converts `EnergyConsumer` and `EnergyConsumerPhase` records into GLM `load` entries with per-phase constant-power fields. When per-phase `EnergyConsumerPhase` records exist, their P/Q are used directly; when they are absent, the lumped P/Q on the `EnergyConsumer` is split evenly into thirds across phases A/B/C (the balanced-load case, e.g. IEEE13's `671`). It distinguishes delta from wye connections, and appends a `_ld` suffix to avoid name collisions with connectivity nodes. A consolidation pass (`_consolidate_loads`) merges single-phase loads sharing the same parent node into multi-phase entries.
- **`_add_lines`** translates `ACLineSegment` objects into `overhead_line` or `underground_line` entries, using `ACLineSegmentPhase` records for per-phase indexing. Impedance data is extracted from `PerLengthPhaseImpedance` (full phase-domain matrices) or `PerLengthSequenceImpedance` (sequence-to-phase conversion), producing R, L, and C matrices scaled by segment length.
- **`_add_capacitors`** converts `LinearShuntCompensator` and per-phase `LinearShuntCompensatorPhase` records into GLM `capacitor` entries, computing per-phase reactive power from nominal voltage, susceptance per section, and section count. As with loads, a balanced capacitor with no per-phase records has its total reactive power split evenly into thirds across A/B/C.
- **`_add_transformers`** maps `PowerTransformer` / `PowerTransformerEnd` pairs to GLM `transformer` and `transformer_configuration` entries. Per-unit resistance and reactance are derived from `TransformerMeshImpedance` when available, falling back to the primary winding's own impedance. Delta-grounded-wye connections are converted to an equivalent wye-wye representation.
- **`_add_regulators`** handles tank-based voltage regulators by grouping `RatioTapChanger`, `TransformerTankEnd`, and `TransformerTank` records under their parent `PowerTransformer`. Tap range, step increment, dwell time, and regulation band are emitted as `regulator_configuration` entries.
- **`_add_switches`** collects all `Switch` subclasses (breakers, reclosers, fuses, disconnectors, etc.), de-duplicates by mRID, and produces GLM `switch` entries with from/to connectivity, phase assignment (via `SwitchPhase` records), and open/closed status.
- **`_generate_coordinates_csv`** extracts spatial coordinates from CIM `Location` / `PositionPoint` data and writes a `Bus,X,Y` CSV file for node placement in downstream visualization.

---

## Workflow

```
CIM XML file
      │
      ▼
  ingest(fn)
      │
      ├─ FeederModel (cimgraph)
      │
      ├─ _add_nodes           → model['node']
      ├─ _add_loads           → model['load']
      │     └─ _consolidate_loads (merge single-phase entries)
      ├─ _add_lines           → model['overhead_line'] / model['underground_line']
      ├─ _add_capacitors      → model['capacitor']
      ├─ _add_transformers    → model['transformer'] / model['transformer_configuration']
      ├─ _add_regulators      → model['regulator'] / model['regulator_configuration']
      ├─ _add_switches        → model['switch']
      └─ _generate_coordinates_csv → <source>_buscoords.csv
```

---

## Key Implementation Details

**Voltage unit conversion.** CIM `BaseVoltage.nominalVoltage` and
`EnergySource.voltageMagnitude` are line-to-line (L-L) values. `Interpreter.py`
expects a node's `nominal_voltage` as a line-to-neutral (L-N) magnitude, so node
voltages stored in `model` are divided by √3. The per-phase `voltage_*` field of
a *delta-connected* load or capacitor is the exception: a delta element sees the
L-L magnitude, so its per-phase voltage is the node's L-N value multiplied back
by √3 (i.e. left at the original L-L value).

**Phase resolution.** CIM `Terminal` objects carry no `phases` field. Phase
membership is inferred from per-phase records (`ACLineSegmentPhase`,
`EnergyConsumerPhase`, `SwitchPhase`) via `_build_cn_phases_map()` and
`_get_phases()`. When no phase records exist, `ABCN` is assumed.

**Impedance conversion.** Line impedances are drawn from
`PerLengthPhaseImpedance` (full asymmetric 3×3 matrix). The matrix is scaled by segment length and converted
from Ω/unit to the `R_matrix`, `L_matrix`, `C_matrix` format GLM expects.
Single-phase segments yield scalar `R`, `L`, `C` values.

**Load consolidation.** Single-phase `EnergyConsumer` records sharing a parent
`ConnectivityNode` are merged into a single multi-phase `load` entry by
`_consolidate_loads()`, preventing `Interpreter.py` from emitting redundant
per-phase sub-objects with multiplexers.

**Skipped loads.** An `EnergyConsumer` is dropped (and reported in a warning
count) when it carries no usable A/B/C power: either every `EnergyConsumerPhase`
record resolves to a split-phase/triplex phase (`SinglePhaseKind.s1`/`s2`), or
it has no per-phase records and a lumped P and Q of zero. Split-phase/triplex
loads are not currently translated; they are skipped rather than fabricated as a
powerless `ABCN` entry. 

**Transformer impedance.** Winding resistance and reactance are taken from
`TransformerMeshImpedance` when available and converted to per-unit on the
winding's rated base. `DELTA_GWYE` connections are internally rewritten to
`WYE_WYE` with the primary voltage divided by √3.

**Regulator configuration.** Tap-changer range and step increment are read
from `RatioTapChanger` and converted to GLM `raise_taps`, `lower_taps`, and
`regulation` (step increment × raise count, expressed as a fraction of
nominal voltage). Per-phase tap positions are not emitted because the
`OrderedPhaseCodeKind` needed to map tank ends to phases is absent from the
CIM17v40 profile.

**Coordinate export.** Geographic coordinates are extracted from `Location` /
`PositionPoint` objects attached to every `ConductingEquipment` and written to
a CSV file (`<source>_buscoords.csv`) with columns `Bus`, `X`, `Y`. The path
is stored in `coordinates_csv` for downstream consumers.

---

## Expected Usage

```python
import cim_adapter as g

g.ingest('path/to/network.xml')

# Access populated model
for node_name, params in g.model['node'].items():
    print(node_name, params['nominal_voltage'])

# Optional: reset state before re-ingesting
g.reset()
g.ingest('path/to/other_network.xml')
```

`Interpreter.py` imports the adapter as a drop-in replacement for `glmanip`
and calls `g.ingest(fn)` before processing `g.model` through its normal
object-construction pipeline. The bus coordinate CSV path in
`g.coordinates_csv` can be passed to the layout engine if geographic placement
is required.

---

## Dependencies

| Package | Role |
|---|---|
| `cimgraph` | CIM XML parsing and graph traversal (`cim17v40` profile) |
| `csv` | Coordinate CSV output |
| `math` | Voltage unit conversion (√3), sequence-to-phase impedance |
| `inspect` | Dynamic enumeration of CIM class hierarchy |
| `os` | Environment variable and path manipulation |
