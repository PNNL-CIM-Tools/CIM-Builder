# Phase 1 — Templates & Primitives

**Goal:** Establish the catalog-shim layer and rewrite every universal primitive to the new signature pattern.

**Size:** 2 days

**Blocked by:** Phase 0

---

## Scope

### Templates

Build `cimbuilder/templates/` with Pydantic models mirroring `grid-kitchen/shared/cataloger/src/cataloger/models.py`:

- `templates/base.py` — `CatalogEntry` base class
- `templates/enums.py` — `WindingConnection`, `WireMaterial`, `WireInsulation`
- `templates/transformer.py` — `PowerTransformerEndCatalog`, `PowerTransformerInfoCatalog`, `TransformerTankEndCatalog`, `TransformerTankInfoCatalog`
- `templates/conductor.py` — `WireInfoCatalog`, `OverheadWireInfoCatalog`, `ConcentricNeutralCableInfoCatalog`, `TapeShieldCableInfoCatalog`
- `templates/shunt.py` — `LinearShuntCompensatorCatalog`
- `templates/load.py` — `EnergyConsumerCatalog`
- `templates/generator.py` — `SynchronousMachineCatalog`
- `templates/der.py` — (empty in Phase 1; populated in Phase 6 with NERC defaults)

### Primitives rewrite

Every builder below is rewritten to follow `STYLE_GUIDE.md` canonical signature, uses `get_cim()` + `TYPE_CHECKING`, uses `CIMUnit` for all quantities.

**Switch** (`object_builder/switch/`):
- `new_breaker.py` (moved from `shunt/` — where it currently lives)
- `new_disconnector.py` (from `switch/` — audit)
- `new_load_break_switch.py` (NEW)
- `new_fuse.py` (NEW)

**Transformer** (`object_builder/transformer/`):
- `new_power_transformer.py` (heavy rewrite; the current version's catalog_parser dependency is deleted)
- `new_power_transformer_end.py` (NEW — currently inlined in new_power_transformer)
- `new_ratio_tap_changer.py` (NEW — current `new_tap_changer.py` is broken stub)
- `new_tap_changer_control.py` (NEW)

**Line** (`object_builder/line/`):
- `new_ac_line_segment.py` (NEW)
- `new_per_length_sequence_impedance.py` (NEW)

**Shunt** (`object_builder/shunt/`):
- `new_linear_shunt_compensator.py` (replaces broken `new_capacitor.py`; delete new_capacitor.py)
- `new_energy_consumer.py` (moved from `load/`)

**Generator** (`object_builder/generator/`):
- `new_synchronous_machine.py` (renamed from `new_synchronous_generator.py`; use correct CIM class name)

**Inverter** (`object_builder/inverter/`):
- `new_power_electronics_connection.py` (audit existing)
- `new_photovoltaic_unit.py` (NEW)
- `new_battery_unit.py` (NEW)
- `new_wind_unit.py` (NEW — PowerElectronicsWindUnit)
- `new_evse.py` (replaces the 5 broken EVSE files)

**Topology** (`object_builder/topology/`):
- `new_bus_bar_section.py` (audit)
- `new_connectivity_node.py` (NEW — factored out from inline use in substation builders)
- `new_junction.py` (NEW — convenience alias that names ConnectivityNodes as "junctions")

**Base** (`object_builder/base/`):
- `new_base_voltage.py` (audit; currently exists but unimported)

**Generic** (`object_builder/generic/`):
- `new_one_terminal_object.py` (audit signature)
- `new_two_terminal_object.py` (audit signature)

**Measurement** (`object_builder/measurement/`):
- `new_analog.py` (audit for unit correctness)
- `new_discrete.py` (audit)

### Utils split

- Split `utils/utils.py` → `utils/terminal.py` (`terminal_to_node`) + `utils/base_voltage.py` (`get_or_create_base_voltage`, renamed from `get_base_voltage`)
- Keep `utils/get_source_bus.py` as `utils/source_bus.py` (rename file, same API)
- Delete `utils/catalog_parser.py` (replaced by templates)
- `utils/__init__.py` re-exports the public API

### Deletions

- `cimbuilder/object_builder/shunt/new_capacitor.py` (replaced by LinearShuntCompensator)
- `cimbuilder/object_builder/inverter/new_EVSE.py`, `new_EVSE_BU.py`, `new_EVSE_BV.py`, `new_EVSE_PEC.py`, `new_EVSE_PEU.py` (5 broken files → `new_evse.py` primitive + `composite_builder/evse_station.py` in Phase 2)
- `cimbuilder/utils/catalog_parser.py`

---

## Testing

Every primitive gets a `tests/object_builder/<category>/test_<name>.py` file. Minimum tests per primitive:
- Creation with all kwargs
- Creation with `template=`
- Template + explicit kwarg override
- CIM graph membership after creation
- Terminal connectivity

---

## Exit criteria

- [ ] All 20+ universal primitives have tests and pass.
- [ ] No primitive has `import cimhub_2023 as cim` at module level for runtime use — only under `TYPE_CHECKING`.
- [ ] `cimbuilder/templates/` is importable and round-trips a sample `PowerTransformerInfoCatalog` through Pydantic.
- [ ] All 5 broken EVSE primitive files deleted.
- [ ] `new_capacitor.py` deleted.
- [ ] Existing `tests/test_single_bus_integration.py` still passes (no regression against legacy topology code, which is untouched in Phase 1).
