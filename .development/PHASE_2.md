# Phase 2 — Composite Builders

**Goal:** Build the multi-object chains that encode CIM domain knowledge — so users don't have to wire PowerTransformer + ends + tap changers + terminals by hand.

**Size:** 2 days

**Blocked by:** Phase 1

---

## Scope

Create `cimbuilder/composite_builder/`. Every composite:
- Takes `network, container, name, <topology>` positionally, like primitives
- Accepts a `template: CatalogEntry` (Pydantic) to pre-fill fields
- Calls primitives only — never constructs CIM objects directly
- Returns a dict with every created object keyed by role

### Files

- `composite_builder/tap_changing_transformer.py` — `new_tap_changing_transformer()`: PowerTransformer + N×PowerTransformerEnd + N×Terminal + RatioTapChanger + TapChangerControl. Accepts `PowerTransformerInfoCatalog`.
- `composite_builder/btm_pv_unit.py` — `new_btm_pv_unit()`: PEC + PhotovoltaicUnit + measurements (extracted from current `aggregate_feeder.py`).
- `composite_builder/ftm_pv_unit.py` — `new_ftm_pv_unit()`: same for front-of-meter.
- `composite_builder/battery_unit.py` — `new_battery_unit()`: PEC + BatteryUnit + SoC measurement.
- `composite_builder/wind_unit.py` — `new_wind_unit()`: PEC + PowerElectronicsWindUnit.
- `composite_builder/feeder_head_breaker.py` — `new_feeder_head_breaker()`: Breaker + FeederArea + boundary measurements (extracted from `aggregate_feeder.py`).
- `composite_builder/aggregate_feeder.py` — `new_aggregate_feeder()`: 30-line orchestrator calling the above. Uses `CIMUnit` throughout. Backwards-compatible signature with current `feeder_builder/aggregate_feeder.py`.
- `composite_builder/evse_station.py` — `new_evse_station()`: clean replacement for the 5 broken EVSE primitive files. Single function, `chargingMode` param, optional battery backing.

### Migration

- Move `cimbuilder/feeder_builder/aggregate_feeder.py` → `cimbuilder/composite_builder/aggregate_feeder.py`, rewrite using the new primitives.
- Move `cimbuilder/feeder_builder/insert_measurements.py` → `cimbuilder/composite_builder/` if it's still needed, or delete.
- Move `cimbuilder/feeder_builder/cim_measurement_manager.py` → `cimbuilder/composite_builder/` or delete (unused?).
- After migration, delete `cimbuilder/feeder_builder/` directory.

---

## Testing

Every composite: `tests/composite_builder/test_<name>.py` asserts the full CIM object graph shape — every primitive is created, terminals are wired, measurements are attached, units are correct.

### Diff test for aggregate_feeder
Run both the old and new `new_aggregate_feeder` against identical inputs (after Phase 1 lands); diff the resulting CIM object graphs. Modulo unit-correctness (old uses `*1000`, new uses `CIMUnit`), they must be equivalent.

---

## Exit criteria

- [ ] `new_aggregate_feeder` passes its existing integration test.
- [ ] `new_tap_changing_transformer` correctly builds from a `PowerTransformerInfoCatalog`.
- [ ] All 5 broken EVSE files (Phase 1 remnants) replaced by 1 primitive + 1 composite.
- [ ] `feeder_builder/` directory deleted.
