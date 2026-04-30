# Phase 3 — Topology Builders (Functional)

**Goal:** Port substation topologies from the current class-based `substation_builder/` module to a functional `topology_builder/` module, preserving behavior.

**Size:** 1.5 days

**Blocked by:** Phase 2

---

## Scope

- Rename `cimbuilder/substation_builder/` → `cimbuilder/topology_builder/`.
- Delete the `SubstationBuilder` ABC (`substation_builder.py`) — no replacement; sessions in Phase 4 take its role.
- Convert each topology class to three free functions:
  - `new_<topology>_substation(connection, name, base_voltage, *, network=None) -> dict`
  - `add_feeder_to_<topology>(network, substation, <bus(es)>, base_voltage, breaker_number, feeder_network, feeder, *, sourcebus=None) -> dict`
  - `add_branch_to_<topology>(network, substation, <bus(es)>, base_voltage, breaker_number, branch_equipment, branch_terminal) -> dict`

### Files

- `topology_builder/single_bus.py` — **already functional** (existing `single_bus_functions.py` pattern). Audit for compliance with new signature rules.
- `topology_builder/double_bus_single_breaker.py` — **already functional** (existing `double_bus_functions.py`). Audit.
- `topology_builder/main_and_transfer.py` — **NEW (port from class)**.
- `topology_builder/ring_bus.py` — **NEW (port from class)**.
- `topology_builder/sectionalized_bus.py` — **NEW (port from class)**.
- `topology_builder/breaker_and_a_half.py` — **NEW (port from class)**. Note: `add_feeder_to_breaker_and_half` takes an additional `tie_number` parameter; document this in the signature.
- `topology_builder/_bays.py` — shared internal helpers (disconnector-breaker-disconnector trio, 8-junction breaker-and-a-half bay, bus tie).

### Return shapes

Creation functions return:
```python
{
    'network': GraphModel,
    'substation': cim.Substation,
    'main_bus': cim.ConnectivityNode,    # or multiple buses for multi-bus topologies
    'base_voltage': cim.BaseVoltage,
}
```

Multi-bus topologies replace `main_bus` with the appropriate named buses, e.g.:
- `double_bus_single_breaker`: `{'north_bus': ..., 'south_bus': ...}`
- `breaker_and_a_half`: `{'main_bus_1': ..., 'main_bus_2': ...}`
- `ring_bus`: `{'buses': [cn1, cn2, ...]}`
- `sectionalized_bus`: `{'buses': [cn1, cn2, ...]}`

`add_feeder_to_*` returns:
```python
{
    'breaker': cim.Breaker,
    'disconnectors': list[cim.Disconnector],
    'junctions': list[cim.ConnectivityNode],
}
```

---

## Testing

`tests/topology_builder/test_<topology>.py` per topology:
- Create substation
- Add 2 feeders + 1 branch
- Assert CIM object graph: expected breaker count, disconnector count, junction count, feeder linkage (`NormalEnergizingSubstation`)
- Export to XML, validate file contents

---

## Exit criteria

- [ ] All 6 topologies work as free functions with consistent return shapes.
- [ ] `substation_builder/` directory removed (shims for legacy classes come in Phase 5).
- [ ] Bay patterns factored into `_bays.py` helpers (no inline duplication across topologies).
- [ ] `tests/test_single_bus_integration.py` continues to pass (it uses `single_bus_functions` which survived the rename).
