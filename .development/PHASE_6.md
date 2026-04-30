# Phase 6 — Catalog Integration & Defaults

**Goal:** Plumb `template: CatalogEntry` through every builder that can be catalog-driven; ship NERC-aligned DER defaults from PDF sources.

**Size:** 1 day

**Blocked by:** Phase 5; user-provided NERC/IEEE PDFs for default content

---

## Scope

### Populate `templates/der.py`

Default Pydantic instances for:
- `NERC_PRC_024_PV_INVERTER` — based on NERC PRC-024 voltage/frequency ride-through for IBRs
- `NERC_PRC_024_BESS` — same for battery storage
- `IEEE_1547_2018_PV_INVERTER` — IEEE 1547-2018 category II/III default parameters
- (user-provided PDFs determine what else ships)

Each default instance is a module-level constant with a citation in its docstring:

```python
NERC_PRC_024_PV_INVERTER = PowerElectronicsConnectionCatalog(
    name='NERC_PRC_024_PV_INVERTER',
    description='NERC PRC-024-3 voltage/frequency ride-through defaults for PV inverters.',
    # ... parameters ...
)
"""
Source: NERC Reliability Standard PRC-024-3, Table 1 (Generator Frequency Protective
Relaying Settings) and Attachment 1 (Generator Voltage Ride-Through Time Duration Curve).
"""
```

### Template coverage checklist

Plumb `template: CatalogEntry | None = None` through these builders:

- [ ] `new_power_transformer` / `new_tap_changing_transformer` (`PowerTransformerInfoCatalog`)
- [ ] `new_ac_line_segment` (`OverheadWireInfoCatalog` → compute per-length impedance)
- [ ] `new_linear_shunt_compensator` (`LinearShuntCompensatorCatalog`)
- [ ] `new_energy_consumer` (`EnergyConsumerCatalog`)
- [ ] `new_btm_pv_unit` / `new_ftm_pv_unit` (DER templates)
- [ ] `new_battery_unit` (BESS template)
- [ ] `new_synchronous_machine` (`SynchronousMachineCatalog`)

Template → CIM field conversion logic lives in each builder, not in the template class. Templates stay pure data.

### Conductor → line segment impedance

When `new_ac_line_segment` receives an `OverheadWireInfoCatalog`, it must:
1. Use Carson's equations or a standard lookup to compute per-length R/X/B from the wire's AC resistance + GMR + geometry.
2. Build the `PerLengthSequenceImpedance` and attach it.

(This is non-trivial. Phase 6 may defer the full Carson's computation and ship a simpler approximation — record the deferral in PHASE_CHECKPOINT.)

### Documentation

- Add "Template precedence" section to `STYLE_GUIDE.md` if not already present.
- Example notebook in `docs/` showing template-driven construction.

---

## Testing

- Integration test: build a feeder using only templates + names. Compare generated CIM to a snapshot.
- Unit tests per builder: `template` alone; `template + override kwarg`; `kwarg without template`.

---

## Exit criteria

- [ ] Template-driven construction works for at least 10 builders.
- [ ] NERC/IEEE DER defaults ship with citations in docstrings.
- [ ] `cim-asset-manager` swap is documented as a single import-path change in a `TODO.md`.
