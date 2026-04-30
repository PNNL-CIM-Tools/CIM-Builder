# Phase 5 — Back-Compat Shims & Migration Docs

**Goal:** Don't break existing notebooks and scripts that import `SingleBusSubstation` etc.

**Size:** 0.5 day

**Blocked by:** Phase 4

---

## Scope

- Create `cimbuilder/_deprecated/substation_classes.py`. For each of the 6 topologies:
  - Define a class with the old constructor signature.
  - In `__post_init__` (or `__init__`), call the corresponding `SubstationSession.<topology>(...)` factory.
  - Emit `DeprecationWarning` once per class on instantiation.
  - Delegate `.new_feeder(...)`, `.new_branch(...)`, `.upload()`, `.write_xml(...)`, `.write_json_ld(...)`, `.pprint(...)` to the session.
- Re-export the shims from `cimbuilder.__init__` at the bottom (after the new API) so `from cimbuilder import SingleBusSubstation` works.
- Run `tests/test_single_bus_integration.py` unchanged against the shims — must pass.

### Shim shape

```python
@dataclass
class SingleBusSubstation:
    connection: ConnectionInterface
    network: GraphModel = field(default=None)
    name: str = field(default='new_single_bus_sub')
    base_voltage: int | "cim.BaseVoltage" = field(default=115000)
    total_sections: int = field(default=4)   # accepted but ignored (pattern only)

    def __post_init__(self):
        warnings.warn(
            "SingleBusSubstation is deprecated; use SubstationSession.single_bus(...).",
            DeprecationWarning, stacklevel=2,
        )
        self._session = SubstationSession.single_bus(
            self.connection, name=self.name, base_voltage=self.base_voltage,
            network=self.network,
        )
        # Expose old attributes for back-compat
        self.network = self._session.network
        self.substation = self._session.substation
        self.main_bus = self._session.buses['main_bus']
        self.base_voltage = self._session.base_voltage
        self.cim = get_cim()

    def new_feeder(self, breaker_number, feeder_network, feeder, sourcebus=None):
        return self._session.add_feeder(breaker_number, feeder_network, feeder, sourcebus=sourcebus)

    def new_branch(self, breaker_number, branch_equipment, branch_terminal):
        return self._session.add_branch(breaker_number, branch_equipment, branch_terminal)

    def upload(self): self._session.upload()
    def write_xml(self, filename): self._session.write_xml(filename)
    def write_json_ld(self, filename): self._session.write_json_ld(filename)
    def pprint(self, cim_class, show_empty=False, json_ld=False, use_names=False):
        self._session.pprint(cim_class, show_empty=show_empty, json_ld=json_ld, use_names=use_names)
```

### Migration guide

- `docs/MIGRATION.md` with a side-by-side block per topology:
  - Old: `sub = SingleBusSubstation(connection=conn, name='s1', base_voltage=115000)`
  - New: `sub = SubstationSession.single_bus(connection=conn, name='s1', base_voltage=115000)`
- Explain the dict-return shape change for `add_feeder` vs `new_feeder` (new API returns a dict; old returned `None`).

---

## Exit criteria

- [ ] `from cimbuilder import SingleBusSubstation` still works and emits `DeprecationWarning`.
- [ ] `tests/test_single_bus_integration.py` passes unchanged.
- [ ] `docs/MIGRATION.md` covers all 6 topologies.
