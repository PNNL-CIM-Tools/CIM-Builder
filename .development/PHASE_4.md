# Phase 4 — Session Classes

**Goal:** Wrap the functional layers (primitives, composites, topologies) in ergonomic `SubstationSession`, `FeederSession`, `NetworkSession` objects so notebook users don't have to thread `network + substation + base_voltage` through every call.

**Size:** 1 day

**Blocked by:** Phase 3

---

## Scope

### `session/substation_session.py`

```python
@dataclass
class SubstationSession:
    network: GraphModel
    substation: "cim.Substation"
    base_voltage: "cim.BaseVoltage"
    topology: str                         # 'single_bus' | 'breaker_and_a_half' | ...
    buses: dict[str, "cim.ConnectivityNode"]  # topology-specific bus refs
    profile: str | None = None

    @classmethod
    def single_bus(cls, connection, name, base_voltage, *, network=None, profile=None) -> SubstationSession: ...

    @classmethod
    def double_bus_single_breaker(cls, connection, name, base_voltage, *, network=None, profile=None) -> SubstationSession: ...

    @classmethod
    def main_and_transfer(cls, connection, name, base_voltage, *, network=None, profile=None) -> SubstationSession: ...

    @classmethod
    def ring_bus(cls, connection, name, base_voltage, *, total_sections=4, network=None, profile=None) -> SubstationSession: ...

    @classmethod
    def sectionalized_bus(cls, connection, name, base_voltage, *, total_sections=2, network=None, profile=None) -> SubstationSession: ...

    @classmethod
    def breaker_and_half(cls, connection, name, base_voltage, *, total_bus_ties=2, network=None, profile=None) -> SubstationSession: ...

    # Feeder / branch dispatch
    def add_feeder(self, breaker_number, feeder_network, feeder, *, sourcebus=None, **topology_kwargs) -> dict: ...
    def add_branch(self, breaker_number, branch_equipment, branch_terminal, **topology_kwargs) -> dict: ...

    # High-level composable methods (each creates a bay + attaches equipment)
    def add_capacitor(self, breaker_number, name, *, b_Mvar, **kwargs) -> "cim.LinearShuntCompensator": ...
    def add_power_transformer(self, breaker_number, name, *, template=None, **kwargs) -> dict: ...
    def add_generator(self, breaker_number, name, *, ratedS_MVA, **kwargs) -> "cim.SynchronousMachine": ...
    def add_load(self, breaker_number, name, *, p_MW, q_Mvar, **kwargs) -> "cim.EnergyConsumer": ...
    def add_der(self, breaker_number, name, *, p_MW, kind='pv', template=None, **kwargs) -> dict: ...

    # Serialization passthroughs
    def write_xml(self, path: str) -> None: ...
    def write_json_ld(self, path: str) -> None: ...
    def upload(self) -> None: ...
    def pprint(self, cim_class: type, **kwargs) -> None: ...
```

### `session/feeder_session.py`

Similar contract for building feeders step-by-step.

### `session/network_session.py`

Multi-substation holder. Manages the top-level `GraphModel`, holds references to `SubstationSession`s, supports inter-substation line creation (`add_transmission_line`).

### Profile handling

Sessions accept `profile=` argument. If `None`, the session uses whatever `CIMG_CIM_PROFILE` env var is set to (current behavior). If provided, the session sets it for the duration (implementation: save prior env, set new, restore on `__del__` or explicit `.close()`).

---

## Testing

`tests/session/`:
- `test_substation_session.py` — rebuild the `test_single_bus_with_multiple_feeders` scenario using the session API, diff CIM output against the functional-API version.
- `test_add_capacitor_workflow.py` — session-level composable workflow.
- `test_network_session.py` — multi-substation scenario.

---

## Exit criteria

- [ ] Session API supports every workflow the current class-based API supports.
- [ ] A notebook can create a multi-substation network in <20 lines using only sessions.
- [ ] Functional API is still the primary MCP/GUI surface; sessions are sugar.
